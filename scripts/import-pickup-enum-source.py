"""Snapshot numeric pickup facts, without inferring costs or loot odds from enums."""
import argparse,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--isaacdocs',type=Path,required=True);a=p.parse_args()
tables={}
for name in ['PickupVariant','HeartSubType','CoinSubType','KeySubType','BombSubType','BatterySubType','ChestSubType']:
 tables[name]={key:int(value) for value,key in re.findall(r'\|(\d+)\s*\|([A-Z][A-Z0-9_]+)',(a.isaacdocs/'docs/enums'/f'{name}.md').read_text())}
(ROOT/'data/pickup-enum-source.json').write_text(json.dumps({'isaacDocsCommit':subprocess.check_output(['git','-C',str(a.isaacdocs),'rev-parse','HEAD'],text=True).strip(),'enums':tables},ensure_ascii=False,indent=2)+'\n')
print('Pinned',len(tables),'pickup enum tables')
