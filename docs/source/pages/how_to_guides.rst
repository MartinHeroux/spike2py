Learn something specific
========================

.. _export:

Export Spike2 data to .mat
----------------------------

Rather than read `.smr` files directly, *spike2py* reads `.mat` files exported from Spike2.

*spike2py* assumes that you used the default export settings when you exported your data. The process of exporting your data to `.mat` files is made simpler by running `this Spike2 script`_, which batch exports all `.smr` files from a given directory to `.mat` format.

.. _import:

Import .mat files using spike2py
--------------------------------

With our Spike2 data exported to `.mat`, we are now ready to import our data into Python using *spike2py*. To do this we need two of the most important classes in *spike2py*: TrialInfo and Trial.

The most basic way to import our data is as follows:

.. code-block:: python

    >>> from spike2py.trial import TrialInfo, Trial
    >>> trial_info = TrialInfo(file='tutorial.mat')
    >>> tutorial = Trial(trial_info)

And now we have our data imported and accessible in the `tutorial` variable.

**But what if my data is not in the same folder?**

That is easy. We simply have to provide the full path to our file. For example, on Linux and Mac I would use:

.. code-block:: python

    >>> trial_info = TrialInfo(file='/home/martin/Desktop/tutorial.mat')

And on Windows I would use:

.. code-block:: python

    >>> trial_info = TrialInfo(file='C:\Users\Martin\Desktop\tutorial.mat')


.. _pathinfo:

Provide additional inputs to TrialInfo
--------------------------------------
`TrialInfo` requires that `file` be specified. If this is the only parameter that we provide, all other parameters will default to `None`. While this is fine if we are having a quick look at our data, we usually will want to specify a few more of the `TrialInfo` parameters.

If we import `TrialInfo` and create an instance with no inputs, we get the following:

.. code-block:: python

    >>> from spike2py.trial import TrialInfo
    >>> trial_info = TrialInfo()
    >>> trial_info
    TrialInfo(
	    file=None,
	    channels=None,
	    name=None,
	    subject_id=None,
	    path_save_figures=None,
	    path_save_trial=None,
    )

If we pass inputs to `TrialInfo`, we might get something like this:

.. code-block:: python

    >>> trial_info
    TrialInfo(
	    file='tremor_postural.mat',
	    channels=['Flow', 'Co2'],
	    name='fatigue_50max',
	    subject_id='sub001',
	    path_save_figures='/home/martin/Desktop/figures',
	    path_save_trial='/home/martin/Desktop/data',
    )

See the following sections for an explanation of each of these additional inputs and how they are used by *spike2py*.

Specify channels to import
~~~~~~~~~~~~~~~~~~~~~~~~~~
There may be times when we don't want to import all available channels. We can specify the channels we want to import by passing a list of channel names to TrialInfo.

For example, the following code import only the `Flow`, and `Co2` channels from `tutorial.mat`:

.. code-block:: python

    >>> from spike2py.trial import TrialInfo, Trial
    >>> channels = ['Flow', 'Co2']
    >>> trial_info = TrialInfo(file='tutorial.mat', channels=channels)
    >>> tutorial = Trial(trial_info)
    >>> tutorial.channels
        [('Flow', 'waveform'), ('Co2', 'waveform')]

Note that we need to use the same spelling and capitalisation that we used in our Spike2 channel names.

Specify a trial name and a subject id
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Depending on how we process our data and the additional files and figures we want to generate, it can be useful to have access to a human-readable trial name and the id of the subject from whom we collected the data.

.. code-block:: python

    >>> from spike2py.trial import TrialInfo, Trial
    >>> sub_id = 'sub001'
    >>> trial_name = 'fatigue_50max'
    >>> trial_info = TrialInfo(file='tutorial.mat',
                               name=trial_name,
                               subject_id=subject_id)
    >>> tutorial = Trial(trial_info)
    >>> tutorial.info.name
        'fatigue_50max'
    >>> tutorial.info.subject_id
        'sub001;


Specify paths to save figures and data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By default, if we generate figures or save (i.e. pickle) our data, these will be stored in `figures` and `data` folders created in folder that contains the `.mat` file we passed to `TrialInfo`. However, we can specify a folder for one or both of these. For example:

.. code-block:: python

    >>> from spike2py.trial import TrialInfo, Trial
    >>> path_save_figures='/home/martin/Desktop/nice_figures'
    >>> path_save_trial = '/home/martin/Documents/vault'
    >>> trial_info = TrialInfo(file='tutorial.mat',
                               path_save_figures=path_to_figures,
	                           path_save_trial=path_save_trial
	                           )
    >>> tutorial = Trial(trial_info)
    >>> tutorial.info.path_save_figures
        PosixPath('/home/martin/Desktop/nice_figures')
    >>> tutorial.info.path_save_trial
        PosixPath('/home/martin/Documents/vault')

The `PosixPath` part of the return value reflects the fact that *spike2py* uses `pathlib`_ to create and manage paths.


.. _this Spike2 script: https://github.com/MartinHeroux/Spike2-batch-export-to-Matab
.. _pathlib: https://docs.python.org/3/library/pathlib.html