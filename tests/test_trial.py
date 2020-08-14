import pytest

from spike2py import trial


def test_trial_init_minimal_example(mat_file):
    info = trial.TrialInfo(file=mat_file)
    balance_1 = trial.Trial(info)
    assert balance_1.trial_info.file == mat_file

