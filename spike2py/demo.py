from pathlib import Path

import matplotlib.pyplot as plt

from spike2py import trial


def test_install():
    info = trial.TrialInfo(file=Path("tests") / "payloads" / "motor_units.mat")
    sample = trial.Trial(info)
    plt.close('all')
    print('\nFigure 1: sample.Flow.plot()\n'
          'Figure 2: sample.Flow.lowpass(cutoff=4, order=8).plot()\n'
          'Figure 3: sample.Volume.plot()\n'
          'Figure 4: sample.Volume.remove_mean().linear_detrend().lowpass(cutoff=5).plot()\n'
          'Figure 5: sample.plot()\n')
    sample.Flow.plot()
    sample.Flow.lowpass(cutoff=4, order=8).plot()
    sample.Volume.plot()
    sample.Volume.remove_mean().linear_detrend().lowpass(cutoff=5).plot()
    sample.plot()


def tutorial_data():
    info = trial.TrialInfo(file=Path("tests") / "payloads" / "motor_units.mat")
    sample = trial.Trial(info)
    return sample
