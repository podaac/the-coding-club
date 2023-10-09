# Dask for Parallelized Analysis of NASA Earthdata in the Cloud

Included here are a collection of notebooks which demonstrate Dask (Python package) for parallel computing in the cloud using AWS resources and Earth data hosted by NASA. They are meant to be both pedagogical and serve as a quick reference/refresher, but do assume some prerequisite knowledge. Included in this readme is a short introduction to parallel computing and Dask, prerequisites you should have to understand the notebooks, and a [short description of each notebook](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/readme.md#notebooks).

## Parallel Computing and Dask
Tersely, parallel computing is a method which:
1. Allows computation of data which is larger than the RAM of a single machine. For example, execution of a block of code can be assigned to processors across multiple machines, allowing the memory requirements to be shared among them.
2. Can make certain computations run faster. For example, the Macbook used to write this readme file has 10 processors, but normal execution of Python code will not utilized the processors in parallel (e.g. split up the work across the processors simultaneously). Parallel processing allows for this.

Dask is a Python package which will let your code utilize parallel processing. It does require a slight modification to the way in which e.g. NumPy is used (and also forces you to not take shortcuts in learning proper syntax for Xarray).

A great further introduction to these concepts can be found on the second bullet of the Prerequisites section below.

## Prerequisites
* Basic knowledge of what the Cloud is and **accessing NASA Earthdata on the Cloud**. If not, checkout the [NASA Earthdata Cloud Cookbook](https://nasa-openscapes.github.io/earthdata-cloud-cookbook/).
* If not familiar with Dask and Parallel computing, read these two brief pages from Ryan Abernathey's book ["An Introduction to Earth and Environmental Data Science"](https://earth-env-data-science.github.io/intro.html):
  1. [Dask intro](https://earth-env-data-science.github.io/lectures/dask/intro.html)
  2. [Basic computations with Dask](https://earth-env-data-science.github.io/lectures/dask/dask_arrays.html)
* **Some Python coding experience**. Basic familiarity is required, more experience with key packages for scientific analysis (e.g. Xarray, NumPy) is encouraged. These packages will be used in the notebooks, and using them with Dask works only if the proper syntax is used, which will likely be familiar to those who have already worked with them. However, don't let this stop you from jumping in!
* **Ability to start a virtual machine (VM) in AWS**. All notebooks here assume that you are in a VM in AWS, and will not work unless you are. E.g. you can spin up your own EC2 instance, use a Cloud Playground service, or try out [Coiled](https://www.coiled.io) (very useful, but does charge a fee).

## Other Resources
* [Pythia](https://projectpythia.org) Comprehensive and pedagogical overview to key concepts in Python Coding for analyzing Earth datasets. Great resource if any of the concepts covered in these notebooks are unfamiliar. It is an educational working group for Pangeo.
* [Pangeo](https://pangeo.io) Compunity platform for big data geoscience
* [Dask website and documentation](https://www.dask.org)

## Notebooks
* [basic_dask.ipynb](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/basic_dask.ipynb). Simple introduction (or refresher) to accessing NASA Earthdata in the cloud with Xarray and basic processing with and without Dask.
* [aggregation_functions.ipynb](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/aggregation_functions.ipynb). Covers parallel methods to subset data and apply aggregation functions (e.g. mean, std) using Xarray and Dask. The notebook works through an example using 0.01 degree resolution, gridded global sea surface temperature data. Mean time series and spatial maps of SST in sub-regions of the mid-latitude eastern Pacific and sub-tropical western Atlantic oceans are computed. The concept of rechunking data to optimize computations is also introduced.
* [general_parallelization.ipynb](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/general_parallelization.ipynb). Demonstrates how to use Dask to parallelize an arbitrary function (e.g. one you've written yourself). Provides an example: coarsening ultra high resolution SST data from 0.01 degree to 1 degree resolution. The notebook also summarizes the results from a cost-performance analysis from running the notebook code on several categories of AWS EC2 instances, which provides guidance to users on instance choice.
