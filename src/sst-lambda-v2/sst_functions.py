"""
"""
import json
import base64
import requests
import s3fs
import boto3
import botocore
import xarray as xr
import pandas as pd
import numpy as np

# Constants
S3_ENDPOINT_DICT = {
    'podaac': 'https://archive.podaac.earthdata.nasa.gov/s3credentials'
}


# Handle EDL login & S3 credentials
def get_creds(s3_endpoint, edl_username, edl_password):
    """Request and return temporary S3 credentials.

    Taken from: https://archive.podaac.earthdata.nasa.gov/s3credentialsREADME
    """

    login = requests.get(
        s3_endpoint,
        allow_redirects=False,
        timeout=30
    )
    login.raise_for_status()

    auth = f"{edl_username}:{edl_password}"
    encoded_auth = base64.b64encode(auth.encode('ascii'))

    auth_redirect = requests.post(
        login.headers['location'],
        data={"credentials": encoded_auth},
        headers={"Origin": s3_endpoint},
        allow_redirects=False,
        timeout=30
    )
    auth_redirect.raise_for_status()
    final = requests.get(auth_redirect.headers['location'],
                         allow_redirects=False,
                         timeout=30)
    results = requests.get(s3_endpoint,
                           cookies={'accessToken': final.cookies['accessToken']},
                           timeout=30)
    results.raise_for_status()
    return json.loads(results.content)


def get_temp_creds(prefix):
    """retreive EDL credentials from AWS Parameter Store
    """
    try:
        ssm_client = boto3.client('ssm', region_name="us-west-2")
        edl_username = ssm_client.get_parameter(
            Name=f"{prefix}-sst-edl-username",
            WithDecryption=True)["Parameter"]["Value"]
        edl_password = ssm_client.get_parameter(
            Name=f"{prefix}-sst-edl-password",
            WithDecryption=True)["Parameter"]["Value"]
        print("Retrieved Earthdata login credentials.")
    except botocore.exceptions.ClientError as error:
        raise error

    # use EDL creds to get AWS S3 Access Keys & Tokens
    s3_creds = get_creds(S3_ENDPOINT_DICT[prefix], edl_username, edl_password)
    print("Retrieved temporary S3 access credentials.")

    return s3_creds


def lambda_handler(event, context):
    """Lambda event handler to orchestrate calculation of global mean."""
    # --------------------
    # Unpack event payload
    # --------------------

    prefix = event["prefix"]

    input_granule_path = event["input_granule_s3path"]
    input_bucket, folder, input_key = input_granule_path.replace("s3://", "").split("/", 2)

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
    s3_file_obj = s3_client_in.open(input_granule_path, mode='rb')

    # -----------------------------------
    # Do science calculations on the data
    # -----------------------------------

    # open data in xarray
    ds = xr.open_dataset(s3_file_obj, engine='h5netcdf')

    # process the function
    sst_unpack(ds)

    # Close dataset
    ds.close()

