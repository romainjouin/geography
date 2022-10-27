import qgis
import requests
import glob
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

# 1) Get the Shapefile

url_shapefile = "https://files.opendatarchives.fr/professionnels.ign.fr/bdforet/BDFORET_V2/BDFORET_2-0__SHP_LAMB93_D001_2014-04-01.7z"
base_dir = "~/Desktop/"
output_file = base_dir + url_shapefile[url_shapefile.rfind("/")+1:]

# Download the file
response = requests.get(url_shapefile)
open(output_file, "wb").write(response.content)

# TO ADD : unzipping => has to be done by hand now

# Find the shapefiles
shape_files = glob.glob(base_dir + '/**/*.shp', recursive=True)


# 2) Load the layer
p = QgsVectorLayer(shape_files[0], 'display name', 'ogr')

# 3) Split 

# Set width and height as you want
window_width = 300
window_height = 300

# Run the function
output = cut_polygon_into_windows(p, window_height, window_width)

# 4) Add the layer to the Layers panel
QgsProject.instance().addMapLayers([output])
