from pathlib import Path
import random

import pytest
import numpy as np
import scipy.io as sio

from spike2py import channels


PAYLOADS_DIR = Path.cwd() / 'tests' / 'payloads'


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
    event_details = channels.channel_details(
        name='stimulator', trial='fatigue2')
    event = {'details': event_details,
             'times': np.array([7.654, 7.882]),
             }
    keyboard_details = channels.channel_details(
        name='keyboard', trial='stim20_1')
    keyboard = {'details': keyboard_details,
                'times': np.array([1.34, 100.334]),
                'codes': ['t', 'a', '5'],
                }
    waveform_details = channels.channel_details(
        name='biceps', trial='max100', units='Volts', sampling_frequency=2048)
    waveform = {'details': waveform_details,
                'times': np.arange(0, 2, 0.25),
                'values': np.array([32, 23, 65, 67, 46, 91, 29, 44]) / 1000,
                }
    wavemark_details = channels.channel_details(
        name='MG', trial='post_50_1', units='Volts', sampling_frequency=10240)
    wavemark = {'details': wavemark_details,
                'times': np.array([7.432, 7.765, 7.915]),
                'action_potentials': [[random.random() for i in range(62)],
                                      [random.random() for i in range(62)],
                                      [random.random() for i in range(62)]],
                }
    return {'event': event,
            'keyboard': keyboard,
            'waveform': waveform,
            'wavemark': wavemark,
            }
