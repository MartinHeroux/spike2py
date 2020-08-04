import os


class Trial:
    """Class for experimental trial recorded using Spike2."""

    def __init__(self, file, name=None, subject_id=None, channels='All'):
        """

        Parameters
        ----------
        file: str
            Absolute path to data file. Only .mat files are currently supported.
        name: str (Default: name of file)
            Descriptive name of trial.
        subject_id: str
            Subject's study identifier
        channels: list
            List of channel names, as they appeared in the original .smr file.
            Example: ['biceps', 'triceps', 'torque']
            If not included, all channels will be processed.

        """
        if name is None:
            name = os.path.split(file)[-1].split('.')[0]
        self.name = name
        self.file = file
        self.subject_id = subject_id
        self.channels = channels
        #TODO: Update read.py and test_read.py based on `channels` default being 'All', which is more informative.
        self._import_trial_data(file, channels)

    def _import_trial_data(self):
        pass


