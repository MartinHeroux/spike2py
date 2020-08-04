import os
import pytest
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


