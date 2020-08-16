import pytest

import numpy as np

from spike2py import trial


def test_trial_init_defaults(trial_default):
    info = trial.TrialInfo(file=trial_default)
    trial1 = trial.Trial(info)
    assert trial1.trial_info.file == trial_default
    assert trial1.trial_info.channels is None
    assert trial1.trial_info.name == "TRIAL"
    assert trial1.trial_info.subject_id == "sub"
    assert trial1.trial_info.path_save_figures == trial_default.parent / "figures"
    assert trial1.trial_info.path_save_trial == trial_default.parent / "data"


def test_trial_init_fully_loaded(trial_info_dict):
    info = trial.TrialInfo(**trial_info_dict)
    trial1 = trial.Trial(info)
    assert trial1.trial_info.file == trial_info_dict["file"]
    assert trial1.trial_info.channels == trial_info_dict["channels"]
    assert trial1.trial_info.name == trial_info_dict["name"]
    assert trial1.trial_info.subject_id == trial_info_dict["subject_id"]
    assert trial1.trial_info.path_save_figures == trial_info_dict["path_save_figures"]
    assert trial1.trial_info.path_save_trial == trial_info_dict["path_save_trial"]


@pytest.mark.parametrize("channel", ["Flex", "Ext", "Angle", "Triangle", "Keyboard"])
def test_trial_init_channels_present(trial_default, channel):
    info = trial.TrialInfo(file=trial_default)
    trial1 = trial.Trial(info)
    assert channel in trial1.__dir__()


def test_trial_save(payload_dir, trial_default):
    info = trial.TrialInfo(file=trial_default)
    trial1 = trial.Trial(info)
    trial1.save()
    pickled_file = payload_dir / 'data' / 'TRIAL.pkl'
    assert pickled_file.exists()


def test_trial_read(payload_dir, trial_default):
    file = payload_dir /'TRIAL.pkl'
    trial1 = trial.load_trial(file)
    assert type(trial1) == trial.Trial
    assert int(np.mean(trial1.Angle.values) * 10e10) == 187862485065
    assert "Flex" in trial1.__dir__()
