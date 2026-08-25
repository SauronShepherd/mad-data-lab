import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data.generation import generate_case
from data.generation.validators import validate_case

if __name__ == '__main__':
    c=generate_case(); validate_case(c.public); print('PASS', c.content_hash)
