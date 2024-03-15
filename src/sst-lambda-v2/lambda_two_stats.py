"""
"""
import os
import boto3
import pandas as pd


def lambda_handler_statistics(event, context):
    """
    Lambda event handler to orchestrate calculation 
    of various statistics in time.
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
    # calculate statistics
    # --------------------

    results = df.iloc[0, 1:6]

    col_list_to_calc = ['analysed_sst']

    results['sum'] = df[col_list_to_calc].sum().values[0]
    results['mean'] = df[col_list_to_calc].mean().values[0]
    results['variance'] = df[col_list_to_calc].var().values[0]
    results['standard_dev'] = df[col_list_to_calc].std().values[0]

    COLUMNS = [
        "point_id", "Y", "X", "lats", "lons",
        "sum", "mean", "variance", "standard_dev"]

    tuple_list = [[
        results['point_id'],
        results['Y'], results['X'], results['lats'], results['lons'],
        results['sum'], results['mean'],
        results['variance'], results['standard_dev']]]

    # Add data to the output dataframe
    output = pd.DataFrame(tuple_list, columns=COLUMNS)

    # -----------------
    # write out results
    # -----------------

    pid = results['point_id']

    output_key = 'result_statistics/' + str(pid) + '_result_statistics.parquet'

    # create the temp path for Lambda to write results to locally
    tmp_file_path = '/tmp/' + output_key

    # write the results to a parquet file
    try:
        output.to_parquet(tmp_file_path, mode='w')
    except Exception as e:
        print("Problem writing to tmp: " + e)

    s3.upload_file(tmp_file_path, output_s3_bucket, output_key)

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)
