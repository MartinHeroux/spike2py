import os
from urllib.request import urlretrieve
from pathlib import Path

import matplotlib.pyplot as plt

from spike2py import trial

DEMO_DATA_S3 = "https://spike2py.s3-ap-southeast-2.amazonaws.com/motor_units.mat"


def test_install():
    demo_data_local = _get_demo_data_from_S3()
    info = trial.TrialInfo(file=demo_data_local)
    sample = trial.Trial(info)
    print(
        "\nFigure 1: sample.Flow.plot()\n"
        "Figure 2: sample.Flow.lowpass(cutoff=4, order=8).plot()\n"
        "Figure 3: sample.Volume.plot()\n"
        "Figure 4: sample.Volume.remove_mean().linear_detrend().lowpass(cutoff=5).plot()\n"
        "Figure 5: sample.plot()\n"
    )
    plt.close("all")
    sample.Flow.plot()
    sample.Flow.lowpass(cutoff=4, order=8).plot()
    sample.Volume.plot()
    sample.Volume.remove_mean().linear_detrend().lowpass(cutoff=5).plot()
    sample.plot()


def _get_demo_data_from_S3():
    tmp = os.getenv("TMP", "/tmp")
    demo_data_local = os.path.join(tmp, os.path.basename(DEMO_DATA_S3))
    urlretrieve(DEMO_DATA_S3, demo_data_local)
    return Path(demo_data_local)


def tutorial_data():
    demo_data_local = _get_demo_data_from_S3()
    info = trial.TrialInfo(file=demo_data_local)
    sample = trial.Trial(info)
    return sample
