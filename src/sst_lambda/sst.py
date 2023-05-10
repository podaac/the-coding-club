# Imports
import requests
import base64
import s3fs
import boto3
import botocore
import json
import xarray as xr
import numpy as np
# import h5netcdf # don't actually need to import but must be installed


# Constants
S3_ENDPOINT_DICT = {
    'podaac':'https://archive.podaac.earthdata.nasa.gov/s3credentials'
}

# Handle EDL login & S3 credentials
def get_creds(s3_endpoint, edl_username, edl_password):
        """Request and return temporary S3 credentials.
        
        Taken from: https://archive.podaac.earthdata.nasa.gov/s3credentialsREADME
        """
        
        login = requests.get(
            s3_endpoint, allow_redirects=False
        )
        login.raise_for_status()

        auth = f"{edl_username}:{edl_password}"
        encoded_auth  = base64.b64encode(auth.encode('ascii'))

        auth_redirect = requests.post(
            login.headers['location'],
            data = {"credentials": encoded_auth},
            headers= { "Origin": s3_endpoint },
            allow_redirects=False
        )
        auth_redirect.raise_for_status()
        final = requests.get(auth_redirect.headers['location'], allow_redirects=False)
        results = requests.get(s3_endpoint, cookies={'accessToken': final.cookies['accessToken']})
        results.raise_for_status()
        return json.loads(results.content)       
        
def get_temp_creds(prefix):
    # retreive EDL credentials from AWS Parameter Store
    try:
        ssm_client = boto3.client('ssm', region_name="us-west-2")
        edl_username = ssm_client.get_parameter(Name=f"{prefix}-sst-edl-username", WithDecryption=True)["Parameter"]["Value"]
        edl_password = ssm_client.get_parameter(Name=f"{prefix}-sst-edl-password", WithDecryption=True)["Parameter"]["Value"]
        print("Retrieved Earthdata login credentials.")
    except botocore.exceptions.ClientError as error:
        raise error

    # use EDL creds to get AWS S3 Access Keys & Tokens
    s3_creds = get_creds(S3_ENDPOINT_DICT[prefix], edl_username, edl_password)
    print("Retrieved temporary S3 access credentials.")
    
    return s3_creds


# Science functions & lambda handler
def sst_global_mean(data_in):
    """
    Calculate the area-weighted sea surface temperature (sst) global mean

    Parameters
    ==========
    data_in: xarray.Dataset()
            the input dataset

    var_name: string
            the variable to calculate the global mean on
             
    Return
    ======
    data_out: ndarray, xarray
             the global mean for the provided variable
    """
    
    # select the sst variable and select single time
    data_var = data_in.analysed_sst.isel(time=0)

    # convert to degrees Celcius
    data_var = data_var - 273.15

    # create the weights
    weights = np.cos(np.deg2rad(data_var.lat))

    # apply weights to data
    data_weighted = data_var.weighted(weights)

    # calculate the global mean on the weighted data
    global_mean = data_weighted.mean()

    return global_mean
    

def lambda_handler(event, context):
    """Lambda event handler to orchestrate calculation of global mean."""
    
    # --------------------
    # Unpack event payload
    # --------------------

    prefix = event["prefix"]
    #key = event["s3_key"]   # Granule name

    granule_path = event["input_granule_s3path"]
    bucket, key = granule_path.replace("s3://", "").split("/", 1)

    # get the name of the user's output S3 bucket
    output_s3_bucket = event["output_granule_s3bucket"]

    # ---------------------------------------------
    # Read data from Earthdata S3 buckets using EDL
    # ---------------------------------------------

    # Get EDL credentials from AWS Parameter Store
    temp_creds_req = get_temp_creds(prefix)

    # Set up S3 client for Earthdata buckets using EDL creds
    s3_client_in = s3fs.S3FileSystem(
        anon=False, 
        key=temp_creds_req['accessKeyId'], 
        secret=temp_creds_req['secretAccessKey'], 
        token=temp_creds_req['sessionToken']
    )

    # open the granule as an s3 obj
    s3_file_obj = s3_client_in.open(granule_path, mode='rb')

    # -----------------------------------
    # Do science calculations on the data
    # -----------------------------------
        
    # open data in xarray
    ds = xr.open_dataset(s3_file_obj, engine='h5netcdf')

    # process the function
    ds_results = sst_global_mean(ds)
    
    # --------------------------------------------------------------
    # Write results to the user's own S3 bucket for further analysis
    # --------------------------------------------------------------

    # create the temp path for Lambda to write results to locally
    tmp_file_path = '/tmp/' + key[-3] + '_mean.nc'
        
    # write the results to a new netcdf file
    ds_results.to_netcdf(tmp_file_path, mode='w')
    
    # Set up S3 client for user output bucket. 
    # Assumes the IAM role the Lambda function runs as has read/write permission to the bucket
    s3_client_out = s3fs.S3FileSystem(
        anon=False 
    )
    
    # upload the resulting file to s3 bucket
    s3_file_obj_new = s3_client_out.put(tmp_file_path, output_s3_bucket)
    
    # Close dataset and S3 file objects
    ds.close()
    s3_file_obj.close()
    s3_file_obj_new.close()
