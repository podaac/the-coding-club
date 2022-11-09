# Class used to generate lists of S3 URIs.
#
# Date Created: 20221014

# Standard imports
from http.cookiejar import CookieJar
import netrc
from socket import gethostname, gethostbyname
from urllib import request

# Third-party imports
import requests
import json
from pathlib import Path

class CMRQuery:
    """Class used to query and download from PO.DAAC's CMR API.
    """

    CMR = "cmr.earthdata.nasa.gov"
    URS = "urs.earthdata.nasa.gov"

    def __init__(self):
        self._token = None

    def login(self):
        """Log into Earthdata and set up request library to track cookies.
        
        Raises an exception if can't authenticate with .netrc file.
        """

        try:
            username, _, password = netrc.netrc().authenticators(self.URS)
        except (FileNotFoundError, TypeError):
            raise Exception("ERROR: There not .netrc file or endpoint indicated in .netrc file.")

        # Create Earthdata authentication request
        manager = request.HTTPPasswordMgrWithDefaultRealm()
        manager.add_password(None, self.URS, username, password)
        auth = request.HTTPBasicAuthHandler(manager)

        # Set up the storage of cookies
        jar = CookieJar()
        processor = request.HTTPCookieProcessor(jar)

        # Define an opener to handle fetching auth request
        opener = request.build_opener(auth, processor)
        request.install_opener(opener)

    def get_token(self, client_id, ip_address):
        """Get CMR authentication token for searching records.
        
        Parameters
        ----------
        client_id: str
            client identifier to obtain token
        ip_address: str
            client's IP address
        """

        try:
            username, _, password = netrc.netrc().authenticators(self.URS)
        except (FileNotFoundError, TypeError) as error:
            raise Exception("ERROR: There not .netrc file or endpoint indicated in .netrc file.")

        # Post a token request and return resonse
        token_url = f"https://{self.CMR}/legacy-services/rest/tokens"
        token_xml = (f"<token>"
                        f"<username>{username}</username>"
                        f"<password>{password}</password>"
                        f"<client_id>{client_id}</client_id>"
                        f"<user_ip_address>{ip_address}</user_ip_address>"
                    f"</token>")
        headers = {"Content-Type" : "application/xml", "Accept" : "application/json"}
        self._token = requests.post(url=token_url, data=token_xml, headers=headers) \
            .json()["token"]["id"]

    def delete_token(self):
        """Delete CMR authentication token."""

        token_url = f"https://{self.CMR}/legacy-services/rest/tokens"
        headers = {"Content-Type" : "application/xml", "Accept" : "application/json"}
        try:
            res = requests.request("DELETE", f"{token_url}/{self._token}", headers=headers)
            return res.status_code
        except Exception as e:
            raise Exception(f"Failed to delete token: {e}.")


    def query_collections_by_keyword(self, provider, keywords, processinglevel=''):
        """Run query on collection referenced by keywords."""

        url = f"https://{self.CMR}/search/collections.umm_json"
        if processinglevel == '':
            params = {
                    "cloud_hosted": "True",
                    "provider" : provider, 
                    "has_granules": "True",
                    "token" : self._token,
                    "scroll" : "true",
                    "page_size" : 2000,
                }
        else:
            params = {
                    "cloud_hosted": "True",
                    "provider" : provider, 
                    "processing_level": processinglevel,
                    "has_granules": "True",
                    "token" : self._token,
                    "scroll" : "true",
                    "page_size" : 2000,
                }
        
        shortnames = []

        response = requests.get(url=url, params=params)   

        json_file = Path('/Users/vmcdonal/s3_lists').joinpath("s3_list.json")
        print(f"Saving list as JSON file: {str(json_file)}")
        with open(json_file, 'w') as jf:
            json.dump(response.json(), jf, indent=2) 

        collections = response.json()['items']

        for coll in collections:

            title="%s %s"%(coll["umm"]["ShortName"],coll["umm"]["EntryTitle"])

            match = 1

            for kw in keywords:
                match *= kw.lower() in title.lower()

                if match == 1:

                    # if it's the first collection, write it out
                    if shortnames == []:
                        shortnames.append(coll["umm"]["ShortName"])
                
                    # otherwise check if the collection has already been added based on a previous keyword, if so skip
                    elif coll["umm"]["ShortName"] in shortnames:
                        continue
                    
                    # if it hasn't been added yet then add to the list
                    else:
                        shortnames.append(coll["umm"]["ShortName"])

        return shortnames
    
    
    def query_granules_by_shortname(self, shortnames, provider, temporal_range):
        """Run query on collection referenced by shortname from provider."""

        granule_urls = []

        url = f"https://{self.CMR}/search/granules.umm_json"
        
        # if just one shortname provided
        if isinstance(shortnames, str):
            params = {
                    "provider" : provider, 
                    "ShortName" : shortnames, 
                    "token" : self._token,
                    "scroll" : "true",
                    "page_size" : 2000,
                    "sort_key" : "start_date",
                    "temporal" : temporal_range
                }

            res = requests.get(url=url, params=params)        
            coll = res.json()
        
            granule_urls.append([url["URL"] for res in coll["items"] for url in res["umm"]["RelatedUrls"] if url["Type"] == "GET DATA VIA DIRECT ACCESS"])
        
        else:
            for shortname in shortnames:
                params = {
                    "provider" : provider, 
                    "ShortName" : shortname, 
                    "token" : self._token,
                    "scroll" : "true",
                    "page_size" : 2000,
                    "sort_key" : "start_date",
                    "temporal" : temporal_range
                }

                res = requests.get(url=url, params=params)        
                coll = res.json()
        
                granule_urls.append([url["URL"] for res in coll["items"] for url in res["umm"]["RelatedUrls"] if url["Type"] == "GET DATA VIA DIRECT ACCESS"])
        
        return granule_urls


    def login_and_run_query(self, short_name, provider, temporal_range):
        """Log into CMR and run query to retrieve a list of S3 URLs."""

        try:
            # Login and retrieve token
            self.login()
            client_id = "podaac_cmr_client"
            hostname = gethostname()
            ip_addr = gethostbyname(hostname)
            self.get_token(client_id, ip_addr)

            # Run query
            s3_urls = self.query_granule_by_shortname(short_name, provider, temporal_range)
            s3_urls.sort()

            # Clean up and delete token
            self.delete_token()            
        except Exception:
            raise
        else:
            # Return list
            return s3_urls