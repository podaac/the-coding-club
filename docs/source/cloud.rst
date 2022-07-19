
Everything about Cloud
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Data migration to the cloud has been PO.DAAC's focus in the past two years. A collection of resources is made available here https://podaac.jpl.nasa.gov/cloud-datasets/about.


Why use Cloud?
~~~~~~~~~~~~~~~~
The short answer is "The data produced by NASA missions, such as SWOT and NISAR, is getting too big".

The long answer can be found in `this article (PDF format),  <https://cdn.earthdata.nasa.gov/conduit/upload/14963/01_Why_Use_the_Cloud.pdf>`_.

Current PO.DAAC data migration status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We are in Phase 5, the last phase of the data migration. Details can be found here https://podaac.jpl.nasa.gov/cloud-datasets/migration

The Beginners' Guide to PO.DAAC in the NASA Earthdata Cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This PODAAC webinar captured well the workflows on cloud-based data.

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/dS2mlI6r-_U" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Breakdown of the webinar:
^^^^^^^^^^^^^^^^^^^^^^^^^^^

=========== =======================================================================
Time        Topic
=========== =======================================================================
0-8:36      PO.DAAC data and user migration
8:36-15:50  PO.DAAC Cloud data access 101 - basic concept and terminology
15:50-      PO.DAAC Cloud data access 101 - Data Access Use cases Now vs Future
20:51-24:55 PO.DAAC Cloud data access 101 - Scripted data access, data-subscriber
20:51-30:36 PO.DAAC Cloud data access 101 - In-cloud access
30:36-32:22 PO.DAAC Cloud data access 101 - OPeNDAP
32:22-35:44 PO.DAAC Cloud data access 101 - Subset/Transform (Harmony)
35:44-38:40 PO.DAAC Cloud data access 101 - Future
38:40 -     PO.DAAC Webpage and cloud resources
=========== =======================================================================


Cloud computing resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Where to get an AWS cloud account?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is one of the most-asked question. Where to start? Below is a list of ranked choices.

1. Ask your institution
    Cloud computing is becoming more and more common. Institutions should have considered cloud computing as a part of their infrastructure, and most likely negotiated with cloud providers for a well discounted price. If you are a part of such an instituion, you should have access to the assitance of getting an AWS account. This is the first choice.

2. Get a free temporary account through NASA-sponsored programs
    NASA `ESDS <https://www.earthdata.nasa.gov/esds>`_ is promoting the cloud computing through supporting various programs that can provide temporary cloud-computing resources. This is one of the best ways to learn access the NASA Earthdata in the cloud and start to experimenting and prototyping cloud-native analysis. `Openscapes <https://www.openscapes.org/>`_ is an excellent example running excellent mentoring programs.

3. Get a free-tier account through AWS
    AWS is providing free-tier account <https://aws.amazon.com/free> to promote the hands-on experience with their platform, products and services. It provides a decent amount of free computing time for prototyping.

4. Budget cloud computing in your research proposals
    This is a long-term solution. Of course you need to write and win a proposal first. The cloud-computing can usually be included as a part of the IT support. Several thousands per year will be sufficient for prototyping. But the budget can easily become several hundred thousand for larger computation.


Cloud-based workflows
~~~~~~~~~~~~~~~~~~~~~~~~

There is no single workflow that fits all needs. Below are several examples  using `jupyter <https://jupyter.org/>`_ as a working environment.

Scenario #1 - Already has an access to a jupyterlab
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    *JupyterLab is a next-generation web-based user interface for Project Jupyter. It enables you to work with documents and activities such as Jupyter notebooks, text editors, terminals, and custom components in a flexible, integrated, and extensible manner.* --- Project Jupyter

If you have an institutional support or a NASA-sponsored program support (e.g., openscapes), you will most likely have a Jupyterlab environment to begin with. This is the ideal scenario, where scientists are provided with a computing environment and do not need to build a computing system by themselves.

What are the steps to learn?

#. Confirm that the AWS region of the jupyterlab is US-WEST-2. (`Here is an explaination of the AWS regions and zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html>`_)
#. Properly configure your EDL once you login the jupyterlab environment.
#. Learn through PODAAC tutorials, e.g.,

   * https://github.com/podaac/tutorials
   * https://github.com/podaac/Data-Recipes

Scenario #2 - Has an AWS account but need to start from scratch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a common scenario for those who have never used AWS cloud nor have institutional support, but were able to obtain an AWS free account. In this case, one need to

#. *spin up* an Elastic Cloud Computer (EC2), in other words an AWS computer,
#. ssh to the EC2 through ssh tunneling,
#. Install necessary software to start a jupyterlab,
#. Start jupyterlab from EC2,
#. Understand how to *ssh tunnel* to access to the EC2 jupyterlab environment through a web browser on your local machine.

This is a scenario that can be very time consuming and frustrating. We strongly suggest that you find and pair with a system admin to understand some basic IT concepts, such as Routing, Subnet, internet gateway, and `Amazon Virtual Private Cloud (VPC) <https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html>`_. If you are from a NASA center, the NASA cybersecurity rules may add another layer of complexity preventing you from a quick set up.

Where to find tutorials and examples?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Earthdata Cloud Primer Cloud Primer for Amazon Web Services https://www.earthdata.nasa.gov/learn/webinars-and-tutorials/cloud-primer-amazon-web-services
#. 2021 Cloud hackathon w/ Openscapes https://nasa-openscapes.github.io/2021-Cloud-Hackathon/
#. 2022 SWOT Oceanography PI Cloud hackathon
#. OPeNDAP in the cloud https://podaac.jpl.nasa.gov/OPeNDAP-in-the-Cloud
#. Harmony subsetting https://github.com/podaac/tutorials/blob/master/notebooks/cloudwebinar/harmony_subset.py
#. Working with ECCO in the cloud https://github.com/podaac/ECCO
#. Study Amazon Estuaries with Data from the EOSDIS Cloud https://github.com/podaac/tutorials/blob/master/notebooks/SWOT-EA-2021/Estuary_explore_inCloud_zarr.ipynb


Knowledge base
~~~~~~~~~~~~~~~~~~

The following is a result of the coding club activities.

Spin up an EC2
^^^^^^^^^^^^^^^^

SSH to an EC2
^^^^^^^^^^^^^^^^

Install necessary software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
