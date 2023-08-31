import pytest
from pytest import approx
import numpy as np

from spike2py import trial


def test_trial_init_defaults(trial_default):
    info = trial.TrialInfo(file=trial_default)
    trial1 = trial.Trial(info)
    assert trial1.info.file == trial_default
    assert trial1.info.channels is None
    assert trial1.info.name == "tremor_kinetic"
    assert trial1.info.subject_id == "sub"
    assert trial1.info.path_save_figures == trial_default.parent / "figures"
    assert trial1.info.path_save_trial == trial_default.parent / "data"


def test_trial_init_fully_loaded(trial_info_dict):
    info = trial.TrialInfo(**trial_info_dict)
    trial1 = trial.Trial(info)
    assert trial1.info.file == trial_info_dict["file"]
    assert trial1.info.channels == trial_info_dict["channels"]
    assert trial1.info.name == trial_info_dict["name"]
    assert trial1.info.subject_id == trial_info_dict["subject_id"]
    assert trial1.info.path_save_figures == trial_info_dict["path_save_figures"]
    assert trial1.info.path_save_trial == trial_info_dict["path_save_trial"]


def test_trial_init_fully_loaded_channel_error_sys_exit(
    trial_info_dict_channel_error, capsys
):
    info = trial.TrialInfo(**trial_info_dict_channel_error)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        trial1 = trial.Trial(info)
    captured = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == (
        (
            "Channel K_angle does not exist in biomech0deg.mat. \n"
            "Available channels include:\n"
            "\n"
            "prox_EMG\n"
            "dist_EMG\n"
            "k_angle\n"
            "k_torque\n"
            "Trig\n"
            "Keyboard\n"
        )
    )


@pytest.mark.parametrize("channel", ["Flex", "Ext", "Angle", "Triangle", "Keyboard"])
def test_trial_init_channels_present(trial_default, channel):
    info = trial.TrialInfo(file=trial_default)
    trial1 = trial.Trial(info)
    assert channel in trial1.__dir__()


def test_trial_save(payload_dir, trial_default):
    info = trial.TrialInfo(file=trial_default)
    trial1 = trial.Trial(info)
    trial1.save()
    pickled_file = payload_dir / "data" / "tremor_kinetic.pkl"
    assert pickled_file.exists()


def test_trial_read(payload_dir, trial_default):
    file = payload_dir / "tremor_kinetic.pkl"
    trial1 = trial.load(file)
    assert isinstance(trial1, trial.Trial)
    assert np.mean(trial1.Angle.values) == approx(1.87862485065)
    assert "Flex" in trial1.__dir__()
