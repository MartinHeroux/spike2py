`spike2py`_ provides a simple interface to analyse and visualise data collected using `Spike2`_ software and `Cambridge Electronics Design (CED)`_ data acquisition boards. With it you can easily plot individual channels to as well as all channels from a given trial. In addition, you can easily apply various signal processing methods to your `waveform` data. Finally, you can easily save your data at any point, allowing you to re-open and continue your work from where they left off.

To demonstrate, the following snippet of code shows you how to:

1. Read a file
2. Remove the mean, rectify and low-pass filter from EMG data
3. Plot the resulting data

>>> from spike2py.trial import TrialInfo, Trial
>>> trial_info = TrialInfo(file="sample.mat")
>>> sample = Trial(trial_info)
>>> sample.Ext.remove_mean().rect().lowpass(cutoff=5)
>>> sample.Ext.plot()

.. _spike2py: https://github.com/MartinHeroux/spike2py
.. _Spike2: http://ced.co.uk/products/spkovin
.. _Cambridge Electronics Design (CED): http://ced.co.uk/
.. _SonPy: http://ced.co.uk/upgrades/spike2sonpy
.. _scipy: .. _`scipy.io`: https://docs.scipy.org/doc/scipy/reference/io.html
