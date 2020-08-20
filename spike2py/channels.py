from pathlib import Path
from typing import NamedTuple, Literal

import numpy as np

import spike2py.plot as plot
import spike2py.sig_proc as sig_proc

from spike2py.types import (
    parsed_wavemark,
    parsed_waveform,
    parsed_event,
    parsed_keyboard,
)


class ChannelDetails(NamedTuple):
    name: str = None
    units: str = None
    sampling_frequency: int = None
    path_save_figures: Path = None
    trial_name: str = None
    subject_id: str = None


class Channel:
    """Base class for all channel types

   Parameters
    ----------
    details
        name
            Name of channel (.e.g 'left biceps')
        units
            Units of recorded signal (e.g., 'Volts' or 'Nm')
        sampling_frequency
            In Hertz (e.g. 2048)
        path
            Defaults to path where data initially retrieved
        trialname
            Defaults to name of data file
        subject_id
            str indentifier
    times
        Sample times of data or events, in seconds
    """

    def __init__(self, details: ChannelDetails, times: np.ndarray) -> None:
        self.details = details
        self.times = times


class Event(Channel):
    """Event channel class
    Parameters
    ----------
    name
        Channel name
    data_dict
        data_dict['times']: np.ndarray of event times in seconds
    """

    def __init__(self, name: str, data_dict: parsed_event) -> None:
        super().__init__(
            ChannelDetails(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self) -> str:
        return "Event channel"

    def plot(self, save: Literal[True, False] = None) -> None:
        plot.channel(self, save=save)


class Keyboard(Channel):
    """Keyboard channel class

    Parameters
    ----------
    name
        Channel name
    data_dict
        data_dict['times']: np.ndarray of times of keyboard events, in seconds
        data_dict['codes']: np.ndarray of str associated with keyboard events
    """

    def __init__(self, name: str, data_dict: parsed_keyboard) -> None:
        self.codes = data_dict["codes"]
        super().__init__(
            ChannelDetails(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self) -> str:
        return "Keyboard channel"

    def plot(self, save: Literal[True, False] = None) -> None:
        plot.channel(self, save=save)

        
class Waveform(Channel, sig_proc.SignalProcessing):
    """Waveform channel class

        Parameters
        ----------
    data_dict
        data_dict['times']: np.ndarray of times of recorded signal, in seconds
        data_dict['values']: np.ndarray of recorded signal values
        data_dict['units']: str describing measurement units (e.g. 'Volts')
        data_dict['sampling_frequency']: int
    """

    def __init__(self, name: str, data_dict: parsed_waveform) -> None:
        details = ChannelDetails(
            name=name,
            units=data_dict["units"],
            sampling_frequency=data_dict["sampling_frequency"],
            path_save_figures=data_dict["path_save_figures"],
            trial_name=data_dict["trial_name"],
            subject_id=data_dict["subject_id"],
        )
        self.values = data_dict["values"]
        self.raw_values = self.values
        super().__init__(details, data_dict["times"])

    def __repr__(self) -> str:
        return "Waveform channel"

    def plot(self, save: Literal[True, False] = None) -> None:
        plot.channel(self, save=save)


class Wavemark(Channel):
    """Wavemark channel class

    Parameters
    ----------
    data_dict
        data_dict['times']: np.ndarray of action potential times, in seconds
        data_dict['action_potentials']: list of lists, where each list is a
            wavemark.
        data_dict['units']: str describing measurement units (e.g. 'Volts')
        data_dict['sampling_frequency']: int
    """

    def __init__(self, name: str, data_dict: parsed_wavemark) -> None:
        details = ChannelDetails(
            name=name,
            units=data_dict["units"],
            sampling_frequency=data_dict["sampling_frequency"],
            path_save_figures=data_dict["path_save_figures"],
            trial_name=data_dict["trial_name"],
            subject_id=data_dict["subject_id"],
        )
        super().__init__(details, data_dict["times"])
        self.action_potentials = data_dict["action_potentials"]
        self._calc_instantaneous_firing_frequency()

    def __repr__(self) -> str:
        return "Wavemark channel"

    def _calc_instantaneous_firing_frequency(self):
        time1: float = self.times[0]
        inst_firing_frequency = list()
        for time2 in self.times[1:]:
            inst_firing_frequency.append(1 / (time2 - time1))
            time1 = time2
        self.inst_firing_frequency = np.array(inst_firing_frequency)

    def plot(self, save: Literal[True, False] = None) -> None:
        plot.channel(self, save=save)
