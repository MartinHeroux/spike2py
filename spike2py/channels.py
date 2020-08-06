from collections import namedtuple


def channel_details(name=None, trial=None, units=None, sampling_frequency=None):
    Details = namedtuple('Details', 'name trial units sampling_frequency')
    return Details(name=name,
                   trial=trial,
                   units=units,
                   sampling_frequency=sampling_frequency,
                   )


class Channel:
    """Base class for all channel types

   Parameters
    ----------
    details: namedtuple
        details.name: str
            Name of channel (.e.g 'left biceps')
        details.trial: str
            Name of trial (.e.g. 'fatigue_5min')
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

    def __init__(self, details, times):
        super().__init__(details, times)


class Keyboard(Channel):
    """Keyboard channel class

    Parameters
    ----------
    codes: str
        Keyboard inputs
    """

    def __init__(self, details, times, codes):
        self.codes = codes
        super().__init__(details, times)


class Waveform(Channel):
    """Waveform channel class

        Parameters
        ----------
        values: numpy.ndarray
            Sampled data
            Same length as `times`
    """

    def __init__(self, details, times, values):
        self.values = values
        super().__init__(details, times)


class Wavemark(Channel):
    """Wavemark channel class

    Parameters
    ----------
    template_length: int
        Length, in samples, of the template used to sort the wavemark
    action_potentials: list
        A list of lists containing wavemark data of length `template_length`
        for each occurrence of the wavemark, of which there are `len(times)`
    """

    def __init__(self, details, times, action_potentials):
        self.action_potentials = action_potentials
        super().__init__(details, times)
