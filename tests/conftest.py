from pathlib import Path
import random

import pytest
import numpy as np
import scipy.io as sio

from spike2py import channels
from spike2py import signal_processing


ACTION_POTENTIALS = [[random.random() for i in range(62)] for _ in range(3)]
PAYLOADS_DIR = Path(__file__).parent / 'payloads'
EVENT = {'name': 'stimulator',
         'data_dict': {'times': np.array([7.654, 7.882]),
                       'ch_type': 'event',
                       }
         }
KEYBOARD = {'name': 'keyboard',
            'data_dict': {'codes': ['t', 'a', '5'],
                          'times': np.array([1.34, 100.334]),
                          'ch_type': 'keyboard',
                          }
            }
WAVEFORM = {'name': 'biceps',
            'data_dict': {'times': np.arange(0, 2, 0.25),
                          'units': 'Volts',
                          'values': np.array([32, 23, 65, 67,
                                              46, 91, 29, 44]) / 1000,
                          'sampling_frequency': 2048,
                          'ch_type': 'waveform',
                          }
            }
WAVEMARK = {'name': 'MG',
            'data_dict': {'units': 'Volts',
                          'times': np.array([7.432, 7.765, 7.915]),
                          'sampling_frequency': 10240,
                          'action_potentials': ACTION_POTENTIALS,
                          'ch_type': 'wavemark',
                          }
            }


@pytest.fixture()
def payload_dir():
    return PAYLOADS_DIR


@pytest.fixture()
def data_setup():
    files = {'biomech': PAYLOADS_DIR / 'biomech0deg.mat',
             'motor_unit': PAYLOADS_DIR / 'motor_units.mat',
             'physiology':  PAYLOADS_DIR / 'physiology.mat',
             }
    mat_datasets = {key: sio.loadmat(value) for key, value in files.items()}
    return {'mat_datasets': mat_datasets,
            'mat_waveform': mat_datasets['biomech']['k_angle'],
            'mat_events': mat_datasets['biomech']['Trig'],
            'mat_keyboard': mat_datasets['physiology']['Keyboard'],
            'mat_keyboard_empty': mat_datasets['biomech']['Keyboard'],
            'mat_wavemark': mat_datasets['motor_unit']['MU1'],
            }


@pytest.fixture()
def channels_init():
    return {'event': EVENT,
            'keyboard': KEYBOARD,
            'waveform': WAVEFORM,
            'wavemark': WAVEMARK,
            }


@pytest.fixture()
def channel_instances():
    return {'event': channels.Event(EVENT),
            'keyboard': channels.Keyboard(KEYBOARD),
            'waveform': channels.Waveform(WAVEFORM),
            'wavemark': channels.Wavemark(WAVEMARK),
            }


@pytest.fixture()
def channels_mock():

    event = {'details': channels.Details(name='stimulator'),
             'times': np.array([7.654, 7.882]),
             'ch_type': 'keyboard',
             '__repr__': 'Event channel',
             }
    keyboard = {'details': channels.Details(name='keyboard'),
                'codes': ['t', 'a', '5'],
                'times': np.array([1.34, 100.334]),
                'ch_type': 'keyboard',
                '__repr__': 'Keyboard channel',
                }
    waveform = {'details': channels.Details(name='biceps',
                                            units='Volts',
                                            sampling_frequency=2048),
                'times': np.arange(0, 2, 0.25),
                'values': np.array([32, 23, 65, 67, 46, 91, 29, 44]) / 1000,
                'ch_type': 'waveform',
                '__repr__': 'Waveform channel',
                }
    wavemark = {'details': channels.Details(name='MG',
                                            units='Volts',
                                            sampling_frequency=10240),
                'times': np.array([7.432, 7.765, 7.915]),
                'action_potentials': ACTION_POTENTIALS,
                'ch_type': 'wavemark',
                'instantaneous_firing_frequency': np.array([3.003003003003009,
                                                            2.07039337474120]),
                '__repr__': 'Wavemark channel',
                }
    return {'event': event,
            'keyboard': keyboard,
            'waveform': waveform,
            'wavemark': wavemark,
            }


@pytest.fixture()
def mixin_methods():
    return ['_setattr', 'remove_mean', 'remove_value', 'lowpass', 'highpass',
            'bandpass', 'bandstop', '_filt', 'calibrate', 'norm_percentage',
            'norm_proportion', 'norm_percent_value', 'interp_new_times',
            'interp_new_fs', '_interp', 'rect', 'linear_detrend',
            ]


def _generate_mixin_values():
    random.seed(42)
    line = np.linspace(0, 5, 10000)
    noise = np.array([random.random() for i in range(10000)])
    return line + noise


@pytest.fixture()
def mixin_values():
    return _generate_mixin_values()


@pytest.fixture()
def mixin():
    mixin = signal_processing.SignalProcessing()
    mixin.values = _generate_mixin_values()
    mixin.details = channels.Details(name='mix_master',
                                     units='mic',
                                     sampling_frequency=1024)
    return mixin
