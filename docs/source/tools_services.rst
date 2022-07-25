Tools and services
--------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The mighty podaac-data-subscriber - download data using one line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `podaac-data-subscriber <https://github.com/podaac/data-subscriber>`_ makes downloading the PODAAC data in the cloud super easy.

If your workflow involves downloading data to your local machine, the data-subscriber is the recommended tool to use. Its github page has a clear instruction on the installation and usage.

The information you need is the short_name for a particular data collection, which can be found from the data collection's landing page. For example, if you are interested in the gridded SSH products from the MEaSURES project, go to podaac.jpl.nasa.gov, search "MEaSUREs Gridded Sea Surface Height Anomalies"



The conventional way using wget and curl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This link points to `Instructions for HTTPS download from the PO.DAAC and NASA Earthdata <https://github.com/podaac/tutorials/blob/master/notebooks/batch_download_podaac_data.md>`_.

A quick look at the data through SOTO and Worldview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Subset large data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Subsetting capability is necessary for large data with high spatial resolution. `HiTiDE <https://podaac-tools.jpl.nasa.gov/hitide/>`_ provides subsetting services for a small group of high-resolution data collections.

HiTiDE
^^^^^^^^
.. image:: media/hitide.png
   :width: 700
   :alt: HiTiDE
