# Dask for Parallelized Analysis of NASA Earthdata in the Cloud

Included here are a collection of notebooks which demonstrate Dask (Python package) for parallel computing in the cloud using AWS resources and Earth data hosted by NASA. They are meant to be both pedagogical and serve as a quick reference/refresher, but do assume some prerequisite knowledge.

## Parallel Computing, the Cloud, and Dask

Tersely, parallel computing is a method which 
1. Allows computation of data which is larger than the RAM of a single machine. For example, the execution of a block of code (say, for a scientific analysis), can be assigned to processors across multiple machines, allowing the memory requirements to be shared among them.
2. Allows some computations to be run faster than they normally would. For example, the Macbook Pro being used to write this readme file technically has 10 processors, but normal execution of Python code will not utilized these processors in parallel (e.g. split up the work to be done across the processors simultaneously). Parallel processing allows for this.
   
A slightly more comprehensive introduction to these concepts can be found elsewhere, e.g. [this page on Pythia](https://earth-env-data-science.github.io/lectures/dask/intro.html)

## Prerequisites
* Python coding experience. A basic familiarity is required, but more experience will make working with Dask easier. Many key packages for scientific analysis (e.g. Xarray, NumPy) work with Dask only if the proper syntax is used, which will likely be familiar to those who have already worked with these packages. However, this should not deter you from jumping in!
* Ability to start a virtual machine (VM) in AWS. All notebooks here assume that you are in a VM in AWS, and will not work unless you are. Whether you start

## Other Resources
* Pythia
* Pangeo
* Dask docs
