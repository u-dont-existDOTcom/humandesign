/* Exact six-rule maximum finder; no interpolation or date priors.
 * Calls installed Swiss Ephemeris. Run only in separate processes. */
#include <stdint.h>
#include <math.h>
#include <stdio.h>
#include <dlfcn.h>
typedef int32_t (*calc_fn)(double,int32_t,int32_t,double*,char*);
typedef int (*houses_fn)(double,int32_t,double,double,int,double*,double*);
typedef void (*path_fn)(const char*);
typedef void (*sid_fn)(int32_t,double,double);
static calc_fn calc; static houses_fn houses;
static char error_text[512];
static const int rulers[12]={4,3,2,1,0,2,3,4,5,6,6,5};
static double norm(double x){x=fmod(x,360.0);return x<0?x+360.0:x;}
static double sep(double a,double b){return fabs(norm(a-b+180.0)-180.0);}
const char* scan_error(void){return error_text;}
int scan_init(const char *library,const char *ephe){
 void *h=dlopen(library,RTLD_NOW|RTLD_LOCAL);
 if(!h){snprintf(error_text,512,"dlopen: %s",dlerror());return -1;}
 calc=(calc_fn)dlsym(h,"swe_calc_ut"); houses=(houses_fn)dlsym(h,"swe_houses_ex");
 path_fn path=(path_fn)dlsym(h,"swe_set_ephe_path");
 sid_fn sid=(sid_fn)dlsym(h,"swe_set_sid_mode");
 if(!calc||!houses||!path||!sid){snprintf(error_text,512,"Swiss symbols absent");return -2;}
 path(ephe);sid(1,0,0);return 0;
}
static int planet(double jd,int p,int sid,double* value){
 double x[6];char err[256]={0};int32_t flags=258|(sid?65536:0);
 int32_t got=calc(jd,p,flags,x,err);
 if(got<0||(got&4)||!(got&2)||!isfinite(x[0])){snprintf(error_text,512,"ephemeris failure jd=%.12f body=%d flags=%d %s",jd,p,got,err);return -1;}
 *value=norm(x[0]);return 0;
}
static int house(double x,const double *c){
 for(int i=1;i<=12;i++){
  double span=norm(c[i==12?1:i+1]-c[i]);
  if(norm(x-c[i])<span)return i;
 }
 return -1;
}
static int place_sign(double x){return (int)(norm(x)/30.0);}
/* Bit order = manifest order. fast stops at a failed necessary condition. */
int scan_mask(double jd,double lat,double lon,int fast,int *trace){
 double c[13],a[10],sc[13],sa[10],v[7],sv;
 int mask=0,ok,h,p;for(int j=0;j<7;j++)v[j]=NAN;
 if(houses(jd,0,lat,lon,'R',c,a)<0){snprintf(error_text,512,"Regiomontanus failure");return -1;}
 if(planet(jd,3,0,&v[3]))return -1;
 h=house(v[3],c);ok=h==2||h==5;if(ok)mask|=4;else if(fast){*trace=0;return mask;}
 if(houses(jd,65536,lat,lon,'P',sc,sa)<0||planet(jd,3,1,&sv)){snprintf(error_text,512,"sidereal failure");return -1;}
 h=(place_sign(sv)-place_sign(sa[0])+12)%12+1;ok=h==4;if(ok)mask|=8;else if(fast){*trace=1;return mask;}
 if(planet(jd,6,0,&v[6])||planet(jd,5,0,&v[5]))return -1;
 ok=fabs(sep(v[6],v[3])-120.0)<=1.0||fabs(sep(v[6],v[5])-120.0)<=1.0;
 if(ok)mask|=2;else if(fast){*trace=2;return mask;}
 p=rulers[place_sign(c[3])];if(isnan(v[p])&&planet(jd,p,0,&v[p]))return -1;
 h=house(v[p],c);ok=h==1||h==10;if(ok)mask|=1;else if(fast){*trace=3;return mask;}
 p=rulers[place_sign(c[10])];if(isnan(v[p])&&planet(jd,p,0,&v[p]))return -1;
 ok=(p!=3&&sep(v[p],v[3])<=1.0)||(p!=5&&sep(v[p],v[5])<=1.0);
 if(ok)mask|=16;else if(fast){*trace=4;return mask;}
 p=rulers[place_sign(c[7])];if(isnan(v[p])&&planet(jd,p,0,&v[p]))return -1;
 h=house(v[p],c);ok=h==4||h==7||h==11;if(ok)mask|=32;else if(fast){*trace=5;return mask;}
 *trace=6;return mask;
}
/* Every integer minute offset examined exactly once. Counts sum to range size. */
int64_t scan_range(double start,int64_t first,int64_t end,double lat,double lon,
 int64_t *hits,int64_t capacity,int64_t *counts){
 int64_t used=0;for(int i=0;i<7;i++)counts[i]=0;
 for(int64_t idx=first;idx<end;idx++){
  int trace=0;int mask=scan_mask(start+(double)idx/1440.0,lat,lon,1,&trace);
  if(mask<0)return -1;
  counts[trace]++;
  if(mask==63){if(used>=capacity){snprintf(error_text,512,"hit-buffer overflow");return -2;}hits[used++]=idx;}
 }
 return used;
}
