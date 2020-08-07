from collections import namedtuple

from .signal_processing import SignalProcessing
import plot


Details = namedtuple('Details', 'name units sampling_frequency')
Details.__new__.__defaults__ = (None, None, None)


class Channel:
    """Base class for all channel types

   Parameters
    ----------
    details: namedtuple
        details.name: str
            Name of channel (.e.g 'left biceps')
        details.units: str
            Units of recorded signal (e.g., 'Volts' or 'Nm')
        details.sampling_frequency: int
            In Hertz (e.g. 2048)
    times: numpy.ndarray
        Sample times of data or events, in seconds
    """

    def __init__(self, details, times):
        self.details = details
        self.times = times


class Event(Channel):
    """Event channel class
    Parameters
    ----------
    times: numpy.ndarray
        Times of events, in seconds
    """

    def __init__(self, name, data_dict):
        details = Details(name=name)
        super().__init__(details, data_dict['times'])

    def __repr__(self):
        return 'Event channel'

    def plot(self):
        plot.event(self.details, self.times)


class Keyboard(Channel):
    """Keyboard channel class

    Parameters
    ----------
    codes: str
        Keyboard inputs
    """

    def __init__(self, name, data_dict):
        details = Details(name=name)
        self.codes = data_dict['codes']
        super().__init__(details, data_dict['times'])

    def __repr__(self):
        return 'Keyboard channel'

    def plot(self):
        plot.keyboard(self.details, self.times, self.codes)


class Waveform(Channel, SignalProcessing):
    """Waveform channel class

        Parameters
        ----------
        values: numpy.ndarray
            Sampled data
            Same length as `times`
    """

    def __init__(self, name, data_dict):
        details = Details(name=name, units=data_dict['units'], sampling_frequency=data_dict['sampling_frequency'])
        self.values = data_dict['values']
        super().__init__(details, data_dict['times'])

    def __repr__(self):
        return 'Waveform channel'

    def plot(self):
        plot.waveform(self.details, self.times, self.values)


class Wavemark(Channel):
    """Wavemark channel class

    Parameters
    ----------
    action_potentials: list
        A list of lists containing wavemark data of length `template_length`
        for each occurrence of the wavemark, of which there are `len(times)`
    """

    def __init__(self, name, data_dict):
        details = Details(name=name, units=data_dict['units'], sampling_frequency=data_dict['sampling_frequency'])
        self.action_potentials = data_dict['action_potentials']
        super().__init__(details, data_dict['times'])
        self._calc_instantaneous_firing_frequency()

    def __repr__(self):
        return 'Wavemark channel'

    def _calc_instantaneous_firing_frequency(self):
        time1 = self.times[0]
        instantaneous_firing_frequency = list()
        for time2 in self.times[1:]:
            instantaneous_firing_frequency.append(1/(time2-time1))
        self.instantaneous_firing_frequency = instantaneous_firing_frequency

    def plot(self):
        plot.wavemark(self.details, self.times, self.action_potentials)
