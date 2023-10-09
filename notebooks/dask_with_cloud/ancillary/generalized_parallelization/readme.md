# Ancillary notebooks, scripts, and results for general_parallelization.ipynb

**Author**: Dean Henze

This directory contains ancillary notebooks, scripts, and results for the general_parallelization.ipynb notebook. This primarily includes an anaylsis to compare the performance of several AWS EC2 instance types running the code from the notebook.

## Performance/Cost Assessment of EC2 Types Using Dask

**Background**

The ability to perform scientific analyses on increasingly large data sets (comprised of either large data files, many data files, or both) is a key target of computing in the cloud, since the necessary computing resources can be utilized by anyone. In AWS, EC2 instances characteristics relevant to parallel computing include:
* Number of CPU cores
* Threads (or vCPUs) per core
* Memory per vCPU (perhaps more relevant than total memory, for parallel computing?)

The goal of this analysis is to assess performance and cost differences between EC2 instances which vary these characteristics.

**Computation and Dataset**

The computation is a coarsening of the MUR SST data product (https://doi.org/10.5067/GHGMR-4FJ04) from 0.01 degree to 1 degree resolution, an example shown below.

![example_figure](./example_downscaling.png)

**Directory contents**

`dscale_s3_dask.ipynb` walks through downscaling 10 MUR 1 km files via S3 connection, comparing computation times with and without dask. In summary, it takes half the time to downscale the files when using two dask workers, as expected.

`dscale_s3_dask.py` generalizes the code in `dscale_s3_dask.ipynb` to make it easier to plug and play on any EC2 instance. It has a callable function to set parallel computing parameters and number of files analyzed, saving the downscaled files to `./sst_downscaled`. Example usage:
```
import dscale_s3_dask as dscale
dscale.downscale_with_parallel(n_workers=24, threads_per_worker=2, n_files=100) # n_files is the number of files to process.
```

**Preliminary Results**

* Main factor in decreasing time for this computation is the product number_of_workers x threads_per_worker. 
* Although the same computation time results from using 24 workers with 2 threads each vs. 48 workers with 1 thread each (above bullet), the former does not produce any memory warnings.
* In a test comparing two EC2 instances that were identical other than bandwidth, the computation time did not seem to be affected by larger bandwidth. 
 

**Further Resources**

*AWS EC2 instance characteristics:*
* [Tables for memory, bandwith, vCPU count](https://aws.amazon.com/ec2/instance-types/)
* [Tables for CPU cores and threads per core](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/cpu-options-supported-instances-values.html)
* [AWS discussion of CPU options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html)

