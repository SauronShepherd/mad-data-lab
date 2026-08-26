from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
def main():
    plan=json.loads((ROOT/'assets/review/MDL-2/art-generation-plan.json').read_text(encoding='utf-8'))
    candidates=[]
    for slot in plan['slots']:
        if len(slot['candidates']) != slot.get('required_candidates', 3):
            raise SystemExit(f"{slot['asset_id']}: candidate count is incomplete")
        sheet = ROOT / slot['contact_sheet']
        if hashlib.sha256(sheet.read_bytes()).hexdigest() != slot['contact_sheet_sha256']:
            raise SystemExit(f"{slot['asset_id']}: contact sheet hash mismatch")
        for rel in slot['candidates']:
            path=ROOT/rel; raw=path.read_bytes(); image=Image.open(path)
            candidate_match = re.search(r'candidate-(\d{3})\.png$', rel)
            if not candidate_match or int(candidate_match.group(1)) not in (1, 2, 3):
                raise SystemExit(f'{rel}: expected stable C01-C03 candidate slot')
            if image.mode != 'RGBA': raise SystemExit(f'{rel}: expected RGBA')
            candidates.append({'asset_id':slot['asset_id'],'candidate_id':f"{slot['asset_id']}-C{int(candidate_match.group(1)):02d}",'path':rel,'sha256':hashlib.sha256(raw).hexdigest(),'width':image.width,'height':image.height,'mode':image.mode,'status':'CANDIDATE'})
    out={'iteration':'MDL-2','status':'CANDIDATES_PREFLIGHT_PASS','approval_status':'IMPLEMENTATION_OWNED','candidates':candidates}
    dest=ROOT/'release-report/MDL-2/art-preflight.json'; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(out,indent=2,sort_keys=True),encoding='utf-8'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
