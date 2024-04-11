"""
"""
import os
from io import StringIO

import pandas as pd
import boto3


def lambda_handler_write(event, context):
    """Lambda event handler to write out single point"""
    # --------------------
    # Unpack event payload
    # --------------------

    input_rows = event["input_rows"]
    collection_name = event["collection_name"]

    rows_df = pd.DataFrame.from_dict(input_rows)

    # get the name of the user's output S3 bucket
    output_s3_bucket = event["output_granule_s3bucket"]

    # Set up S3 client for user output bucket.
    s3_out = boto3.client('s3')

    # ------------------------------------------------
    # Write parquet geographic points
    # ------------------------------------------------

    for i, row in rows_df.iterrows():

        pid = row['point_id']
        ptime = row['time']

        output_key = collection_name + '/geo_points/' + str(pid) + '/' + str(ptime) + '.parquet'

        # create the temp path for Lambda to write results to locally
        tmp_file_path = '/tmp/' + output_key

        if not os.path.exists('/tmp/' + collection_name + '/geo_points/' + str(pid) + '/'):
            print('creating directory: ' + '/tmp/' + collection_name + '/geo_points/' + str(pid) + '/')
            os.makedirs('/tmp/' + collection_name + '/geo_points/' + str(pid) + '/')

        # write the results to a parquet file
        try:
            print('writing file to tmp: ' + tmp_file_path)
            out_row = row.to_frame().T
            out_row.to_parquet(tmp_file_path)
        except Exception as e:
            print("Problem writing to tmp: " + str(e))

        s3_out.upload_file(tmp_file_path, output_s3_bucket, output_key)

        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
