# Class used to generate lists of S3 URIs.
#
# Author: nicole.tebaldi@jpl.nasa.gov
# Date Created: 20221014

# Standard imports
from http.cookiejar import CookieJar
import netrc
import requests
from urllib import request

class S3List:
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

    def run_query(self, shortname, provider, temporal_range):
        """Run query on collection referenced by shortname from provider."""

        url = f"https://{self.CMR}/search/granules.umm_json"
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
        return [url["URL"] for res in coll["items"] for url in res["umm"]["RelatedUrls"] if url["Type"] == "GET DATA VIA DIRECT ACCESS"]