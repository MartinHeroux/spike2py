Topic Guides
============

What **spike2py** is (and what it isn't)
----------------------------------------
**spike2py** is (somewhat) based on the Unix philosophy: do one thing and do it well. We say 'somewhat' because **spike2py** actually does a few things. We also say 'somewhat' because the jury is still out on whether **spike2py** actually does things well!

**spike2py** aims to simplify a few of the basic speed bumps to analysing Spike2 data in Python.

1. It imports and parses the data
2. It plots trial and channel data
3. It stores data for later use
4. It can execute many common signal processing steps

The rest is left up to you, the user.

You will have to code the analysis pipeline to extract the outcomes you are interested in across the all the trials from collected from all your participants. You will have to code your own figures to highlight certain aspects of your data.

**spike2py** has room to grow, but only a little. Extra functionality can be added, but only if it fits within the four primary aims of **spike2py**.

Alternatives to spike2py
------------------------

`Cambridge Electronics Design`_ maintain and distribute the `SonPy`_ library, which supports Python 3. Unfortunately, `SonPy` is only available as a Windows installer, and its interface is somewhat complex for users new to programming and Python.

Another option is `Neo`_, a Python package for working with electrophysiology data in Python. As stated by the authors, "The goal of Neo is to improve interoperability between Python tools for analyzing, visualizing and generating electrophysiology data by providing a common, shared object model." This package has been around since 2014 and is still actively being developed.

.. _Cambridge Electronics Design: http://ced.co.uk/
.. _SonPy: http://ced.co.uk/upgrades/spike2sonpy
.. _Neo: https://github.com/NeuralEnsemble/python-neo
