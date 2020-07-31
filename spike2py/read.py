import sys
import textwrap
import scipy.io as sio


def read(file, channels=None):
    """User interface to read data files.

    Parameters
    ----------
    file: str
        Absolute path to data file. Only .mat files are currently supported.
    channels: list
        List of channel names, as they appeared in the original .smr file.
        Example: ['biceps', 'triceps', 'torque']

    Returns
    -------
    dict
        Data from a trial where `keys` are channel names and `values`
        are deeply nested numpy.ndarray
    """

    data = dict()
    file_extension = file.split('.')[-1]
    if file_extension == 'mat':
        data = _read_mat(file, channels)
        data = _parse_mat_data(data)
    elif file_extension == 'smr':
        print('Processing .smr files is currently not supported.\n'
              'In Spike2 export the data to .mat and start over.')
        sys.exit(1)
    return data


def _read_mat(mat_file, channels):
    data = sio.loadmat(mat_file)
    if not channels:
        channels = [data_key for data_key in data.keys() if data_key[:2] != '__']
    return {key: value for (key, value) in data.items() if key in channels}


def _parse_mat_data(mat_data):
    signal_type_parser = {5: _parse_mat_events,
                          6: _parse_mat_keyboard,
                          10: _parse_mat_waveform,
                          14: _parse_mat_wavemark}
    parsed_data = dict()
    for key, value in mat_data.items():
        parsed_data[key] = signal_type_parser[len(value.dtype)](value)
    return parsed_data


def _parse_mat_waveform(mat_waveform):
    return {'times': mat_waveform['times'][0][0].flatten(),
            'units': mat_waveform['units'][0][0].flatten()[0],
            'values': mat_waveform['values'][0][0].flatten(),
            'sampling_frequency': int(1 / mat_waveform['interval'][0][0].flatten()),
            }


def _parse_mat_keyboard(mat_keyboard):
    keyboard_codes = mat_keyboard['codes'][0][0].flatten()
    characters = None
    if len(keyboard_codes) != 0:
        characters = _keyboard_codes_to_characters(keyboard_codes)
    return {'codes': characters,
            'times': mat_keyboard['times'][0][0].flatten(),
            }


def _keyboard_codes_to_characters(keyboard_codes):
    hex_keyboard_codes = textwrap.fill(keyboard_codes.tostring().hex(), 8).split('\n')
    return [bytearray.fromhex(hex_code[0:8][:2]).decode()
            for hex_code in hex_keyboard_codes]


def _parse_mat_events(mat_events):
    return {'times': mat_events['times'][0][0].flatten()}


def _parse_mat_wavemark(mat_wavemark):
    concatenated_wavemarks = mat_wavemark['values'][0][0].flatten()
    wavemark_template_length = int(mat_wavemark['length'][0][0].flatten())
    number_of_wavemarks = int(len(concatenated_wavemarks) / wavemark_template_length)
    split_wavemarks = concatenated_wavemarks.reshape(wavemark_template_length, number_of_wavemarks)

    return {'units': mat_wavemark['units'][0][0].flatten()[0],
            'template_length': wavemark_template_length,
            'discharge_times': mat_wavemark['times'][0][0].flatten(),
            'sampling_frequency': int(1 / mat_wavemark['interval'][0][0].flatten()),
            'action_potentials': split_wavemarks,
            }
