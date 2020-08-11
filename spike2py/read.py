from pathlib import Path
import sys
import textwrap

import scipy.io as sio


CHANNEL_DATA_LENGTH = {'event': 5,
                       'keyboard': 6,
                       'waveform': 10,
                       'wavemark': 14,
                       }


def read(file, channels=None):
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

    file_extension = Path(file).suffix
    if file_extension == '.smr':
        print('Processing .smr files is currently not supported.\n'
              'In Spike2 export the data to .mat and start over.')
        sys.exit(1)
    if file_extension != '.mat':
        print(f'Processing {file_extension} files is currently not supported.'
              f'\nIn Spike2 export the data to .mat and start over.')
        sys.exit(1)
    return _parse_mat_data(_read_mat(file, channels))


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
    if channels is None:
        channels = [data_key
                    for data_key in data.keys()
                    if not data_key.startswith('__')]
    return {key: value
            for (key, value) in data.items()
            if key in channels}


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
    parser_lookup = {CHANNEL_DATA_LENGTH['event']: _parse_mat_events,
                     CHANNEL_DATA_LENGTH['keyboard']: _parse_mat_keyboard,
                     CHANNEL_DATA_LENGTH['waveform']: _parse_mat_waveform,
                     CHANNEL_DATA_LENGTH['wavemark']: _parse_mat_wavemark}
    parsed_data = dict()
    for key, value in mat_data.items():
        parsed_data[key] = parser_lookup[len(value.dtype)](value)
    return parsed_data


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

    return {'times': _flatten_array(mat_events['times']),
            'ch_type': 'event',
            }


def _flatten_array(array):
    return array[0][0].flatten()


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

    keyboard_codes = _flatten_array(mat_keyboard['codes'])
    characters = None
    if len(keyboard_codes) != 0:
        characters = _keyboard_codes_to_characters(keyboard_codes)
    return {'codes': characters,
            'times': _flatten_array(mat_keyboard['times']),
            'ch_type': 'keyboard',
            }


def _keyboard_codes_to_characters(keyboard_codes):
    """Helper function that converts encoded character(s) into list of str

    Parameters
    ----------
    keyboard_codes: list
         List of int values, where each keyboard entry is encoded by four int
         values.
         e.g. single keyboard entry: [42, 0, 0, 0]
         e.g. multi keyboard entries: [42, 0, 0, 0, 57, 0, 0, 0, 73, 0, 0, 0]

    Returns
    -------
    list
        List of str values, corresponding to each of the keyboard entries.
    """

    hex_keyboard_codes = textwrap.fill(
        keyboard_codes.tostring().hex(), 8).split('\n')
    return [bytearray.fromhex(hex_code[0:8][:2]).decode()
            for hex_code in hex_keyboard_codes]


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
    units_flattened = _flatten_array(mat_waveform['units'])
    units = None
    if units_flattened.size > 0:
        units = units_flattened[0]
    times = _flatten_array(mat_waveform['times'])
    values = _flatten_array(mat_waveform['values'])
    shortest_array = min(len(times), len(values))
    return {'times': times[:shortest_array],
            'units': units,
            'values': values[:shortest_array],
            'sampling_frequency':
                int(1 / _flatten_array(mat_waveform['interval'])),
            'ch_type': 'waveform',
            }


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

    units = None
    times = None
    sampling_frequency = None
    action_potentials = None

    units_flattened = _flatten_array(mat_wavemark['units'])

    if units_flattened.size > 0:
        units = units_flattened[0]
        times = mat_wavemark['times'][0][0].flatten()
        sampling_frequency = int(1 / mat_wavemark['interval'][0][0].flatten())
        action_potentials = _extract_wavemarks(mat_wavemark)
    return {'units': units,
            'times': times,
            'sampling_frequency': sampling_frequency,
            'action_potentials': action_potentials,
            'ch_type': 'wavemark',
            }


def _extract_wavemarks(mat_wavemark):
    """Helper function to flatten, extract and group wavemark values"""
    template_length = int(_flatten_array(mat_wavemark['length']))
    concatenated_wavemarks = _flatten_array(mat_wavemark['values'])
    number_of_wavemarks = int(len(concatenated_wavemarks) / template_length)
    return concatenated_wavemarks.reshape(template_length, number_of_wavemarks)
