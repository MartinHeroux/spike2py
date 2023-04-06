from pathlib import Path

from spike2py.trial import TrialInfo, Trial
channels_1 = ['MMax', 'Ds8', 'Keyboard', 'FDI', 'stim']
channels_2 = ['Ds8', 'Keyboard', 'FDI', 'stim']

test_file = Path('/home/martin/Dropbox/Martin/sketchbook/python/projects/spike2py_reflex/data/02_data000_HF_B.mat')

try:
    trial_info = TrialInfo(file=test_file.__str__(),
                           channels=channels_1)
    test_data = Trial(trial_info)
except ValueError:
    trial_info = TrialInfo(file=test_file.__str__(),
                           channels=channels_2)
    test_data = Trial(trial_info)


test_data.plot()

