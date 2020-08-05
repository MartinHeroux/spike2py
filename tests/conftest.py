import os
import random

import pytest
import numpy as np
import scipy.io as sio

PAYLOADS_DIR = ('tests', 'payloads')


@pytest.fixture()
def data_setup():
    files = {'biomech': os.path.join(*PAYLOADS_DIR, 'biomech0deg.mat'),
             'motor_unit': os.path.join(*PAYLOADS_DIR, 'motor_units.mat'),
             'physiology': os.path.join(*PAYLOADS_DIR, 'physiology.mat')
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
    event = {'name': 'stimulator',
             'trial_name': 'fatigue2',
             'times': np.array([7.654, 7.882]),
             }
    keyboard = {'name': 'keyboard',
                'trial_name': 'stim20_1',
                'times': np.array([1.34, 100.334]),
                'codes': ['t', 'a', '5'],
                }
    waveform = {'name': 'biceps',
                'trial_name': 'max_100',
                'times': np.arange(0, 2, 0.25),
                'units': 'Volts',
                'values': np.array([32, 23, 65, 67, 46, 91, 29, 44]) / 1000,
                'sampling_frequency': 2048,
                }
    wavemark = {'name': 'MG',
                'trial_name': 'post_50_1',
                'times': np.array([7.432, 7.765, 7.915]),
                'units': 'Volts',
                'template_length': 62,
                'sampling_frequency': 10240,
                'action_potentials': [[random.random() for i in range(62)],
                                      [random.random() for i in range(62)],
                                      [random.random() for i in range(62)]],
                }
    return {'event': event,
            'keyboard': keyboard,
            'waveform': waveform,
            'wavemark': wavemark,
            }
