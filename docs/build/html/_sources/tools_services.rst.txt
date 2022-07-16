Tools and services
--------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The mighty podaac-data-subscriber
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Data lives in a server, which is called on-premise if it is in a cooled room at Pasadena several miles to our office at JPL but called **Cloud** if it is in one of the Amazon Web Service (AWS) facilities. The point is that basic data access should not be very different regardless where the data are hosted.

The `podaac-data-subscriber <https://github.com/podaac/data-subscriber>`_ makes downloading the PODAAC data super easy.

If your workflow involves downloading data to your local machine, the data-subscriber is the recommended tool to use. The github page has clear instruction on installation and usage.

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
