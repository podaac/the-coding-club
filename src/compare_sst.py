import numpy as np
import pandas as pd
import requests

"""
The following routines are used for the SST-comparison project by the PO.DAAC coding club. 

This project explores cloud-native, granule-based analysis of data in the POCLOUD (Earthdata cloud). 

"""

def regrid(data_in, resolution=2):
    """
    Resample the global SST data specified in data_in

    Parameters
    ==========
    data_in: ndarray xarray with dimension (lat, lon)
             Sea surface temperature
    resolution: scalar
             the output resolution, default at 1-degree

    Return
    ======
    data_out: ndarray, xarray
             the resmapled SST at the specified resolution
    """
    
    return data_in.interp(lat=np.arange(-90,90,resolution)).interp(lon=np.arange(-180,180,resolution))



def find_dataset_by_keyword(provider='podaac',
                            keywords=['sst', 'sea surface temperature'],
                            processinglevel=''):
    """
    Construct a CMR query to return collections/datasets that match 
    all the keywords from the keywords list.

    Parameters
    ==========
    provider: string
        the data provider, default is 'podaac'
    keywords: list of strings
        the keywords to search for in the shortname and longname
    processinglevel: int or string, default ''
        the processing level, if not specified will search all levels

    Returns
    =======
    entries_df: pandas dataframe
        the collections resulting from the CMR keyword search
    
    """

    collection_url = 'https://cmr.earthdata.nasa.gov/search/collections'

    if 'podaac' in provider.lower().replace('.',''):
        provider='POCLOUD'

    # handle the case where no processing level is given, so all levels returned
    if processinglevel == '':
        response = requests.get(collection_url,params={'cloud_hosted': 'True',
                                        'has_granules': 'True',
                                        'provider': provider,
                                        'page_size':2000,},
                                headers={'Accept': 'application/json', } )

    else: # provide the processing level specified as a search parameter
        response = requests.get(collection_url,params={'cloud_hosted': 'True',
                                        'has_granules': 'True',
                                        'provider': provider,
                                        'processing_level': processinglevel, 
                                        'page_size':2000,},
                                headers={'Accept': 'application/json', } )
    
    collections = response.json()['feed']['entry']
    

    entries={}
    entries['short_name']=[]
    entries['long_name']=[]
    entries['concept_id']=[]
    entries['processing_level'] =[]
    entries['time_start']=[]
    entries['time_end']=[]
    
    # Loop through results and filter to only those that contain the keywords in the shortname or longname
    for collection in collections:
        
        title="%s %s %s"%(collection["short_name"],collection["dataset_id"][:97],collection["id"])

        match = 1

        for kw in keywords:
            match *= kw.lower() in title.lower()

            if match == 1:
                # if it's the first collection, write it out
                if entries['short_name'] == []:
                    entries['short_name'].append(collection["short_name"])
                    entries['concept_id'].append(collection["id"])
                    entries['long_name'].append(collection["dataset_id"])
                    entries['processing_level'].append(collection["processing_level_id"])
                    entries['time_start'].append(collection["time_start"][:10])
                    try:
                        entries['time_end'].append(collection["time_end"][:10])
                    except:
                        entries['time_end'].append(['NaT/Present'])

                # otherwise check if the collection has already been added based on a previous keyword, if so skip
                elif entries['short_name'][-1] == collection["short_name"]:
                    continue

                else: # if it hasn't been added yet then add to entries
                    entries['short_name'].append(collection["short_name"])
                    entries['concept_id'].append(collection["id"])
                    entries['long_name'].append(collection["dataset_id"])
                    entries['processing_level'].append(collection["processing_level_id"])
                    entries['time_start'].append(collection["time_start"][:10])
                    try:
                        entries['time_end'].append(collection["time_end"][:10])
                    except:
                        entries['time_end'].append(['NaT/Present'])
    
    # return the dataframe of matching results
    entries_df = pd.DataFrame(entries)
    return entries_df