import os
import pytest
import numpy as np


from spike2py import read


PAYLOADS_DIR = ('tests', 'payloads')


def test_read_smoke_test():
    file = os.path.join(*PAYLOADS_DIR, 'tremor_kinetic.mat')
    data = read.read(file)
    actual = list(data.keys())
    assert actual == ['Flex', 'Ext', 'Angle', 'triangle', 'Keyboard']


def test_read_with_channels_smoke_test():
    file = os.path.join(*PAYLOADS_DIR, 'tremor_kinetic.mat')
    channels = ['Flex', 'Ext', 'Angle']
    data = read.read(file, channels)
    actual = list(data.keys())
    assert actual == ['Flex', 'Ext', 'Angle']


def test_exit_code_no_smr_file():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read.read('file.smr')
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_message_no_smr_file(capfd):
    with pytest.raises(SystemExit):
        read.read('file.smr')
        actual = capfd.readouterr()[0].strip()
        expected = ('Processing .smr files is currently not supported.\n '
                    'In Spike2 export the data to .mat and start over.')
        assert actual == expected


def test_parse_mat_events(data_setup):
    actual = read._parse_mat_events(data_setup['mat_events'])['times']
    actual_int = [int(val*100000) for val in actual]
    assert actual_int == [8189053, 8189254, 8189452, 8189653, 8189854]


def test_parse_mat_keyboard_codes(data_setup):
    actual = read._parse_mat_keyboard(data_setup['mat_keyboard'])
    assert actual['codes'] == ['J', '9', '.', '5', 'S']


def test_parse_mat_keyboard_times(data_setup):
    actual = read._parse_mat_keyboard(data_setup['mat_keyboard'])['times']
    actual_int = [int(val * 100000) for val in actual]
    assert actual_int == [1331245, 1549645, 1634445, 1696845, 11522445]


def test_parse_mat_keyboard_empty(data_setup):
    actual = read._parse_mat_keyboard(data_setup['mat_keyboard_empty'])['times']
    assert len(actual) == 0


def test_parse_mat_waveform_len_times(data_setup):
    actual = read._parse_mat_waveform(data_setup['mat_waveform'])['times']
    assert len(actual) == 22493


def test_parse_mat_waveform_len_values(data_setup):
    actual = read._parse_mat_waveform(data_setup['mat_waveform'])['values']
    assert len(actual) == 22493


def test_parse_mat_waveform_mean_values(data_setup):
    actual = read._parse_mat_waveform(data_setup['mat_waveform'])['values']
    actual_int = int(np.mean(actual) * 100000)
    assert actual_int == 3472608


def test_parse_mat_waveform_units(data_setup):
    actual = read._parse_mat_waveform(data_setup['mat_waveform'])['units']
    assert actual == 'deg'


def test_parse_mat_waveform_sampling_frequency(data_setup):
    actual = read._parse_mat_waveform(data_setup['mat_waveform'])['sampling_frequency']
    assert actual == 200


def test_parse_mat_wavemark_units(data_setup):
    actual = read._parse_mat_wavemark(data_setup['mat_wavemark'])['units']
    assert actual == ' Volt'


def test_parse_mat_wavemark_len_discharge_times(data_setup):
    actual = read._parse_mat_wavemark(data_setup['mat_wavemark'])['times']
    assert len(actual) == 62


def test_parse_mat_wavemark_discharge_times(data_setup):
    actual = read._parse_mat_wavemark(data_setup['mat_wavemark'])['times']
    actual_int = [int(val * 100000) for val in actual]
    actual_int_sample = actual_int[:3] + actual_int[-3:]
    assert actual_int_sample == [399001, 405992, 411668, 1173429, 1184660, 1195989]


def test_parse_mat_wavemark_sampling_frequency(data_setup):
    actual = read._parse_mat_wavemark(data_setup['mat_wavemark'])['sampling_frequency']
    assert actual == 25000


def test_parse_mat_wavemark_action_potentials(data_setup):
    actual = read._parse_mat_wavemark(data_setup['mat_wavemark'])['action_potentials']
    assert actual.shape == (62, 256)
