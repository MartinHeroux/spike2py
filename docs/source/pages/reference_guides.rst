Reference Guide
===============

.. module:: spike2py.trial

trial.TrialInfo
~~~~~~~~~~~~~~~
.. autoclass:: TrialInfo

trial.Trial
~~~~~~~~~~~
.. autoclass:: Trial
    :members: save

trial.load
~~~~~~~~~~
.. autofunction:: load


.. module:: spike2py.channels

channels.ChannelInfo
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: ChannelInfo

channels.Channel
~~~~~~~~~~~~~~~~
.. autoclass:: Channel

channels.Event
~~~~~~~~~~~~~~
.. autoclass:: Event
    :members: plot

channels.Keyboard
~~~~~~~~~~~~~~~~~
.. autoclass:: Keyboard
    :members: plot

channels.Waveform
~~~~~~~~~~~~~~~~~
.. autoclass:: Waveform
    :members: plot

channels.Wavemark
~~~~~~~~~~~~~~~~~
.. autoclass:: Wavemark
       :members: plot


.. module:: spike2py.sig_proc

sig_proc.SignalProcessing
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: SignalProcessing
       :members: remove_mean, remove_value, lowpass, highpass, bandpass, bandstop, calibrate, norm_percentage, norm_proportion, norm_percent_value, rect, interp_new_times, interp_new_fs, linear_detrend


.. module:: spike2py.plot

plot.plot_channel
~~~~~~~~~~~~~~~~~
.. autofunction:: plot_channel

plot.plot_trial
~~~~~~~~~~~~~~~
.. autofunction:: plot_trial


.. module:: spike2py.read

read.read
~~~~~~~~~
.. autofunction:: read
