from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_production_ui_uses_state_driven_investigation_map_not_board_mechanics():
    source = (ROOT / "src/main.jsx").read_text(encoding="utf-8")
    assert "INVESTIGATION MAP" in source
    assert "map-node" in source
    assert "experimentRegistry.map" in source
    assert "board.png" not in source
    for obsolete in ("action points", "action_points", "dice", "pawn movement", "inventory", "rounds"):
        assert obsolete not in source.lower()
    assert "}%" not in source


def test_board_artifact_is_not_a_production_reference():
    production = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "src").rglob("*") if path.is_file())
    assert "board.png" not in production
