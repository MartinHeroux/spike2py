from collections import namedtuple

from spike2py import read, channels


CHANNEL_GENERATOR = {
    "event": channels.Event,
    "keyboard": channels.Keyboard,
    "waveform": channels.Waveform,
    "wavemark": channels.Wavemark,
}


TrialInfo = namedtuple(
    "TrialInfo", "file channels name subject_id path_figures path_save_trial"
)
TrialInfo.__new__.__defaults__ = (None, None, None, None, None, None)


class Trial:
    """Class for experimental trial recorded using Spike2."""

    def __init__(self, trial_info):
        """

        Parameters
        ----------
        trial_info.file: str
            Absolute path to data file. Only .mat files supported.
        trial_info.channels: list
            List of channel names, as they appeared in the original .smr file.
            Example: ['biceps', 'triceps', 'torque']
            If not included, all channels will be processed.
        trial_info.name: str (Default: name of file)
            Descriptive name of trial.
        trial_info.subject_id: str
            Subject's study identifier
        trial_info.path_figures: str
            Path where trial and channel figures are to be saved
        trial_info.path_save_trial: str
            Path where trial data to be saved
        """
        if not trial_info.file:
            raise ValueError(
                "trial_info must include a valid full path to a data file."
            )
        self.trial_info = trial_info
        self._parse_trial_data()

    def __repr__(self):
        return (
            f"Trial(file={repr(self.trial_info.file)}, \n\tchannels={self.trial_info.channels}, "
            f"\n\tname={self.trial_info.name}, \n\tsubject_id={self.trial_info.subject_id}\n\t)"
        )

    def _parse_trial_data(self):
        trial_data = self._import_trial_data()
        channel_names = list()
        for key, value in trial_data.items():
            channel_names.append((key, value["ch_type"]))
            value["fig_path"] = self.trial_info.path_figures
            value["trial_name"] = self.trial_info.name
            value["subject_id"] = self.trial_info.subject_id
            setattr(
                self, key, CHANNEL_GENERATOR[value["ch_type"]](key, value),
            )
        self.channels = channel_names

    def _import_trial_data(self):
        return read.read(self.trial_info.file, self.trial_info.channels)
