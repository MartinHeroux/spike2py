import pickle
from pathlib import Path
from dataclasses import dataclass
from typing import List, Literal, Union

from spike2py import channels, read, plot


CHANNEL_GENERATOR = {
    "event": channels.Event,
    "keyboard": channels.Keyboard,
    "textmark": channels.Textmark,
    "waveform": channels.Waveform,
    "wavemark": channels.Wavemark,
}


@dataclass
class TrialInfo:
    """Information about trial

    See :class:`spike2py.trial.Trial` parameters for details.
    """

    file: Path = None
    channels: List[str] = None
    name: str = None
    subject_id: str = None
    path_save_figures: Path = None
    path_save_trial: Path = None

    def __repr__(self):
        return (
            f"TrialInfo(\n"
            f"\tfile={repr(self.file)},\n"
            f"\tchannels={repr(self.channels)},\n"
            f"\tname={repr(self.name)}, \n"
            f"\tsubject_id={repr(self.subject_id)},\n"
            f"\tpath_save_figures={repr(self.path_save_figures)},\n"
            f"\tpath_save_trial={repr(self.path_save_trial)},\n"
            f")"
        )


class Trial:
    """Class for experimental trial recorded using Spike2

    Parameters
    ----------
    trial_info : NamedTuple
        file : pathlib.Path, str
            Absolute path to data file. Only .mat files supported
        channels : List[str]
            List of channel names, as they appeared in the original .smr file
            Example: ['biceps', 'triceps', 'torque']
            If not included, all channels will be processed
        name : str
            Descriptive name for trial; defaults to filename
        subject_id : str
            Subject's study identifier
        path_save_figures : pathlib.Path
            Path where trial and channel figures are to be saved
            Defaults to new 'figures' folder where .mat was retrieved
        path_save_trial : pathlib.Path
            Path where trial data to be saved
            Defaults to new 'data' folder where .mat was retrieved

    Attributes
    ----------
    trial_info : NamedTuple
        Same as parameter
    channels : List[Tuple[str, str]]
        Pairs of channel names and channel types.
        For example: [('Torque', 'waveform'), ('Trigger', 'event')]
    <Channels> : channels.Channel
        Each channel appears with its name as an attribute.
        For example: trial1.Torque

    Raises
    ------
    ValueError
        If parameter `info.file` is not a valid full path to a data file

    """

    def __init__(self, trial_info: TrialInfo) -> None:
        if not trial_info.file:
            raise ValueError("info must include a valid full path to a data file.")
        self._add_defaults_to_trial_info(trial_info)
        self._parse_trial_data()

    def __repr__(self) -> str:
        channel_text = list()
        for channel_name, channel_type in self.channels:
            channel_text.append(f"\n\t\t{channel_name} ({channel_type})")
        channel_info = "".join(channel_text)
        return (
            f"\n{self.info.name}"
            f"\n\tfile = {Path(self.info.file).absolute().as_uri()}"
            f"\n\tsubject_id = {self.info.subject_id}"
            f"\n\tpath_save_figures = {self.info.path_save_figures}"
            f"\n\tpath_save_trial = {self.info.path_save_trial}"
            f"\n\tchannels {channel_info}"
        )

    def _add_defaults_to_trial_info(self, trial_info: TrialInfo):
        name = trial_info.name if trial_info.name else Path(trial_info.file).stem
        subject_id = trial_info.subject_id if trial_info.subject_id else "sub"
        path_save_figures = _check_make_path(
            path_to_check=trial_info.path_save_figures,
            path_to_make=Path(trial_info.file).parent / "figures",
        )
        path_save_trial = _check_make_path(
            path_to_check=trial_info.path_save_trial,
            path_to_make=Path(trial_info.file).parent / "data",
        )
        self.info = TrialInfo(
            file=Path(trial_info.file),
            channels=trial_info.channels,
            name=name,
            subject_id=subject_id,
            path_save_figures=path_save_figures,
            path_save_trial=path_save_trial,
        )

    def _parse_trial_data(self):
        trial_data = self._import_trial_data()
        channel_names = list()
        for key, value in trial_data.items():
            channel_names.append((key.title(), value["ch_type"]))
            value["path_save_figures"] = self.info.path_save_figures
            value["trial_name"] = self.info.name
            value["subject_id"] = self.info.subject_id
            setattr(
                self,
                key.title(),
                CHANNEL_GENERATOR[value["ch_type"]](key, value),
            )
        self.channels = channel_names

    def _import_trial_data(self):
        return read.read(self.info.file, self.info.channels)

    def plot(self, save: Literal[True, False] = None) -> None:
        plot.plot_trial(self, save=save)

    def save(self):
        """Save trial

        Trial will be saved (pickled) to `info.path_save_trial` as info.name + '.pkl'

        """
        if not self.info.path_save_trial.exists():
            self.info.path_save_trial.mkdir()
        pickle_file = self.info.path_save_trial / (self.info.name + ".pkl")
        with open(pickle_file, "wb") as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)


def _check_make_path(path_to_check: Path, path_to_make: Path):
    if path_to_check:
        path_to_check = Path(path_to_check)
    else:
        path_to_check = path_to_make
    if not path_to_check.exists():
        path_to_check.mkdir(parents=True)
    return path_to_check


def load(file: Union[Path, str]) -> Trial:
    """Load saved (pickled) trial

    Parameters
    ----------
    file: pathlib.Path, str
        Full path and file name to pickled file.
        For example: '/home/tammy/Desktop/trial1.pkl`

    Returns
    -------
    Trial
        Instance of Trial class that was previously saved

    """
    with open(file, "rb") as trial_file:
        return pickle.load(trial_file)
