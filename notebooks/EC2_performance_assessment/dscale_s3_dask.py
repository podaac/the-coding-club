"""
This script is to be run on an AWS EC2 instance. Additionally, to access Earthdata S3 buckets, 
credentials must be placed in a .netrc file, e.g.:

machine urs.earthdata.nasa.gov
    login <Earthdata username>
    password <Earthdata password>
    
where the <Earthdata username> and <Earthdata password> are your login credentials.
"""


import gc
import os
import time

import s3fs
import requests

import xarray as xr
#import h5py
import numpy as np
import pandas as pd

import dask
import dask.array as da
from dask.distributed import Client, LocalCluster, progress
from dask import delayed
import multiprocessing



def init_S3FileSystem():
    """
    This routine automatically pulls your EDL crediential from .netrc file and use it 
    to obtain a temporary AWS S3 credential through a podaac service accessable at 
    https://archive.podaac.earthdata.nasa.gov/s3credentials
    
    Return:
    =======
    s3: an AWS S3 filesystem
    """
    import requests, s3fs
    creds = requests.get('https://archive.podaac.earthdata.nasa.gov/s3credentials').json()
    s3 = s3fs.S3FileSystem(anon=False,
                           key=creds['accessKeyId'],
                           secret=creds['secretAccessKey'], 
                           token=creds['sessionToken'],
                           client_kwargs={'region_name':'us-west-2'})
    return s3



def downscale_xr_s3(fs_s3, filepath_s3, output_dir, chunks=None):
    """
    Open and downscale SST's from 1 km to 100 km from a MUR 1 km file on an S3 bucket. fs_s3 is the 
    S3 file system and filepath_s3 is the MUR filepath on S3. output_dir is the directory to save 
    the downscaled data file in.
    """
    
    print('Opening ', filepath_s3)
    s3_file_obj = fs_s3.open(filepath_s3, mode='rb')
    sstdata = xr.open_dataset(s3_file_obj, chunks=chunks)
    
    def downscale_mursst(sst):
        """
        This function takes MUR SST 1km data (with dimensions of 17900x36000), reshapes, and 
        computes the mean temperature in 1x1 degree boxes, and then returns the processed 
        SST data (shape 180x360).

        Parameters
        ----------
        sst: 2D array-like of sea surface temperatures.
        """
        sst0 = np.r_[sst[0:1, :], sst]; del sst
        sst = sst0.reshape(180, 100, 360, 100).mean(axis=-1).mean(axis=1); del sst0
        return sst
    
    print("Downscaling.")
    sst_downscaled = downscale_mursst(sstdata['analysed_sst'][0, ...])
    
    # Save downscaled SST to .nc file:
    print("Saving output.")
    ds = xr.Dataset(
        data_vars=dict(
            sst=(["time", "lat", "lon"], np.expand_dims(sst_downscaled, axis=0)) # Add dim for time.
            ),
        coords=dict(
            lon=sstdata['lon'].values[::100], # lons, lats in downscaled res.
            lat=sstdata['lat'].values[::100],
            time=sstdata["time"].values,
            ),
        attrs=dict(
            description="SST downscaled from MUR 1 km file to 100 km resolution.",
            units="K",
            ),
        )
    ds.to_netcdf(output_dir + filepath_s3.split("/")[-1][:-3] + "_downscaled.nc")
    
    sstdata.close()
    


@dask.delayed
def downscale_xr_s3_dd(fs_s3, filepath_s3, output_dir, chunks=None):
    """
    Open and downscale SST's from 1 km to 100 km from a MUR 1 km file on an S3 bucket. fs_s3 is the 
    S3 file system and filepath_s3 is the MUR filepath on S3. output_dir is the directory to save 
    the downscaled data file in.
    """
    
    print('Opening ', filepath_s3)
    s3_file_obj = fs_s3.open(filepath_s3, mode='rb')
    sstdata = xr.open_dataset(s3_file_obj, chunks=chunks)
    
    def downscale_mursst(sst):
        """
        This function takes MUR SST 1km data (with dimensions of 17900x36000), reshapes, and 
        computes the mean temperature in 1x1 degree boxes, and then returns the processed 
        SST data (shape 180x360).

        Parameters
        ----------
        sst: 2D array-like of sea surface temperatures.
        """
        sst0 = np.r_[sst[0:1, :], sst]; del sst
        sst = sst0.reshape(180, 100, 360, 100).mean(axis=-1).mean(axis=1); del sst0
        return sst
    
    print("Downscaling.")
    sst_downscaled = downscale_mursst(sstdata['analysed_sst'][0, ...])
    
    # Save downscaled SST to .nc file:
    print("Saving output.")
    ds = xr.Dataset(
        data_vars=dict(
            sst=(["time", "lat", "lon"], np.expand_dims(sst_downscaled, axis=0)) # Add dim for time.
            ),
        coords=dict(
            lon=sstdata['lon'].values[::100], # lons, lats in downscaled res.
            lat=sstdata['lat'].values[::100],
            time=sstdata["time"].values,
            ),
        attrs=dict(
            description="SST downscaled from MUR 1 km file to 100 km resolution.",
            units="K",
            ),
        )
    ds.to_netcdf(output_dir + filepath_s3.split("/")[-1][:-3] + "_downscaled.nc")
    
    sstdata.close()
    
    
    
if __name__=="__main__":
    
    # Get temporary AWS credentials for access
    fs_s3 = init_S3FileSystem()
    
    # File paths of all MUR granules:
    s3path = "s3://podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1/"
    fns = fs_s3.glob(s3path+"*.nc")
    print("total granules = ",len(fns))
    print("Example filename: ", fns[0])
    
    # Directory to place downscaled files in:
    if not os.path.isdir("./sst_downscaled/"):
        os.mkdir("./sst_downscaled/")
    
    # Test downscaling one file:
    #downscale_xr_s3(fs_s3, fns[0], "./sst_downscaled/", chunks=None)
    
    # Start dask client:
    n_workers = multiprocessing.cpu_count()
    print(n_workers)
    
    client = Client(n_workers=int(n_workers/2), threads_per_worker=1)
    print(client)
    
    # Run downscaling tasks using dask delayed:
    dscale_tasks = []
    chunks = {'time':1, 'lat':int(17999/3), 'lon':int(36000/3)}
    for i in range(100):
        dscale_tasks.append(downscale_xr_s3_dd(fs_s3, fns[i], "./sst_downscaled/", chunks=None))
    print(dscale_tasks)
    
        # time the computation:
    tick = time.time()
    _ = da.compute(*dscale_tasks)
    tock = time.time()
    print("Total computation time =", str(tock-tick), "seconds.")
    
    client.close()