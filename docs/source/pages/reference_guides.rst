Reference Guide
===============

trial.Trial
~~~~~~~~~~~
.. module:: spike2py.trial

.. autoclass:: Trial
    :members: save

trial.TrialInfo
~~~~~~~~~~~~~~~
.. autoclass:: TrialInfo

.. module:: spike2py.channels

channels.Channel
~~~~~~~~~~~~~~~~
.. autoclass:: Channel

channels.ChannelInfo
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: ChannelInfo

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

.. module:: spike2py.plot

plot.channel
~~~~~~~~~~~~

.. autofunction:: spike2py.plot.channel

.. module:: spike2py.sig_proc

sig_proc.SignalProcessing
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: SignalProcessing
       :members: remove_mean, remove_value, lowpass, highpass, bandpass, bandstop, calibrate, norm_percentage, norm_proportion, norm_percent_value, rect, interp_new_times, interp_new_fs, linear_detrend