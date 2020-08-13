from pathlib import Path

from spike2py import read, channels


CHANNEL_GENERATOR = {
    "event": channels.Event,
    "keyboard": channels.Keyboard,
    "waveform": channels.Waveform,
    "wavemark": channels.Wavemark,
}


class Trial:
    """Class for experimental trial recorded using Spike2."""

    def __init__(self, file, channels=None, name=None, subject_id=None):
        """

        Parameters
        ----------
        file: str
            Absolute path to data file. Only .mat files supported.
        channels: list
            List of channel names, as they appeared in the original .smr file.
            Example: ['biceps', 'triceps', 'torque']
            If not included, all channels will be processed.
        name: str (Default: name of file)
            Descriptive name of trial.
        subject_id: str
            Subject's study identifier

        """
        if name is None:
            name = Path(file).stem
        self.name = name
        self.file = file
        self.channels = channels
        self.subject_id = subject_id
        self._parse_trial_data()

    def __repr__(self):
        return (
            f"Trial(file={repr(self.file)}, \n\tchannels={self.channels}, "
            f"\n\tname={self.name}, \n\tsubject_id={self.subject_id}\n\t)"
        )

    def _parse_trial_data(self):
        trial_data = self._import_trial_data()
        channel_names = list()
        for key, value in trial_data.items():
            channel_names.append((key, value["ch_type"]))
            setattr(self, key, CHANNEL_GENERATOR[value["ch_type"]](key, value))
        self.channels = channel_names

    def _import_trial_data(self):
        return read.read(self.file, self.channels)
