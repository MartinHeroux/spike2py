import os
from pathlib import Path
import random

import pytest
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

from spike2py import channels, sig_proc


ACTION_POTENTIALS = [[random.random() for i in range(62)] for _ in range(3)]
PAYLOADS_DIR = Path(__file__).parent / "payloads"
PATH = Path(".")
EVENT = {
    "name": "stimulator",
    "data_dict": {
        "times": np.array([7.654, 7.882]),
        "ch_type": "event",
        "path_save_figures": Path("."),
        "trial_name": "strong_you_are",
        "subject_id": "Yoda",
    },
}
KEYBOARD = {
    "name": "keyboard",
    "data_dict": {
        "codes": ["t", "a", "5"],
        "times": np.array([1.34, 100.334]),
        "ch_type": "keyboard",
        "path_save_figures": Path("."),
        "trial_name": "strong_you_are",
        "subject_id": "Yoda",
    },
}
WAVEFORM = {
    "name": "biceps",
    "data_dict": {
        "times": np.arange(0, 2, 0.25),
        "units": "Volts",
        "values": np.array([32, 23, 65, 67, 46, 91, 29, 44]) / 1000,
        "sampling_frequency": 2048,
        "ch_type": "waveform",
        "path_save_figures": Path("."),
        "trial_name": "strong_you_are",
        "subject_id": "Yoda",
    },
}
WAVEMARK = {
    "name": "MG",
    "data_dict": {
        "units": "Volts",
        "times": np.array([7.432, 7.765, 7.915]),
        "sampling_frequency": 10240,
        "action_potentials": ACTION_POTENTIALS,
        "ch_type": "wavemark",
        "path_save_figures": Path("."),
        "trial_name": "strong_you_are",
        "subject_id": "Yoda",
    },
}


PATH_TO_MAT_FILES = [
    PAYLOADS_DIR / "physiology.mat",
    PAYLOADS_DIR / "biomech0deg.mat",
    PAYLOADS_DIR / "motor_units.mat",
]


@pytest.fixture()
def payload_dir():
    return PAYLOADS_DIR


@pytest.fixture()
def data_setup():
    files = {
        "physiology": PATH_TO_MAT_FILES[0],
        "biomech": PATH_TO_MAT_FILES[1],
        "motor_unit": PATH_TO_MAT_FILES[2],
    }
    mat_datasets = {key: sio.loadmat(value) for key, value in files.items()}
    return {
        "mat_datasets": mat_datasets,
        "mat_waveform": mat_datasets["biomech"]["k_angle"],
        "mat_events": mat_datasets["biomech"]["Trig"],
        "mat_keyboard": mat_datasets["physiology"]["Keyboard"],
        "mat_keyboard_empty": mat_datasets["biomech"]["Keyboard"],
        "mat_wavemark": mat_datasets["motor_unit"]["MU1"],
    }


@pytest.fixture()
def channels_init():
    return {
        "event": EVENT,
        "keyboard": KEYBOARD,
        "waveform": WAVEFORM,
        "wavemark": WAVEMARK,
    }


@pytest.fixture()
def channels_mock():
    event = {
        "info": channels.ChannelInfo(
            name="stimulator",
            path_save_figures=Path("."),
            trial_name="strong_you_are",
            subject_id="Yoda",
        ),
        "times": np.array([7.654, 7.882]),
        "ch_type": "keyboard",
        "__repr__": "Event channel",
    }
    keyboard = {
        "info": channels.ChannelInfo(
            name="keyboard",
            path_save_figures=Path("."),
            trial_name="strong_you_are",
            subject_id="Yoda",
        ),
        "codes": ["t", "a", "5"],
        "times": np.array([1.34, 100.334]),
        "ch_type": "keyboard",
        "__repr__": "Keyboard channel",
    }
    waveform = {
        "info": channels.ChannelInfo(
            name="biceps",
            units="Volts",
            sampling_frequency=2048,
            path_save_figures=Path("."),
            trial_name="strong_you_are",
            subject_id="Yoda",
        ),
        "times": np.arange(0, 2, 0.25),
        "values": np.array([32, 23, 65, 67, 46, 91, 29, 44]) / 1000,
        "ch_type": "waveform",
        "__repr__": "Waveform channel",
    }
    wavemark = {
        "info": channels.ChannelInfo(
            name="MG",
            units="Volts",
            sampling_frequency=10240,
            path_save_figures=Path("."),
            trial_name="strong_you_are",
            subject_id="Yoda",
        ),
        "times": np.array([7.432, 7.765, 7.915]),
        "action_potentials": ACTION_POTENTIALS,
        "ch_type": "wavemark",
        "instantaneous_firing_frequency": np.array([3.003003, 6.6666667]),
        "__repr__": "Wavemark channel",
    }
    return {
        "event": event,
        "keyboard": keyboard,
        "waveform": waveform,
        "wavemark": wavemark,
    }


@pytest.fixture()
def mixin_methods():
    return [
        "_setattr",
        "remove_mean",
        "remove_value",
        "_float_to_string_with_underscore",
        "lowpass",
        "highpass",
        "bandpass",
        "bandstop",
        "_filt",
        "_check_valid_cutoff",
        "_check_valid_filter_order",
        "_cutoff_to_string",
        "calibrate",
        "norm_percentage",
        "norm_proportion",
        "norm_percent_value",
        "interp_new_times",
        "_check_new_times",
        "interp_new_fs",
        "_interp",
        "rect",
        "linear_detrend",
    ]


def _generate_mixin_values():
    random.seed(42)
    line = np.linspace(0, 5, 10000)
    noise = np.array([random.random() for _ in range(10000)])
    values = line + noise
    times = np.linspace(0, 100, 10000)
    return values, times


@pytest.fixture()
def mixin():
    mixin = sig_proc.SignalProcessing()
    mixin.values, mixin.times = _generate_mixin_values()
    mixin.info = channels.ChannelInfo(
        name="mix_master", units="mic", sampling_frequency=1000
    )
    return mixin


@pytest.fixture()
def negative_value_mixin():
    mixin = sig_proc.SignalProcessing()
    values, _ = _generate_mixin_values()
    mixin.values = -1 * values
    mixin.info = channels.ChannelInfo(
        name="mix_master", units="mic", sampling_frequency=1000
    )
    return mixin


@pytest.fixture()
def trial_default():
    _remove_files_in_folder_in_payloads_dir(folder="figures")
    _remove_files_in_folder_in_payloads_dir(folder="data")
    yield PAYLOADS_DIR / "tremor_kinetic.mat"
    _remove_files_in_folder_in_payloads_dir(folder="figures")
    _remove_files_in_folder_in_payloads_dir(folder="data")


def _remove_files_in_folder_in_payloads_dir(folder):
    path = PAYLOADS_DIR / folder
    if path.exists():
        for file in path.glob("*"):
            file.unlink()
        path.rmdir()


@pytest.fixture()
def trial_info_dict():
    yield {
        "file": PATH_TO_MAT_FILES[1],
        "channels": ["k_angle", "k_torque", "prox_EMG"],
        "name": "TREMOR",
        "subject_id": "ET01",
        "path_save_figures": PAYLOADS_DIR / "trial_figures",
        "path_save_trial": PAYLOADS_DIR / "study_data",
    }
    _remove_files_in_folder_in_payloads_dir(folder="trial_figures")
    _remove_files_in_folder_in_payloads_dir(folder="study_data")


@pytest.fixture()
def trial_info_dict_channel_error():
    yield {
        "file": PATH_TO_MAT_FILES[1],
        "channels": ["K_angle", "k_torque", "prox_EMG"],
        "name": "TREMOR",
        "subject_id": "ET01",
        "path_save_figures": PAYLOADS_DIR / "trial_figures",
        "path_save_trial": PAYLOADS_DIR / "study_data",
    }
    _remove_files_in_folder_in_payloads_dir(folder="trial_figures")
    _remove_files_in_folder_in_payloads_dir(folder="study_data")


@pytest.fixture()
def physiology_data():
    _remove_files_in_folder_in_payloads_dir(folder="figures")
    _remove_files_in_folder_in_payloads_dir(folder="data")
    plt.close("all")
    yield PAYLOADS_DIR / "physiology.mat"
    plt.close("all")
    _remove_files_in_folder_in_payloads_dir(folder="figures")
    _remove_files_in_folder_in_payloads_dir(folder="data")


@pytest.fixture()
def motor_units_data():
    _remove_files_in_folder_in_payloads_dir(folder="figures")
    _remove_files_in_folder_in_payloads_dir(folder="data")
    plt.close("all")
    yield PAYLOADS_DIR / "motor_units.mat"
    plt.close("all")
    _remove_files_in_folder_in_payloads_dir(folder="figures")
    _remove_files_in_folder_in_payloads_dir(folder="data")


@pytest.fixture()
def tutorial_data_dict():
    tmp = os.getenv("TMP", "/tmp")
    yield {
        "file": Path(tmp) / "motor_units.mat",
        "channels": [
            ("Dia_Smu", "waveform"),
            ("Mu2", "wavemark"),
            ("Flow", "waveform"),
            ("Volume", "waveform"),
            ("Co2", "waveform"),
            ("Mu1", "wavemark"),
        ],
    }
