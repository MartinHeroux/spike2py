from collections import namedtuple
from pathlib import Path

import read
import channels


CHANNEL_GENERATOR = {
    "event": channels.Event,
    "keyboard": channels.Keyboard,
    "waveform": channels.Waveform,
    "wavemark": channels.Wavemark,
}


Trial_Info = namedtuple(
    "TrialInfo", "file channels name subject_id path_save_figures path_save_trial",
)
Trial_Info.__new__.__defaults__ = (None, None, None, None, None, None)


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
        trial_info.path_save_figures: str
            Path where trial and channel figures are to be saved
            Defaults to new 'figures' folder where .mat was retrieved
        trial_info.path_save_trial: str
            Path where trial data to be saved
            Defaults to new 'data' folder where .mat was retrieved
        """
        if not trial_info.file:
            raise ValueError(
                "trial_info must include a valid full path to a data file."
            )
        self._if_needed_add_defaults_to_trial_info(trial_info)
        self._parse_trial_data()

    def __repr__(self):
        channel_text = list()
        for channel_name, channel_type in self.channels:
            channel_text.append(f"\n\t\t{channel_name} ({channel_type})")
        channel_info = "".join(channel_text)
        return (
            f"\n{self.trial_info.name}"
            f"\n\tfile = {self.trial_info.file.absolute().as_uri()}"
            f"\n\tsubject_id = {self.trial_info.subject_id}"
            f"\n\tchannels {channel_info}"
        )

    def _if_needed_add_defaults_to_trial_info(self, trial_info):
        name = trial_info.name if trial_info.name else "trial"
        subject_id = trial_info.subject_id if trial_info.subject_id else "sub"
        path_save_figures = _check_make_path(
            path_to_check=trial_info.path_save_figures,
            path_to_make=Path(trial_info.file).parent / "figures",
        )
        path_save_trial = _check_make_path(
            path_to_check=trial_info.path_save_trial,
            path_to_make=Path(trial_info.file).parent / "data",
        )
        self.trial_info = Trial_Info(
            file=trial_info.file,
            channels=trial_info.channels,
            name=name.upper(),
            subject_id=subject_id,
            path_save_figures=path_save_figures,
            path_save_trial=path_save_trial,
        )

    def _parse_trial_data(self):
        trial_data = self._import_trial_data()
        channel_names = list()
        for key, value in trial_data.items():
            channel_names.append((key.title(), value["ch_type"]))
            value["path_save_figures"] = self.trial_info.path_save_figures
            value["trial_name"] = self.trial_info.name
            value["subject_id"] = self.trial_info.subject_id
            setattr(
                self, key.title(), CHANNEL_GENERATOR[value["ch_type"]](key, value),
            )
        self.channels = channel_names

    def _import_trial_data(self):
        return read.read(self.trial_info.file, self.trial_info.channels)


def _check_make_path(path_to_check, path_to_make):
    if path_to_check:
        path_to_check = Path(path_to_check)
    else:
        path_to_check = path_to_make
    if not path_to_check.exists():
        path_to_check.mkdir(parents=True)
    return path_to_check
