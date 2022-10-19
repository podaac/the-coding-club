# Script to generate S3 lists for a collection shortname and temporal range.
#
# Command line arguments:
# -s: short name of the collection
# -t: temporal range to retrieve S3 URIs
# -d: Directory to save S3 URI list to.
#
# Example: python3 S3List_run.py -s AMSR2-REMSS-L2P-v8a -t 2022-07-18T00:00:00Z,2022-07-18T23:59:59Z -d /Users/username/sst-hackathon/s3_lists
#
# Author: nicole.tebaldi@jpl.nasa.gov
# Date Created: 20221014

# Standard imports
import argparse
from datetime import datetime
import json
from pathlib import Path
from socket import gethostname, gethostbyname

# Local imports
from S3List import S3List

def create_args():
    """Create and return argparser with arguments."""

    arg_parser = argparse.ArgumentParser(description="Retrieve a list of S3 URIs")
    arg_parser.add_argument("-d",
                            "--directory",
                            type=str,
                            help="Directory to save S3 list to")
    arg_parser.add_argument("-s",
                            "--shortname",
                            type=str,
                            help="The collection shortname")
    arg_parser.add_argument("-t",
                            "--temporalrange",
                            type=str,
                            help="Temporal range to retrieve URIs for")
    return arg_parser

def generate_lists(short_name, temporal_range, list_dir):
    """ Generate a list of S3 URIs for a collection and save to list directory.
    
    Assumes temporal_range format: 
    "{YYYY}-{MM}-{DD}T-{HH}:{MM}:{SS}Z,{YYYY}-{MM}-{DD}T-{HH}:{MM}:{SS}Z"
    Example: "2022-07-18T00:00:00Z,2022-07-18T23:59:59Z"

    Attributes
    ----------
    short_name: str
        String short name of the collection
    temporal_range: str
        Temporal range to retreive data for.
    """

    start = datetime.now()

    # Download object
    s3list = S3List()

    try:

        # Login and retrieve token
        print("Login and retrieve token.")
        s3list.login()
        client_id = "podaac_cmr_client"
        hostname = gethostname()
        ip_addr = gethostbyname(hostname)
        s3list.get_token(client_id, ip_addr)

        # Run query
        print("Run query.")
        provider = "POCLOUD"
        s3_urls = s3list.run_query(short_name, provider, temporal_range)
        s3_urls.sort()

        # Save list of downloads as JSON
        list_file = Path(list_dir).joinpath(f"{short_name}_s3_list.json")
        with open(str(list_file), 'w') as jf:
            json.dump(s3_urls, jf, indent=2)

        # Clean up and delete token
        print("Attempting to delete token.")
        status = s3list.delete_token()
        if status == 204: 
            print("Token deleted.")

    except Exception as e:
        print(f"ERROR: {e}")
        print("Exiting program.")

    end = datetime.now()
    print(f"Total execution time: {end - start}.")

def run_list_generation():

    # Command line arguments
    arg_parser = create_args()
    args = arg_parser.parse_args()

    # Generate list
    generate_lists(args.shortname, args.temporalrange, args.directory)

if __name__ == "__main__":
    run_list_generation()