#!/usr/bin/env python3
import lzma, struct, numpy as np
def decode(path):
    raw=lzma.decompress(open(path,"rb").read()); q0,d1,n,step=struct.unpack("<qiId",raw[:24]); dd=np.frombuffer(raw[24:],dtype="<i4").astype(np.int64); d=np.empty(n-1,dtype=np.int64); d[0]=d1
    if n>2: d[1:]=d1+np.cumsum(dd)
    q=np.empty(n,dtype=np.int64); q[0]=q0; q[1:]=q0+np.cumsum(d); return ((q/1e5)%360).astype(np.float64),step
def interpolate(path,start_jd,target_jd):
    a,step=decode(path); x=(np.asarray(target_jd)-start_jd)*24/step; i=np.floor(x).astype(int); f=x-i; i=np.clip(i,0,len(a)-2); b=a[i]; c=a[i+1]; delta=((c-b+180)%360)-180; return (b+f*delta)%360
