

class Channel:
    """Base class for all channel types"""

    def __init__(self, name, trial_name):
        """Create Channel instance

        Parameters
        ----------
        name: str
            Channel name
        trial_name: str
            Trial name
        """
        self.name = name
        self.trial_name = trial_name


class Event(Channel):
    """Event channel class"""

    def __init__(self, name, trial_name, times):
        """Create Event channel instance

        Parameters
        ----------
        times: numpy.ndarray
            Times of events, in seconds
        """
        self.times = times
        super().__init__(name, trial_name)


class Keyboard(Event):
    """Keyboard channel class"""

    def __init__(self, times, codes, name, trial_name):
        """Create Keyboard channel instance

        Parameters
        ----------
        times: numpy.ndarray
            Times of keyboard inputs, in seconds
        codes: str
            Keyboard inputs
        """

        self.codes = codes
        super().__init__(times, name, trial_name)


class Waveform(Event):
    """Waveform channel class"""

    def __init__(self, times, units, values, sampling_frequency, name, trial_name):
        """Create Waveform channel instance

        Parameters
        ----------
        times: numpy.ndarray
            Time axis in seconds
        units: str
            Measurement units of `values`, if provided
        values: numpy.ndarray
            Sampled data
            Same length as `times`
        sampling_frequency: int
            Sampling frequency used to record data
        """

        self.units = units
        self.values = values
        self.sampling_frequency = sampling_frequency
        super().__init__(times, name, trial_name)


class Wavemark(Event):
    """Wavemark channel class"""

    def __init__(self, units, template_length, times, sampling_frequency,
                 action_potentials, name, trial_name):
        """Create Wavemark channel instance

        Parameters
        ----------
        units str
            Measurement units of `values`, if provided
            Will usually be Volts
        template_length: int
            Length, in samples, of the template used to sort the wavemark
        times: numpy.ndarray
            Times of wavemarks, in seconds
        sampling_frequency: int
            Sampling frequency used to record data from which wavemarks were obtained
        action_potentials: list
            A list of lists containing wavemark data of length `template_length` for each
            occurrence of the wavemark, of which there are `len(times)`
        """

        self.units = units
        self.template_length = template_length
        self.sampling_frequency = sampling_frequency
        self.action_potentials = action_potentials
        super().__init__(times, name, trial_name)
