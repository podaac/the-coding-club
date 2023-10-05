# Dask for Parallelized Analysis of NASA Earthdata in the Cloud

Included here are a collection of notebooks which demonstrate Dask (Python package) for parallel computing in the cloud using AWS resources and Earth data hosted by NASA. They are meant to be both pedagogical and serve as a quick reference/refresher, but do assume some prerequisite knowledge.

## Parallel Computing and Dask
Tersely, parallel computing is a method which:
1. Allows computation of data which is larger than the RAM of a single machine. For example, execution of a block of code can be assigned to processors across multiple machines, allowing the memory requirements to be shared among them.
2. Can make certain computations run faster. For example, the Macbook used to write this readme file has 10 processors, but normal execution of Python code will not utilized the processors in parallel (e.g. split up the work across the processors simultaneously). Parallel processing allows for this.

Dask is a Python package which will let your code utilize parallel processing in your .py and .ipynb files. 

A slightly more comprehensive introduction to these concepts can be found elsewhere, e.g. [this page on Pythia](https://earth-env-data-science.github.io/lectures/dask/intro.html)

## Prerequisites
* **Basic knowledge of what the Cloud is**, and accessing NASA Earthdata on the Cloud. If not, checkout the [NASA Earthdata Cloud Cookbook](https://nasa-openscapes.github.io/earthdata-cloud-cookbook/).
* **Some Python coding experience**. Basic familiarity is required, but more experience will make working with Dask easier. Many key packages for scientific analysis (e.g. Xarray, NumPy) work with Dask only if the proper syntax is used, which will likely be familiar to those who have already worked with them. However, don't let this stop you from jumping in!
* **Ability to start a virtual machine (VM) in AWS. All notebooks here assume that you are in a VM in AWS, and will not work unless you are**. E.g. you can spin up your own EC2 instance, use a Cloud Playground service, or try out [Coiled](https://www.coiled.io) (very useful, but does charge a fee).

## Other Resources
* Pythia
* Pangeo
* Dask docs
