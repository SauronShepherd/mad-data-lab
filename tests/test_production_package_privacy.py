from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_production_package_excludes_private_truth_inputs():
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")
    databricksignore = (ROOT / ".databricksignore").read_text(encoding="utf-8")
    for content in (dockerignore, databricksignore):
        assert "data/generation/private_specs/" in content
        assert "data/fixtures/private/" in content
