import pytest
from pytest import approx

import numpy as np

from spike2py import read


def test_read_smoke_test(payload_dir):
    file = payload_dir / "tremor_kinetic.mat"
    data = read.read(file)
    actual = list(data.keys())
    assert actual == ["Flex", "Ext", "Angle", "triangle", "Keyboard"]


def test_read_with_channels_smoke_test(payload_dir):
    file = payload_dir / "tremor_kinetic.mat"
    channels = ["Flex", "Ext", "Angle"]
    data = read.read(file, channels)
    actual = list(data.keys())
    assert actual == ["Flex", "Ext", "Angle"]


def test_read_missing_mat_file(payload_dir, capsys):
    file = payload_dir / "tremor_kenetic.mat"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        data = read.read(file)
    captured = capsys.readouterr()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert captured.out == (
        (
            (
                "File tremor_kenetic.mat not found. "
                "Please verify path and file name and try again.\n"
            )
        )
    )


def test_exit_code_no_smr_file(payload_dir):
    file = payload_dir / "tremor_kinetic.smr"
    with pytest.raises(
        read.WrongFileType,
        match="Processing .smr files is not supported."
        "\nIn Spike2 export the data to .mat and start over.",
    ):
        data = read.read(file)


def test_parse_mat_events(data_setup):
    actual = read._parse_mat_events(data_setup["mat_events"])["times"]
    assert actual == approx([81.89053, 81.89254, 81.89452, 81.89653, 81.89854])


def test_parse_mat_keyboard_codes(data_setup):
    actual = read._parse_mat_keyboard(data_setup["mat_keyboard"])
    assert actual["codes"] == ["J", "9", ".", "5", "S"]


def test_parse_mat_keyboard_times(data_setup):
    actual = read._parse_mat_keyboard(data_setup["mat_keyboard"])["times"]
    assert actual == approx([13.312455, 15.496455, 16.344455, 16.968455, 115.224455])


def test_parse_mat_keyboard_empty(data_setup):
    actual = read._parse_mat_keyboard(data_setup["mat_keyboard_empty"])["times"]
    assert len(actual) == 0


def test_parse_mat_waveform_len_times(data_setup):
    actual = read._parse_mat_waveform(data_setup["mat_waveform"])["times"]
    assert len(actual) == 22493


def test_parse_mat_waveform_len_values(data_setup):
    actual = read._parse_mat_waveform(data_setup["mat_waveform"])["values"]
    assert len(actual) == 22493


def test_parse_mat_waveform_mean_values(data_setup):
    actual = read._parse_mat_waveform(data_setup["mat_waveform"])["values"]
    assert np.mean(actual) == approx(34.726087101048)


def test_parse_mat_waveform_units(data_setup):
    actual = read._parse_mat_waveform(data_setup["mat_waveform"])["units"]
    assert actual == "deg"


def test_parse_mat_waveform_sampling_frequency(data_setup):
    actual = read._parse_mat_waveform(data_setup["mat_waveform"])["sampling_frequency"]
    assert actual == 200


def test_parse_mat_wavemark_units(data_setup):
    actual = read._parse_mat_wavemark(data_setup["mat_wavemark"])["units"]
    assert actual == " Volt"


def test_parse_mat_wavemark_len_discharge_times(data_setup):
    actual = read._parse_mat_wavemark(data_setup["mat_wavemark"])["times"]
    assert len(actual) == 62


def test_parse_mat_wavemark_discharge_times(data_setup):
    actual = read._parse_mat_wavemark(data_setup["mat_wavemark"])["times"]
    actual_sample = actual[:3] + actual[-3:]
    assert actual_sample == approx([15.7243, 15.90654, 16.07658])


def test_parse_mat_wavemark_sampling_frequency(data_setup):
    actual = read._parse_mat_wavemark(data_setup["mat_wavemark"])["sampling_frequency"]
    assert actual == 25000


def test_parse_mat_wavemark_action_potentials(data_setup):
    actual = read._parse_mat_wavemark(data_setup["mat_wavemark"])["action_potentials"]
    assert actual.shape == (62, 256)
