"""Save references to pinned IsaacDocs attack blocks; no inference of unlock requirements."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--isaacdocs',required=True,type=Path);args=p.parse_args()
commit=subprocess.check_output(['git','-C',str(args.isaacdocs),'rev-parse','HEAD'],text=True).strip()
source={}
for row in json.loads((ROOT/'data/boss-guides.json').read_text()):
 file=row['sourceFile'];lines=(args.isaacdocs/'docs/entities/bosses'/file).read_text().splitlines()
 name=row.get('sourceBoss',row['en']);blocks=[]
 starts=[i for i,line in enumerate(lines) if line.startswith('|') and line.split('|')[1].strip() not in ['', 'Boss','-']]
 for n,index in enumerate(starts):
  label=lines[index].split('|')[1].strip()
  if label==name or label.startswith(name+' ('):
   end=starts[n+1] if n+1<len(starts) else len(lines)
   attacks=[line.split('|')[3].strip() for line in lines[index:end] if line.startswith('|') and len(line.split('|'))>4]
   blocks.append({'label':label,'startLine':index+1,'endLine':end,'attacks':list(dict.fromkeys(a for a in attacks if a))})
 if not blocks:raise ValueError('Missing state source: '+row['id']+' / '+name)
 source[row['id']]={'file':file,'blocks':blocks}
(ROOT/'data/boss-state-source.json').write_text(json.dumps({'isaacDocsCommit':commit,'bosses':source},ensure_ascii=False,indent=2)+'\n')
print('Pinned attack references:',len(source),'at',commit[:7])
