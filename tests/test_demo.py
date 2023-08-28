import os
from pathlib import Path

import pytest

from spike2py import demo


@pytest.mark.demo
def test_get_demo_data_from_S3():
    x = demo._get_demo_data_from_S3()
    tmp = os.getenv("TMP", "/tmp")
    assert x == Path(tmp) / "motor_units.mat"


@pytest.mark.demo
def test_install(capsys):
    demo.test_install()
    captured = capsys.readouterr()
    assert captured.out == (
        "\nFigure 1: sample.Flow.plot()\n"
        "Figure 2: sample.Flow.lowpass(cutoff=4, order=8).plot()\n"
        "Figure 3: sample.Volume.plot()\n"
        "Figure 4: sample.Volume.remove_mean().linear_detrend().lowpass(cutoff=5).plot()\n"
        "Figure 5: sample.plot()\n\n"
    )


@pytest.mark.demo
def test_tutorial_data(tutorial_data_dict):
    actual = demo.tutorial_data()
    assert actual.info.file == tutorial_data_dict["file"]
    assert actual.channels == tutorial_data_dict["channels"]
