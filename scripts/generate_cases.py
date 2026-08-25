import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output', default='data/fixtures/public/case_0042.bundle.json'); ap.add_argument('--seed', type=int, default=42); args=ap.parse_args()
    c=generate_case(seed=args.seed)
    path=Path(args.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(json.dumps(c.canonical, ensure_ascii=False, sort_keys=True, indent=2).encode())
    private=Path('data/fixtures/private/case_0042_truth.json'); private.parent.mkdir(parents=True, exist_ok=True); private.write_bytes(json.dumps(c.private, ensure_ascii=False, sort_keys=True, indent=2).encode())
    Path('data/fixtures/hashes').mkdir(parents=True, exist_ok=True); Path('data/fixtures/hashes/case_0042.sha256').write_text(c.content_hash+'\n', encoding='utf-8')
    print(c.content_hash)
if __name__ == '__main__': main()
