.. _installation:

Installation
============

Create a virtual environment
----------------------------

spike2py works with `Python 3.8 or above`_. It is recommended you create a dedicated `Python environment`_ before you install spike2py. In your project directory, run the following commands:

.. code-block:: bash

   python -m venv env

Then activate your new virtual environment.

On macOS and Linux:

.. code-block:: bash

   source env/bin/activate

On Windows:

.. code-block:: bash

   .\env\Scripts\activate

Install spike2py and its dependencies
-------------------------------------

With your virtual environment activated, run the following command:

.. code-block:: bash

   pip install spike2py

Testing your spike2py installation
----------------------------------

With your virtual environment activated, start Python and type the following:

.. code-block:: python

    >>> import spike2py
    >>> spike2py.demo.test_install()

    Figure 1: sample.Flow.plot()
    Figure 2: sample.Flow.lowpass(cutoff=4, order=8).plot()
    Figure 3: sample.Volume.plot()
    Figure 4: sample.Volume.remove_mean().linear_detrend().plot()
    Figure 5: sample.plot()

You should see a series of five figures.


.. _Python 3.8 or above: https://www.python.org/downloads/
.. _Python environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment