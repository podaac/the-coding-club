import os
from io import BytesIO
from skimage import io
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import urllib.request
import urllib.parse
import urllib
import mapbox_vector_tile
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
from PIL import Image as plimg
import numpy as np
from owslib.wms import WebMapService
from IPython.display import Image, display

import matplotlib.image as mpimg

img_bg = mpimg.imread('darkrift-orig_full.png')
img_podaac = mpimg.imread('podaac_logo_B_color.png')
img_nasa = mpimg.imread('nasa_jpl_logo_0.png')

def setup_bg():
    ax = plt.axes([0, 0, 1, 1])
    ax.patch.set_alpha(0.8)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()
    ax.imshow(img_bg,aspect='auto',zorder=0)
    return

def setup_logo():
    ax = plt.axes([0.85, 0.01, 0.1, 0.1])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()
    ax.imshow(img_nasa)

    ax = plt.axes([0.91, 0.01, 0.1, 0.1])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_axis_off()
    ax.imshow(img_podaac)
    return

def setup_caption(date_str):
    plt.figtext(0.03, 0.5, "SMAP RSS Sea Surface Salinity 8-day Running Average V5.0", fontsize=19, fontweight="bold", ha='center',va='center',color='w', rotation=90)
    plt.figtext(0.07, 0.5, "(2015-2022)", fontsize=28, fontweight="bold", ha='center',va='center',color='w', rotation=90)

    plt.figtext( 0.89, 0.95, date_str,fontsize=35,fontweight='bold', ha='center',va='center',color='w')

def get_gibs_wms_raw_image(layername,date_str):
    proj4326 = "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?version=1.3.0&service=WMS&request=GetMap&format=image/png&STYLE=default&bbox=-90,-180,90,180&CRS=EPSG:4326&HEIGHT=512&WIDTH=512&TIME="+date_str+"&layers="+layername+"&TRANSPARENT=TRUE"

    # Request image.
    img = io.imread(proj4326) 
    return img

def get_gibs_colorbar_img(layername):
    legendURL = None

    # Construct capability URL.
    wmsUrl = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetCapabilities'

    # Request WMS capabilities.
    response = requests.get(wmsUrl)

    # Display capabilities XML in original format. Tag and content in one line.
    WmsXml = xmltree.fromstring(response.content)
    # print(xmltree.tostring(WmsXml, pretty_print = True, encoding = str))

    # Coverts response to XML tree.
    WmsTree = xmlet.fromstring(response.content)

    for child in WmsTree.iter():
        for layer in child.findall("./{http://www.opengis.net/wms}Capability/{http://www.opengis.net/wms}Layer//*/"): 
         if layer.tag == '{http://www.opengis.net/wms}Layer': 
            f = layer.find("{http://www.opengis.net/wms}Name")
            if f is not None:
                if f.text == layername:
                    # Style.
                    e = layer.find(("{http://www.opengis.net/wms}Style/" +
                                    "{http://www.opengis.net/wms}LegendURL/" +
                                    "{http://www.opengis.net/wms}OnlineResource"))
                    if e is not None:
                        legendURL = e.attrib["{http://www.w3.org/1999/xlink}href"]

    return np.array(plimg.open(urllib.request.urlopen(legendURL)))

