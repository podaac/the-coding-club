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
