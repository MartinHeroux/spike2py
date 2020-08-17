How-To Guides
=============

Export your Spike2 data to `.mat`
---------------------------------

Rather than read `.smr` files directly, `spike2py` reads `.mat` files exported from Spike2. `spike2py` assumes that you used the default export settings when you exported your data. The process of exporting your data to `.mat` files is made simpler by running `this Spike2 script`_, which batch exports all `.smr` files from a given directory to `.mat` format.

Specify which channels are imported
-----------------------------------


.. _this Spike2 script: https://github.com/MartinHeroux/Spike2-batch-export-to-Matab