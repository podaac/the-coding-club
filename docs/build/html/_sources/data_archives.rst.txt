
Data Archives and Access
---------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

The very first thing -- EDL and .netrc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NASA Earthdata, which includes PO.DAAC data, requires Earthdata Login (EDL) to access. The very first thing is to register an Earthdata Login account (free) from https://urs.earthdata.nasa.gov/.

Once you have registered the EDL, make sure to generate the **.netrc** file in your home directory. Some podaac tools, such as podaac-data-subscriber, will automatically read your EDL credential from the .netrc file. The result is a lifesaver: you do not need to enter your username and password every time you try to download some data.

Were you a hitchhiker to the Galaxy, **.netrc** is your towel. Spend some time, complete it, test it, set it once and for all. It is just a text file with two lines after all. It will save you from the frustration caused by constant popups of the out-of-nowhere error messages blocking you from getting to the data.

Find your data -- The search engines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NASA Earthdata search
^^^^^^^^^^^^^^^^^^^^^^^

PODAAC has 835 data collections, 344 of which have been migrated to the Cloud. By the Fall of 2022, all of the 835 collections will be in the Cloud and PODAAC on-premise services will be gradully deprecated. How to find a data collection that fits to your need?

The ultimate search engine for the NASA Earthdata is through Earthdata Search https://search.earthdata.nasa.gov/search. You can find not only PODAAC data but the data collections from all 12 DAACs. It is built on a centralized database called `The Common Metadata Repository (CMR) <https://cmr.earthdata.nasa.gov/search/>`_, currently has 8729 data collections.

The Earthdata search's interface is straightforward to use:

.. image:: media/earthdatasearch.png
   :width: 700
   :alt: Earthdata search

Search through PODAAC website
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have no interest of non-PODAAC data, https://podaac.jpl.nasa.gov/datasetlist can be a good place to find your data. The filter function in the left panel is particularly useful to narrow down a search.

.. image:: media/podaacsearch.png
   :width: 700
   :alt: PODAAC search


A glance of All data collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Search engine can speed up our quest for certain dataset or granules, but have you ever wondered for a complete list of all data collections? I have. When the total number is less than several hundred, a complete list can be very handy at times. Here they are.

* `This link points to a table of all PODAAC data collections <https://podaac.jpl.nasa.gov/datasetlist?view=table>`_

* `This link points to a table of all PODAAC data collections in the cloud <https://podaac.jpl.nasa.gov/datasetlist?view=table&provider=POCLOUD>`_.
