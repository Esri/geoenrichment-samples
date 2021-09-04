import os
from tempfile import tempdir
from pathlib import Path

from arcgis.geometry import Polygon
from arcgis.gis import GIS
from dotenv import load_dotenv, find_dotenv

from generate_infographic import custom_create_report

# variables which should be set based on unique requirements
report_item_id = '2ce64a16cb3c431186a47c6a42156515'  # Demographic Summary built-in infographic
output_path = Path(tempdir)/'output-infographic.pdf'
geom = Polygon({
    "rings": [[
        [-123.202067106731, 46.7620299475149],
        [-122.202716898989, 46.7620299475149],
        [-122.202716898989, 47.1868400401426],
        [-123.202067106731, 47.1868400401426],
        [-123.202067106731, 46.7620299475149]
    ]], "spatialReference": {"wkid": 4326, "latestWkid": 4326}})

# use python-dotenv to load ArcGIS Online organization url and credentials
load_dotenv(find_dotenv())
url, user, pswd = [os.getenv(itm) for itm in ['AGOL_URL', 'AGOL_USERNAME', 'AGOL_PASSWORD']]
assert all([url, user, pswd])

# create a GIS object instance
gis = GIS(url, username=user, password=pswd)
assert isinstance(gis, GIS)

# create custom report using function
result_path = custom_create_report(
    study_areas=geom,
    gis=gis,
    report_id=report_item_id,
    out_path=output_path
)
