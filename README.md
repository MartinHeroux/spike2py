[![spike2py](https://raw.githubusercontent.com/MartinHeroux/spike2py/master/docs/source/img/spike2py_icon_600x300.png)](https://github.com/MartinHeroux/spike2py)


[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![coverage](https://img.shields.io/badge/coverage-96%25-yellowgreen)
    [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md)
[![Documentation Status](https://readthedocs.org/projects/spike2py/badge/?version=latest)](https://spike2py.readthedocs.io/en/latest/?badge=latest)

**spike2py** provides a simple interface to analyse and visualise data collected using [Spike2](http://ced.co.uk/products/spkovin) software and [Cambridge Electronics Design (CED)](http://ced.co.uk/) data acquisition boards. With it you can easily plot individual channels or all channels from a given trial. In addition, you can easily apply various signal processing methods to your `waveform` data. Finally, you can easily save your data at any point, allowing you to re-open and continue your work from where they left off.

To demonstrate, the following snippet of code shows you how to:

1. Read a file
2. Plot the electromyography (EMG) signal from one of the channels
2. Remove the mean of the first 500 samples and rectify EMG signal, and plot the result

```python
>>> from spike2py.trial import TrialInfo, Trial
>>> trial_info = TrialInfo(file="sample.mat")
>>> sample = Trial(trial_info)
>>> sample.muscle_emg.plot()
>>> sample.muscle_emg.remove_mean(first_n_samples=500).rect().plot()
```

[![emg_raw](https://raw.githubusercontent.com/MartinHeroux/spike2py/master/docs/source/img/EMG_400x132.png)](https://github.com/MartinHeroux/spike2py)

## Documentation

Introductory tutorials, how-to's and other useful documentation are available on [Read the Docs](https://spike2py.readthedocs.io/en/latest/index.html)

## Installing

**spike2py** is available on PyPI:

```console
$ python -m pip install spike2py
```

**spike2py** officially supports Python 3.8+.

## Caveat
**spike2py** works with Matlab files exported from Spike2 v7, or any other Spike2 version that exports to Matlab 5.0 format.
Spike2 v10 exports files to Matlab 7.3 format, which is currently not supported by **spike2py**.
The ability to open both Matlab file formats will be added in future version of **spike2py**.

## Contributing

Like this project? Want to help? We would love to have your contribution! Please see [CONTRIBUTING](CONTRIBUTING.md) to get started.

## Code of conduct

This project adheres to the Contributor Covenant code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [heroux.martin@gmail.com](heroux.martin@gmail.com).

## License

[GPLv3](./LICENSE)
