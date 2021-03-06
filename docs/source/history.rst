
PO.DAAC history
---------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Milestones
~~~~~~~~~~~~~~~~~~~~~~
.. image:: _static/podaac_history.png
   :width: 700
   :alt: PODAAC history


The short-lived Seasat -- the cornerstone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: media/seasat.jpg
   :width: 100
   :alt: Seasat 

The origin of the PO.DAAC is historically traced to the short lived operation of the NASA Seasat mission launched in 1978.  The Seasat altimeter, one of several instruments on the Seasat platform, was among the first space based remote sensing instruments dedicated to large scale oceanographic measurements of sea level, but only survived for a few months. However, the measurements from this and the other instruments represented scientific breakthroughs for the period and made commensurate demands for data storage, access and distribution.  

The PODS and NODS -- from tapes to CD-ROMS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Pilot Ocean Data System (PODS), a distant precursor to PO.DAAC, was founded at JPL to meet these demands including implementing distribution (and subsetting!) of data from local hard disks for local users, and via time series plots and magnetic tapes for remote users. Later to meet the needs of more emerging oceanographic missions, and as the data infrastructure and management matured, PODS morphed into the NASA Ocean Data System (NODS). More robust data access included distribution via CD-ROMs in addition to tapes. 

The beginning of PO.DAAC -- FTP and HTTPS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, in 1991 the PO.DAAC was established as the archive of record and distribution source for the successful TOPEX/Poseidon altimeter launched in 1992, and the instrument that has served as the foundation of the modern satellite observed sea level record. During this period, the PO.DAAC developed improved infrastructure to implement distribution via FTP, later HTTPS, and other online servers as part of the family of DAACs within the NASA EOSDIS program.  This included developing and deploying web services for data extraction, subsetting and visualization, and data discovery and search, and metadata services.

The need of Cloud by SWOT -- a New Era
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Surface Water and Ocean Topography (SWOT) mission will use a high-resolution Ka-band Interferometer to measure the ocean sea surface topography and terrestrial waters. It will generate more than 20 Terabytes/day data flow. On-premise data management and distribution becomes less practical. A new strategy and data management was adopted that focuses on leveraging the extendable scale and flexibility of cloud storage and computing.  This was not only a PO.DAAC decision but the entire NASA Earth Science Data Systems program has made a technical and business decision to move its data derived from earth observing assets to the cloud to streamline the data management (ingest, archive, discovery, distribution) using open source software, improve management of distribution and storage costs, promote open science, analysis in place, and interdisciplinary science across the spectrum of its measurements, and reduce data movement (download). 

Cloud-based data management is relatively new to Earth science. Adapting to the new system can be disorienting. This guidebook aims to estabilish clear pathways to PO.DAAC data and tools.     

Further reading:

Hausman, J., D. Moroni, M. Gangl, V. Zlotnicki, J. Vazquez-Cuervo, E. M. Armstrong, C. Oaida, M. Gierach, C. Finch, and C. Schroeder. 2019. The evolution of the PO.DAAC: Seasat to SWOT. Advances in Space Research, https://doi.org/10.1016/j.asr.2019.11.030.
