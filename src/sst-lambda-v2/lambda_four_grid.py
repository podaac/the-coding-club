"""
"""
import os
import boto3
import pandas as pd
import xarray as xr
import numpy as np


def lambda_handler_aggregate_grid(event, context):
    """
    Lambda event handler to aggregate pixel statistics 
    back into grid.
    """
    # --------------------
    # Unpack event payload
    # --------------------
    input_granule_path = event["input_granule_s3path"]

    # get the name of the user's output S3 bucket
    output_s3_bucket = event["output_granule_s3bucket"]

    # ---------------------------------------------
    # Read intermediate data from user S3 bucket
    # ---------------------------------------------

    # Set up S3 client for user output bucket.
    s3 = boto3.client('s3')

    # open the granule as an s3 obj
    s3_file_obj = s3.open(input_granule_path, mode='rb')

    # ------------------------------------------------
    # Explode the nc file to parquet geographic points
    # ------------------------------------------------

    # open data in xarray
    df = pd.read_parquet(s3_file_obj)

    # --------------------
    # rebuild grid
    # --------------------

    grid_pairs = [(x, y)
                  for x in pd.unique(df['lats'])
                  for y in pd.unique(df['lons'])
                  ]

    tmp_grid = np.array(grid_pairs)
    full_grid = pd.DataFrame({'lats': tmp_grid[:, 0], 'lons': tmp_grid[:, 1]})
    full_grid = full_grid.sort_values(by=['lats', 'lons'])
    full_grid = full_grid.reset_index(drop=True)

    data_onto_full_grid = pd.merge(full_grid, df, how='left')

    # --------------------
    # build xarray dataset
    # --------------------

    out_lat = pd.unique(data_onto_full_grid['lats'])
    out_lon = pd.unique(data_onto_full_grid['lons'])

    sum_2d = data_onto_full_grid['sum'].values.reshape(
        len(pd.unique(data_onto_full_grid['lats'])),
        len(pd.unique(data_onto_full_grid['lons']))
        )
    sum_xr = xr.DataArray(
        sum_2d,
        coords=[('lat', out_lat), ('lon', out_lon)])
    sum_xr = sum_xr.rename("sum")

    mean_2d = data_onto_full_grid['mean'].values.reshape(
        len(pd.unique(data_onto_full_grid['lats'])),
        len(pd.unique(data_onto_full_grid['lons']))
        )
    mean_xr = xr.DataArray(
        mean_2d,
        coords=[('lat', out_lat), ('lon', out_lon)])
    mean_xr = mean_xr.rename("mean")

    var_2d = data_onto_full_grid['variance'].values.reshape(
        len(pd.unique(data_onto_full_grid['lats'])),
        len(pd.unique(data_onto_full_grid['lons']))
        )
    var_xr = xr.DataArray(
        var_2d,
        coords=[('lat', out_lat), ('lon', out_lon)])
    var_xr = var_xr.rename("var")

    std_2d = data_onto_full_grid['standard_dev'].values.reshape(
        len(pd.unique(data_onto_full_grid['lats'])),
        len(pd.unique(data_onto_full_grid['lons']))
        )
    std_xr = xr.DataArray(
        std_2d,
        coords=[('lat', out_lat), ('lon', out_lon)])
    std_xr = sum_xr.rename("std")

    ds = xr.Dataset(

        data_vars={
            "sum": sum_xr,
            "mean": mean_xr,
            "variance": var_xr,
            "standard_dev": std_xr}
    )

    output_key = 'result_statistics_gridded.nc'

    # create the temp path for Lambda to write results to locally
    tmp_file_path = '/tmp/' + output_key

    # write the results to a parquet file
    try:
        ds.to_netcdf(tmp_file_path)
    except Exception as e:
        print("Problem writing to tmp: " + str(e))

    s3.upload_file(tmp_file_path, output_s3_bucket, output_key)

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)
