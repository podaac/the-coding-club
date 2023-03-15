import requests
import s3fs
import xarray as xr
import numpy as np
# import h5netcdf # don't actually need to import but must be installed

s3_cred_endpoint = {
    'podaac':'https://archive.podaac.earthdata.nasa.gov/s3credentials'
}

def get_temp_creds(provider):
    return requests.get(s3_cred_endpoint[provider]).json()

temp_creds_req = get_temp_creds('podaac')

s3_client = s3fs.S3FileSystem(
        anon=False, 
        key=temp_creds_req['accessKeyId'], 
        secret=temp_creds_req['secretAccessKey'], 
        token=temp_creds_req['sessionToken']
    )

def regrid(data_in, resolution=2):
    """
    Resample the global SST data specified in data_in

    Parameters
    ==========
    data_in: ndarray xarray with dimension (lat, lon)
             Sea surface temperature
    resolution: scalar
             the output resolution, default at 1-degree

    Return
    ======
    data_out: ndarray, xarray
             the resmapled SST at the specified resolution
    """
    
    return data_in.interp(lat=np.arange(-90,90,resolution)).interp(lon=np.arange(-180,180,resolution))
    
def lambda_handler(event, context):
    
    key = event["s3_key"]

    # open the granule as an s3 obj
    s3_file_obj = s3_client.open(key, mode='rb')
        
    # open in in xarray
    ds = xr.open_dataset(s3_file_obj, engine='h5netcdf')
        
    # process the function
    ds_results = regrid(ds)
        
    # create the temp path to write results to
    tmp_file_path = '/tmp/' + key[-3] + '_regrid.nc'
        
    # write the results to a new netcdf file
    ds_results.to_netcdf(tmp_file_path, mode='w')
    
    # put the results back in the same bucket
    # result_bucket = 's3://' + bucket + key
    
    # send back to the s3 bucket
    # s3_file_obj_new = s3_client.put(tmp_file_path, result_bucket)
    
    print(ds_results)

