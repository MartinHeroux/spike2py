import os
import sys
import textwrap

import scipy.io as sio


def read(file, channels='All'):
    """Interface to read data files

    Parameters
    ----------
    file: str
        Absolute path to data file. Only .mat files are currently supported.
    channels: list
        List of channel names, as they appeared in the original .smr file.
        Example: ['biceps', 'triceps', 'torque']
        If not included, all channels will be processed.

    Returns
    -------
    dict
        Data from a trial where `keys` are channel names and `values`
        are deeply nested numpy.ndarray
    """

    file_extension = os.path.splitext(file)[-1]
    if file_extension == '.smr':
        print('Processing .smr files is currently not supported.\n'
              'In Spike2 export the data to .mat and start over.')
        sys.exit(1)
    if file_extension != '.mat':
        print(f'Processing {file_extension} files is currently not supported.\n'
              'In Spike2 export the data to .mat and start over.')
        sys.exit(1)
    data = _read_mat(file, channels)
    data = _parse_mat_data(data)
    return data


def _read_mat(mat_file, channels):
    """Read Spike2 data exported to a Matlab .mat file

    Parameters
    ----------
    mat_file: str
        Absolute path to .mat file
    channels: list, None
        List of channel names, as they appeared in the original .smr file,
        or None, in which case all channels are processed.

    Returns
    -------
    dict
        Requested channels with channel names as `keys` and deeply nested
        arrays containing channel data as `values`.
    """
    data = sio.loadmat(mat_file)
    if channels == 'All':
        channels = [data_key for data_key in data.keys() if not data_key.startswith('__')]
    return {key: value for (key, value) in data.items() if key in channels}


def _parse_mat_data(mat_data):
    """Parse deeply nested array that contain channel data

    Parameters
    ----------
    mat_data: array
        Deeply nested array containing channel data and metadata.

    Returns
    -------
    dict
        Channel data and metadata.
        The `keys` and `values` will differ for the different channel types.
        See the `_parse_mat_<channel type>` helper functions for details.
    """
    signal_type_parser = {5: _parse_mat_events,
                          6: _parse_mat_keyboard,
                          10: _parse_mat_waveform,
                          14: _parse_mat_wavemark}
    parsed_data = dict()
    for key, value in mat_data.items():
        parsed_data[key] = signal_type_parser[len(value.dtype)](value)
    return parsed_data


def _parse_mat_waveform(mat_waveform):
    """Parse waveform channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_waveform: array
         Deeply nested array containing waveform channel data and metadata.

    Returns
    -------
    dict
        Data from waveform channel.
    """
    units_flattened = _flatten(mat_waveform['units'])
    units = None
    if len(units_flattened) != 0:
        units = units_flattened[0]
    return {'times': _flatten(mat_waveform['times']),
            'units': units,
            'values': _flatten(mat_waveform['values']),
            'sampling_frequency': int(1 / _flatten(mat_waveform['interval'])),
            }


def _parse_mat_keyboard(mat_keyboard):
    """Parse keyboard channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_keyboard: array
         Deeply nested array containing keyboard channel data and metadata.

    Returns
    -------
    dict
        Data from keyboard channel.
    """

    keyboard_codes = _flatten(mat_keyboard['codes'])
    characters = None
    if len(keyboard_codes) != 0:
        characters = _keyboard_codes_to_characters(keyboard_codes)
    return {'codes': characters,
            'times': _flatten(mat_keyboard['times']),
            }


def _keyboard_codes_to_characters(keyboard_codes):
    """Helper function that converts encoded character(s) into str

    Parameters
    ----------
    keyboard_codes: list
         List of int values, where each keyboard entry is encoded by four int values.
         Example of single keyboard entry: [42, 0, 0, 0]
         Example of multiple keyboard entries: [42, 0, 0, 0, 57, 0, 0, 0, 73, 0, 0, 0]

    Returns
    -------
    list
        List of str values, corresponding to each of the keyboard entries.
    """

    hex_keyboard_codes = textwrap.fill(keyboard_codes.tostring().hex(), 8).split('\n')
    return [bytearray.fromhex(hex_code[0:8][:2]).decode()
            for hex_code in hex_keyboard_codes]


def _parse_mat_events(mat_events):
    """Parse event channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_waveform: array
         Deeply nested array containing waveform channel data and metadata.

    Returns
    -------
    dict
        Data from waveform channel.
    """

    return {'times': _flatten(mat_events['times'])}


def _parse_mat_wavemark(mat_wavemark):
    """Parse wavemark channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_wavemark: array
         Deeply nested array containing wavemark channel data and metadata.

    Returns
    -------
    dict
        Data from wavemark channel.
    """

    units_flattened = _flatten(mat_wavemark['units'])
    units = None
    times = None
    sampling_frequency = None
    template_length = None
    action_potentials = None
    if len(units_flattened) != 0:
        units = units_flattened[0]
        times = mat_wavemark['times'][0][0].flatten()
        sampling_frequency = int(1 / mat_wavemark['interval'][0][0].flatten())
        template_length = int(_flatten(mat_wavemark['length']))

        concatenated_wavemarks = _flatten(mat_wavemark['values'])
        number_of_wavemarks = int(len(concatenated_wavemarks) / template_length)
        action_potentials = concatenated_wavemarks.reshape(template_length, number_of_wavemarks)
    return {'units': units,
            'template_length': template_length,
            'times': times,
            'sampling_frequency': sampling_frequency,
            'action_potentials': action_potentials,
            }


def _flatten(array):
    return array[0][0].flatten()
