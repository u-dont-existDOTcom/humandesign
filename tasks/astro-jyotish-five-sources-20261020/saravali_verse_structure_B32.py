"""Hash-gated source-structure audit only, not source critical edition or forecast."""
import argparse,bisect,hashlib,json,re,fitz
from pathlib import Path
SHA='b6fd2523fb349095a8a595e7d9750bacd8ff0ec7f495a0b58287a38f2c79baa6'
CH=re.compile(r'(?im)^\s*Chapter\s+(\d+)\s*$')
SL=re.compile(r'(?i)\bSlokas?\s+(\d+)\s*\.\s*(?:[-–—]\s*([0-9lI]+)\s*\.)?')
def audit(pdf,expanded=False):
 b=Path(pdf).read_bytes()
 if hashlib.sha256(b).hexdigest()!=SHA:raise ValueError('Wrong uploaded PDF')
 doc=fitz.open(stream=b,filetype='pdf')
 pp=[doc[i].get_text('text') for i in range(4,len(doc))]
 off=[];s=0
 for x in pp:off.append(s);s+=len(x)+1
 txt='\n'.join(pp);chs=list(CH.finditer(txt))
 if [int(m.group(1)) for m in chs]!=list(range(1,56)):raise ValueError('Chapter error')
 rows=[];issues=[]
 for i,m in enumerate(chs):
  ch=int(m.group(1));end=chs[i+1].start() if i<54 else len(txt)
  nums=set();ranges=[]
  for n in SL.finditer(txt,m.end(),end):
   lo=int(n.group(1));raw=n.group(2);hi=int(raw.replace('l','1').replace('I','1')) if raw else lo
   if raw and raw!=str(hi):issues.append(['text-layer 1/l confusion',ch,n.group(0)])
   if hi<lo:
    if (ch,lo,hi)!=(47,44,15):raise ValueError('Unverified descending range')
    issues.append(['English printed descending 44–15; Sanskrit 44–45',ch,n.group(0)])
    hi=45
   if any(k in nums for k in range(lo,hi+1)):raise ValueError('Repeated number')
   nums.update(range(lo,hi+1));ranges.append([lo,hi,5+bisect.bisect_right(off,n.start())-1])
  if nums!=set(range(1,max(nums)+1)):raise ValueError('Number gap')
  rows.append({'chapter':ch,'page':5+bisect.bisect_right(off,m.start())-1,'headings':len(ranges),'verses':len(nums),**({'ranges':ranges} if expanded else {})})
 if len(issues)!=2 or sum(x['headings'] for x in rows)!=1429 or sum(x['verses'] for x in rows)!=2532:raise ValueError('Count differs')
 return {'source_sha256':SHA,'chapters':55,'range_headings':1429,'numbered_verse_units':2532,'exceptions':issues,'rows':rows,'scope':'English source numbering structure only. No predictive or Sanskrit critical validation.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('pdf');p.add_argument('--ranges',action='store_true');a=p.parse_args()
 print(json.dumps(audit(a.pdf,a.ranges),ensure_ascii=False,indent=2))
