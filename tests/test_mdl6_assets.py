from pathlib import Path
from PIL import Image

from scripts import audio_preflight, image_preflight


def test_packaged_images_meet_mdl6_budget():
    image_preflight.main()


def test_production_audio_meets_mdl6_budget():
    audio_preflight.main()
    assert (Path(__file__).parents[1] / "public/audio/mad_data_lab_curiosity.mp3").is_file()


def test_mdl6_production_artwork_manifest_and_alpha_contract():
    root = Path(__file__).parents[1]
    manifest = root / "assets/review/MDL-6/art-candidates.json"
    assert manifest.is_file()
    badge = root / "public/assets/mdl6-achievement-badges.png"
    recovery = root / "public/assets/mdl6-recovery-background.png"
    with Image.open(badge) as image:
        assert image.format == "PNG"
        assert image.mode == "RGBA"
        assert image.width >= 512 and image.height >= 512
    with Image.open(recovery) as image:
        assert image.format == "PNG"
        assert image.width / image.height > 1.5
