"""Rebuild source-derived facts in a disposable copy; fail on drift or missing output."""
import hashlib,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def signatures(root):
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
         for area in ['docs','data','local-tools/progress'] for p in (root/area).rglob('*')
         if p.is_file() and '.vitepress/dist' not in str(p) and '.vitepress/cache' not in str(p)}
before=signatures(ROOT)
with tempfile.TemporaryDirectory() as directory:
 work=Path(directory)/'repo'
 shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('.git','node_modules','dist','cache','__pycache__'))
 for script in ['generate-achievements','generate-tool-data','generate-mode-rewards','generate-completion-rewards','generate-entry-pages','generate-synergy-guide','generate-challenge-pages','generate-reference-pages','generate-save-progress-data']:
  subprocess.run(['python3',str(work/'scripts'/f'{script}.py')],cwd=work,check=True,stdout=subprocess.DEVNULL)
 after=signatures(work)
 changed=[path for path in sorted(before.keys()|after.keys()) if before.get(path)!=after.get(path)]
 if changed:
  print('Generated content is stale. Run the generators:\n'+'\n'.join(changed))
  raise SystemExit(1)
print('PASS deterministic generated pages, catalogs, rewards and offline lookup data')
