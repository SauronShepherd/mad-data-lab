from pathlib import Path

from scripts import audio_preflight, image_preflight


def test_packaged_images_meet_mdl6_budget():
    image_preflight.main()


def test_production_audio_meets_mdl6_budget():
    audio_preflight.main()
    assert (Path(__file__).parents[1] / "public/audio/mad_data_lab_curiosity.mp3").is_file()
