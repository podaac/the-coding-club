"""
"""
import os
import s3fs
import boto3
import xarray as xr
import pandas as pd
import numpy as np

import sst_functions


def convert_to_dataframe(data_in):
    """
    Convert data from xarray Dataset to Pandas Dataframe,
    formatted to be written as parquet

    Parameters
    ==========
    data_in: xarray.Dataset()
        the input dataset

    Returns
    =======
    df: pandas.DataFrame()
        the parquet-formatted dataframe

    """

    time = str(data_in.time.values[0])

    lats = data_in.lat.values
    lons = data_in.lon.values

    sst = data_in['analysed_sst'][0, :, :].values
    sst_anom = data_in['sst_anomaly'][0, :, :].values

    data_sst = sst.reshape(-1)
    data_sst_anom = sst_anom.reshape(-1)

    Y, X = np.unravel_index(range(sst.size), sst.shape)

    num_points = len(data_sst)
    point_id_list = [i for i in range(num_points)]

    time_list = [time for _ in range(num_points)]

    lat_value_list = [lats[idx] for idx in Y]
    lon_value_list = [lons[idx] for idx in X]

    # ---------------------------------
    # create pandas dataframe structure 
    # ---------------------------------

    columns = ["time",
               "point_id",
               "Y",
               "X",
               "lats",
               "lons",
               "analysed_sst",
               "sst_anomaly"]

    df = pd.DataFrame(columns=columns)

    tuple_list = list(zip(time_list,
                          point_id_list,
                          Y,
                          X,
                          lat_value_list,
                          lon_value_list,
                          data_sst,
                          data_sst_anom))

    # Add data to the output dataframe
    new_data = pd.DataFrame(tuple_list, columns=columns)

    df = pd.concat([df, new_data])

    return df


def lambda_handler_explode(event, context):
    """Lambda event handler to orchestrate calculation of global mean."""
    # --------------------
    # Unpack event payload
    # --------------------

    prefix = event["prefix"]

    input_granule_path = event["input_granule_s3path"]

    # get the name of the user's output S3 bucket
    output_s3_bucket = event["output_granule_s3bucket"]

    # ---------------------------------------------
    # Read data from Earthdata S3 buckets using EDL
    # ---------------------------------------------

    # Get EDL credentials from AWS Parameter Store
    temp_creds_req = sst_functions.get_temp_creds(prefix)

    # Set up S3 client for Earthdata buckets using EDL creds
    s3_client_in = s3fs.S3FileSystem(
        anon=False,
        key=temp_creds_req['accessKeyId'],
        secret=temp_creds_req['secretAccessKey'],
        token=temp_creds_req['sessionToken']
    )

    # open the granule as an s3 obj
    s3_file_obj = s3_client_in.open(input_granule_path, mode='rb')

    # Set up S3 client for user output bucket.  
    s3_out = boto3.client('s3')

    # ------------------------------------------------
    # Explode the nc file to parquet geographic points
    # ------------------------------------------------

    # open data in xarray
    ds = xr.open_dataset(s3_file_obj, engine='h5netcdf')

    sst_df = convert_to_dataframe(ds)

    for i in range(sst_df.shape[0]):
        row = sst_df[i:i+1]

        pid = row['point_id'][i]
        ptime = row['time'][i]

        output_key = str(pid) + '/' + str(ptime) + '.parquet'

        # create the temp path for Lambda to write results to locally
        tmp_file_path = '/tmp/' + output_key

        # write the results to a parquet file
        try:
            row.to_parquet(tmp_file_path, mode='w')
        except Exception as e:
            print("Problem writing to tmp: " + e)

        s3_out.upload_file(tmp_file_path, output_s3_bucket, output_key)

        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
