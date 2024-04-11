"""
"""
import os
import boto3
import pandas as pd
import numpy as np
import awswrangler as wr


def lambda_handler_statistics(event, context):
    """
    Lambda event handler to orchestrate calculation 
    of various statistics in time.
    """
    # --------------------
    # Unpack event payload
    # --------------------
    input_path = event["input_s3path"]
    collection_name = event["collection_name"]

    # get the name of the user's output S3 bucket
    output_s3_bucket = event["output_s3bucket"]

    # ---------------------------------------------
    # Read intermediate data from user S3 bucket
    # ---------------------------------------------

    # Set up S3 client for user output bucket.
    s3 = boto3.client('s3')

    # open data in pandas
    df = wr.s3.read_parquet(path=input_path)

    # --------------------
    # calculate statistics
    # --------------------

    results = df.iloc[0, 1:6]

    col_list_to_calc = ['analysed_sst']

    results['sum'] = df[col_list_to_calc].sum(skipna=True).values[0]
    results['mean'] = df[col_list_to_calc].mean(skipna=True).values[0]
    results['variance'] = df[col_list_to_calc].var(skipna=True).values[0]
    results['standard_dev'] = df[col_list_to_calc].std(skipna=True).values[0]

    if results['sum'] == 0:
        results['sum'] = np.nan

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

    output_key = collection_name + '/result_statistics/' + str(pid) + '_result_statistics.parquet'

    # create the temp path for Lambda to write results to locally
    tmp_file_path = '/tmp/' + output_key

    if not os.path.exists('/tmp/' + collection_name + '/result_statistics/'):
        print('creating directory: ' + '/tmp/' + collection_name + '/result_statistics/')
        os.makedirs('/tmp/' + collection_name + '/result_statistics/')

    # write the results to a parquet file
    try:
        print('writing tmp file: ' + tmp_file_path)
        output.to_parquet(tmp_file_path, object_encoding='infer', engine='fastparquet')
    except Exception as e:
        print("Problem writing to tmp: " + str(e))

    s3.upload_file(tmp_file_path, output_s3_bucket, output_key)

    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)
