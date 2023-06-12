# Performance/Cost Assessment of EC2 Types Using Dask
This directory contains notebooks, scripts, and key results from an anaylsis to compare the performance of several AWS EC2 instance types utilizing Dask parallel computing to perform an earth science-relevant computation.

**Background**
The ability to perform scientific analyses on increasingly large data sets (comprised of either large data files, many data files, or both) is a key target of computing in the cloud, since the necessary computing resources can be utilized by anyone. In AWS, EC2 instances characteristics relevant to parallel computing include:
* Number of vCPUs
* Number of CPU cores
* Memory per vCPU (perhaps more relevant than total memory, for parallel computing)
* Threads per core

**Computation and Dataset**
The computation is a downscaling of a MUR 1 km SST data product (https://doi.org/10.5067/GHGMR-4FJ04) to 100 km resolution.

![example_figure](./example_downscaling.png)
**Figure 1. Example results of downscaling a MUR 1 km SST product**
