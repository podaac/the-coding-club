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

Data Visualization through SOTO and NASA Worldview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The PO.DAAC State of the Oceans (SOTO) tool is an interactive, web-based tool for visualizing
oceangraphic satellite maps, creating animations and querying data values. The purpose of the tool is to
promote discovery and investigation of ocean phenomena. The technology and its contents are based on the
NASA WorldView system but it has been engineered to meet the needs of the ocean community and PO.DAAC data.


SOTO
^^^^^^^^
.. image:: media/soto.png
   :width: 700



Subset large data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Subsetting capability is necessary for large data with high spatial resolution. `HiTiDE <https://podaac-tools.jpl.nasa.gov/hitide/>`_ provides subsetting services for a small group of high-resolution data collections.

HiTiDE
^^^^^^^^
.. image:: media/hitide.png
   :width: 700
   :alt: HiTiDE
