# Ancillary notebooks, scripts, and results for `general_parallelization.ipynb`

**Author**: Dean Henze

This directory contains ancillary notebooks, scripts, and results for the `general_parallelization.ipynb` notebook. This primarily includes an analysis to compare the performance of several AWS EC2 instance types running the code from the notebook. The following sections provide an overview of this analysis and its results. A [description of the files in this directory](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/readme.md#directory-contents) are given further below.

## Performance/Cost Assessment of EC2 Types Using Dask

### Background

The computation in `general_parallelization.ipynb` coarsens the MUR (Multiscale Ultrahigh Resolution) SST data product (https://doi.org/10.5067/GHGMR-4FJ04) from 0.01 degree to 1 degree resolution. An example is shown in the below figure. The notebook presents a toy example of processing 10 files but the goal ultimately is to process 100, 1000, 10,000 files. For these larger number of files, computation time and cost become more consequential. The goal of this small assessment is to compare computation times and costs of several EC2 instance types, in order to provide guidance to users in their own computations. 

![example_figure](./example_downscaling.png)

### Analysis

AWS offers hundreds of EC2 instance types, which vary in aspects such as number of processors (vCPU's), memory per processor, and processor type. AWS groups these EC2 types into several general use cases such as "general-purpose", "compute-optimized", "memory-optimized", and "accelerated-computing" (while all of these classes have instances of comparable processor numbers, the classes differ in memory per processor and processor type). For this analysis, an EC2 instance was taken from each of these use-cases: a small instance from the "general purpose" case as a control, and larger instances from the other three case types. The code from `general_parallelization.ipynb` was adapted to an exectuable .py script and run on the EC2 instances for 10, 100, and 1000 files. Computation times are output by the .py script, and costs are derived using computation times and AWS Linux on-demand pricing per hour (pricing table included here). Guidance on running the .py script are given in the [Directory Contents](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/readme.md#directory-contents) section.   

### Results

![results_figure1](./downscale_computation_times.jpg)

![results_figure2](./aws-costs_downscale-comp.jpg)

* Computation times for larger instances reduced computation time of 1000 files from ~8 hrs to ~20 minutes over the small general-purpose instance used as a control.
* It was found that for our computation, each worker (e.g. processor, vCPU) required at least ~6 GB of memory. This limited the maximuim number of vCPUs that could be instantiated, depending on the memory per vCPU of the instance.
* The memory-optimized instances performed the best both in terms of cost and performance. The compute-optimized performed almost as well, and the fact a fewer number of processors could be run (due to lower memory per processor), suggested that these might be better if our computation required less memory per processor.
* The accelerated-computing instance performed the slowest despite costing the most per hour. This demonstrated that these instance types do not necessarily perform the best "out of the package" for an arbitrary task, and require more technical knowledge to utilize.
* Two memory-optimized instances were tested, which were identical other than bandwidth. For these, the computation time did not seem to be affected by larger bandwidth. 

## Directory Contents

* [dscale_mur.py](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/dscale_mur.py) wraps the code from `generalized_parallelization.ipynb` into a script which can be run on an EC2 instance. Example usage:
```
import dscale_s3_dask as dscale
dscale.downscale_with_parallel(n_workers=24, threads_per_worker=2, n_files=100) # n_files is the number of files to process.
```
Where `n_workers` and `threads_per_worker` are passed to an instance of Dask's `Client()`, and `n_files` is the number of MUR files to downscale. Downscaled files are saved to the directory "./sst_downscaled", and computation timing results are saved to a file "computation_results_\<ec2type\>_\<runtime\>.csv", where \<ec2type\> is the instance type, and \<runtime\> is the timestamp when `dscale_mur.py` was run.
* [dscale_computation_results_all.csv](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/dscale_computation_results_all.csv) contains computation timing results from `dscale_mur.py` used in the analysis presented above, combined into a single file.
* [combine_all_results.ipynb](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/combine_all_results.ipynb) can be used as a template for combining timing output files from multiple runs of `dscale_mur.py` (e.g. if you wish to create your own version of `dscale_computation_results_all.csv`).
* [Amazon_EC2_On-Demand_Pricing.csv](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/Amazon_EC2_On-Demand_Pricing.csv) contains EC2 pricing taken from an AWS webpage in summer 2023 (originally hosted [here](https://aws.amazon.com/ec2/pricing/on-demand/)).
* [plot_all_results.ipynb](https://github.com/podaac/the-coding-club/blob/main/notebooks/dask_with_cloud/ancillary/generalized_parallelization/plot_all_results.ipynb) takes data from `dscale_computation_results_all.csv` and `Amazon_EC2_On-Demand_Pricing.csv` to generate the figures in the Results section above. Figures are saved as "downscale_computation_times.jpg" and "aws-costs_downscale-comp.jpg".

## Other Resources

*AWS EC2 instance characteristics:*
* [Tables for memory, bandwith, vCPU count](https://aws.amazon.com/ec2/instance-types/)
* [Tables for CPU cores and threads per core](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/cpu-options-supported-instances-values.html)
* [AWS discussion of CPU options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-optimize-cpu.html)

