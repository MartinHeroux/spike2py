import sys
from pathlib import Path
import textwrap
from typing import List, Final

import scipy.io as sio
import numpy as np

from spike2py.types import (
    mat_data,
    parsed_wavemark,
    parsed_waveform,
    parsed_event,
    parsed_textmark,
    parsed_keyboard,
    parsed_spike2py_data,
    parsed_mat_data,
)

CHANNEL_DATA_LENGTH: Final = {
    "event": 5,
    "keyboard": 6,
    "textmark": 8,
    "waveform": 10,
    "wavemark": 14,
}


class WrongFileType(Exception):
    """Custom exception to use when `.mat` file not provided"""

    pass


def read(file: Path, channels: List[str] = None) -> parsed_spike2py_data:
    """Interface to read data files

    Parameters
    ----------
    file
        Absolute path to data file. Only .mat files are currently supported.
    channels
        List of channel names, as they appeared in the original .smr file.
        Example: ['biceps', 'triceps', 'torque']
        If not included, all channels will be processed.

    Raises
    ------
    WrongFileType
        `file` parameter is not a `.mat` file

    Returns
    -------
    dict
        Data from a trial where `keys` are channel names and `values`
        are deeply nested numpy.ndarray
    """

    file_extension = Path(file).suffix
    if file_extension != ".mat":
        raise WrongFileType(
            f"Processing {file_extension} files is not supported."
            "\nIn Spike2 export the data to .mat and start over."
        )
    return _parse_mat_data(_read_mat(file, channels))


def _read_mat(mat_file: Path, channels: List[str]) -> mat_data:
    """Read Spike2 data exported to a Matlab .mat file

    Parameters
    ----------
    mat_file
        Absolute path to .mat file
    channels
        List of channel names, as they appeared in the original .smr file,
        or None, in which case all channels are processed.

    Returns
    -------
    dict
        Requested channels with channel names as `keys` and deeply nested
        arrays containing channel data as `values`.
    """
    try:
        data: dict = sio.loadmat(mat_file)
    except OSError:
        print(
            f"File {mat_file.name} not found. Please verify path and file name and try again."
        )
        sys.exit(1)
    all_channels = [
        data_key for data_key in data.keys() if not data_key.startswith("__")
    ]
    if channels is None:
        channels = all_channels
    else:
        _verify_channels_exists(channels, all_channels, mat_file)
    return {key: value for (key, value) in data.items() if key in channels}


def _verify_channels_exists(channels, all_channels, mat_file):
    for channel in channels:
        if channel not in all_channels:
            print(
                f"Channel {channel} does not exist in {mat_file.name}. \n"
                f"Available channels include:\n"
            )
            for ch in all_channels:
                print(ch)
            sys.exit(1)


def _parse_mat_data(mat_data: mat_data) -> parsed_mat_data:
    """Parse deeply nested array that contain channel data

    Parameters
    ----------
    mat_data
        Deeply nested array containing channel data and metadata.

    Returns
    -------
    dict
        Channel data and metadata.
        The `keys` and `values` will differ for the different channel types.
        See the `_parse_mat_<channel type>` helper functions for details.
    """
    parser_lookup = {
        CHANNEL_DATA_LENGTH["event"]: _parse_mat_events,
        CHANNEL_DATA_LENGTH["textmark"]: _parse_mat_textmark,
        CHANNEL_DATA_LENGTH["keyboard"]: _parse_mat_keyboard,
        CHANNEL_DATA_LENGTH["waveform"]: _parse_mat_waveform,
        CHANNEL_DATA_LENGTH["wavemark"]: _parse_mat_wavemark,
    }
    parsed_data = dict()
    for key, value in mat_data.items():
        parsed_data[key] = parser_lookup[len(value.dtype)](value)
    return parsed_data


def _parse_mat_events(mat_events: np.ndarray) -> parsed_event:
    """Parse event channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_events
         Deeply nested array containing waveform channel data and metadata.

    Returns
    -------
    dict
        Data from event channel.
    """

    return {
        "times": _flatten_array(mat_events["times"]),
        "ch_type": "event",
    }


def _flatten_array(array):
    return array[0][0].flatten()


def _parse_mat_keyboard(mat_keyboard: np.ndarray) -> parsed_keyboard:
    """Parse keyboard channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_keyboard
         Deeply nested array containing keyboard channel data and metadata.

    Returns
    -------
    dict
        Data from keyboard channel.
    """

    keyboard_codes = _flatten_array(mat_keyboard["codes"])
    characters = None
    if len(keyboard_codes) != 0:
        characters = _keyboard_codes_to_characters(keyboard_codes)
    return {
        "codes": characters,
        "times": _flatten_array(mat_keyboard["times"]),
        "ch_type": "keyboard",
    }


def _parse_mat_textmark(mat_textmark: np.ndarray) -> parsed_textmark:
    """Parse textmark ('Memory') channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_textmark
         Deeply nested array containing keyboard channel data and metadata.

    Returns
    -------
    dict
        Data from textmark channel.
    """

    codes = list(mat_textmark["text"][0][0])
    return {
        "codes": codes,
        "times": _flatten_array(mat_textmark["times"]),
        "ch_type": "textmark",
    }


def _keyboard_codes_to_characters(keyboard_codes: List[int]) -> List[str]:
    """Helper function that converts encoded character(s) into list of str

    Parameters
    ----------
    keyboard_codes
         List of int values, where each keyboard entry is encoded by four int
         values.
         e.g. single keyboard entry: [42, 0, 0, 0]
         e.g. multi keyboard entries: [42, 0, 0, 0, 57, 0, 0, 0, 73, 0, 0, 0]

    Returns
    -------
    list
        List of str values, corresponding to each of the keyboard entries.
    """

    hex_keyboard_codes = textwrap.fill(keyboard_codes.tobytes().hex(), 8).split("\n")
    return [
        bytearray.fromhex(hex_code[0:8][:2]).decode() for hex_code in hex_keyboard_codes
    ]


def _parse_mat_waveform(mat_waveform: np.ndarray) -> parsed_waveform:
    """Parse waveform channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_waveform
         Deeply nested array containing waveform channel data and metadata.

    Returns
    -------
    dict
        Data from waveform channel.
    """
    units_flattened = _flatten_array(mat_waveform["units"])
    units = None
    if units_flattened.size > 0:
        units = units_flattened[0]
    times = _flatten_array(mat_waveform["times"])
    values = _flatten_array(mat_waveform["values"])
    shortest_array = min(len(times), len(values))
    return {
        "times": times[:shortest_array],
        "units": units,
        "values": values[:shortest_array],
        "sampling_frequency": int(1 / _flatten_array(mat_waveform["interval"])[0]),
        "ch_type": "waveform",
    }


def _parse_mat_wavemark(mat_wavemark: np.ndarray) -> parsed_wavemark:
    """Parse wavemark channel data as exported by Spike2 to .mat

    Parameters
    ----------
    mat_wavemark
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

    units_flattened = _flatten_array(mat_wavemark["units"])

    if units_flattened.size > 0:
        units = units_flattened[0]
        times = mat_wavemark["times"][0][0].flatten()
        sampling_frequency = int(1 / mat_wavemark["interval"][0][0].flatten()[0])
        action_potentials = _extract_wavemarks(mat_wavemark)
    return {
        "units": units,
        "times": times,
        "sampling_frequency": sampling_frequency,
        "action_potentials": action_potentials,
        "ch_type": "wavemark",
    }


def _extract_wavemarks(mat_wavemark: np.ndarray) -> List[List[int]]:
    """Helper function to flatten, extract and group wavemark values"""
    template_length = int(_flatten_array(mat_wavemark["length"])[0])
    concatenated_wavemarks = _flatten_array(mat_wavemark["values"])
    number_of_wavemarks = int(len(concatenated_wavemarks) / template_length)
    return concatenated_wavemarks.reshape(template_length, number_of_wavemarks)
