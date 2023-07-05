from pathlib import Path
from typing import NamedTuple, Literal

import numpy as np

import spike2py.plot as plot
import spike2py.sig_proc as sig_proc

from spike2py.types import (
    parsed_wavemark,
    parsed_waveform,
    parsed_textmark,
    parsed_event,
    parsed_keyboard,
)


class ChannelInfo(NamedTuple):
    """Information about channel

    See :class:`spike2py.channels.Channel` parameters for details.
    """

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
     channel_info
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
         Sample times in seconds
    """

    def __init__(self, channel_info: ChannelInfo, times: np.ndarray) -> None:
        self.info = channel_info
        self.times = times


class Event(Channel):
    """Event channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of Event channel
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Event was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Event times in seconds
    """

    def __init__(self, name: str, data_dict: parsed_event) -> None:
        super().__init__(
            ChannelInfo(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self) -> str:
        return "Event channel"

    def plot(self, save: Literal[True, False] = False) -> None:
        """Save Event channel figure

        Parameters
        ----------
        save
            Set to `True` to save Event figure to `path_save_figures`
        """
        plot.plot_channel(self, save=save)
        return self


class Keyboard(Channel):
    """Keyboard channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of Keyboard channel; default is 'keyboard'
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Keyboard was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Event times in seconds
        - ['codes']: np.ndarray of str associated with keyboard events
    """

    def __init__(self, name: str, data_dict: parsed_keyboard) -> None:
        self.codes = data_dict["codes"]
        super().__init__(
            ChannelInfo(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self) -> str:
        return "Keyboard channel"

    def plot(self, save: Literal[True, False] = False) -> None:
        """Save Keyboard channel figure

        Parameters
        ----------
        save
            Set to `True` to save Keyboard figure to `path_save_figures`
        """

        plot.plot_channel(self, save=save)
        return self


class Textmark(Channel):
    """Textmark channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of textmark channel; default is 'Memory'
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Keyboard was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Event times in seconds
        - ['codes']: np.ndarray of str associated with keyboard events
    """

    def __init__(self, name: str, data_dict: parsed_textmark) -> None:
        self.codes = data_dict["codes"]
        super().__init__(
            ChannelInfo(
                name=name,
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self) -> str:
        return "Textmark channel"

    def plot(self, save: Literal[True, False] = False) -> None:
        """Save Textmark channel figure

        Parameters
        ----------
        save
            Set to `True` to save Textmark figure to `path_save_figures`
        """

        plot.plot_channel(self, save=save)
        return self


class Waveform(Channel, sig_proc.SignalProcessing):
    """Waveform channel class

    Inherits from Channel and sig_proc.SignalProcessing

    Parameters
    ----------
    name
        Name of Waveform channel
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Waveform was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Waveform times in seconds
        - ['values']: np.ndarray - Waveform float values
        - ['units']: str - Measurement units (e.g. 'Volts')
        - ['sampling_frequency']: int - Sampling frequency of Wavemark
    """

    def __init__(self, name: str, data_dict: parsed_waveform) -> None:
        self.values = data_dict["values"]
        self.raw_values = self.values
        super().__init__(
            ChannelInfo(
                name=name,
                units=data_dict["units"],
                sampling_frequency=data_dict["sampling_frequency"],
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )

    def __repr__(self) -> str:
        return "Waveform channel"

    def plot(self, save: Literal[True, False] = None) -> None:
        """Save Waveform channel figure

        Parameters
        ----------
        save
            Set to `True` to save Waveform figure to `path_save_figures`
        """
        plot.plot_channel(self, save=save)
        return self


class Wavemark(Channel):
    """Wavemark channel class

    Inherits from Channel

    Parameters
    ----------
    name
        Name of Wavemark channel
    data_dict:
        - ['path_save_figures']: Path - Directory where channel figure saved
        - ['trial_name']: str - Name of trial where Wavemark was recorded
        - ['subject_id']: str - Identifier
        - ['times']: np.ndarray - Wavemark times in seconds
        - ['values']: np.ndarray - Waveform float values
        - ['action_potentials']: list of lists - Each list is a Wavemark
        - ['units']: str - Measurement units (e.g. 'Volts')
        - ['sampling_frequency']: int - Sampling frequency of Wavemark
    """

    def __init__(self, name: str, data_dict: parsed_wavemark) -> None:
        super().__init__(
            ChannelInfo(
                name=name,
                units=data_dict["units"],
                sampling_frequency=data_dict["sampling_frequency"],
                path_save_figures=data_dict["path_save_figures"],
                trial_name=data_dict["trial_name"],
                subject_id=data_dict["subject_id"],
            ),
            data_dict["times"],
        )
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

    def plot(self, save: Literal[True, False] = None):
        """Save Waveform channel figure

        Parameters
        ----------
        save
            Set to `True` to save Wavemark figure to `path_save_figures`
        """
        plot.plot_channel(self, save=save)
        return self
