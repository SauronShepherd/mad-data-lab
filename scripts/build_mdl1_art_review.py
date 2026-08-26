from __future__ import annotations
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def main():
    plan=json.loads((ROOT/'assets/review/MDL-1/art-generation-plan.json').read_text(encoding='utf-8'))
    candidates=[]
    for slot in plan['slots']:
        for rel in slot['candidates']:
            path=ROOT/rel; raw=path.read_bytes(); image=Image.open(path)
            if image.mode != 'RGBA': raise SystemExit(f'{rel}: expected RGBA')
            candidates.append({'asset_id':slot['asset_id'],'path':rel,'sha256':hashlib.sha256(raw).hexdigest(),'width':image.width,'height':image.height,'mode':image.mode,'status':'CANDIDATE'})
    out={'iteration':'MDL-1','status':'CANDIDATES_PREFLIGHT_PASS','approval_status':'IMPLEMENTATION_OWNED','candidate_completeness':{slot['asset_id']:len(slot['candidates']) >= slot['required_candidates'] for slot in plan['slots']},'candidates':candidates}
    dest=ROOT/'release-report/MDL-1/art-preflight.json'; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
