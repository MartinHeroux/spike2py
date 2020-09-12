import pytest
import matplotlib.pyplot as plt
from pathlib import Path

from spike2py.trial import TrialInfo, Trial


@pytest.mark.mpl_image_compare(baseline_dir=str(Path('.') / "baseline"))
def test_waveform(physiology_data):
    trial_info = TrialInfo(physiology_data)
    physiology = Trial(trial_info)
    plt.close("all")
    physiology.Abdo.plot()
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir=str(Path('.') / "baseline"))
def test_event(physiology_data):
    trial_info = TrialInfo(physiology_data,)
    physiology = Trial(trial_info)
    plt.close("all")
    physiology.Magnet.plot()
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir=str(Path('.') / "baseline"))
def test_keyboard(physiology_data):
    trial_info = TrialInfo(physiology_data,)
    physiology = Trial(trial_info)
    plt.close("all")
    physiology.Keyboard.plot()
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir=str(Path('.') / "baseline"))
def test_entire_trial1(physiology_data):
    trial_info = TrialInfo(physiology_data,)
    physiology = Trial(trial_info)
    plt.close("all")
    physiology.plot()
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir=str(Path('.') / "baseline"))
def test_entire_trial2(motor_units_data):
    trial_info = TrialInfo(motor_units_data)
    motor_units = Trial(trial_info)
    plt.close("all")
    motor_units.plot()
    return plt.gcf()


@pytest.mark.mpl_image_compare(baseline_dir=str(Path('.') / "baseline"))
def test_wavemark(motor_units_data):
    trial_info = TrialInfo(motor_units_data)
    motor_units = Trial(trial_info)
    plt.close("all")
    motor_units.Mu2.plot()
    return plt.gcf()
