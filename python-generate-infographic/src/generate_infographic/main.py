import json
from pathlib import Path
from typing import Union, List

from arcgis.geoenrichment import create_report
from arcgis.geometry import Geometry
from arcgis.gis import GIS


def custom_create_report(
        study_areas: Union[Geometry, List[Geometry]],
        gis: GIS,
        report_id: str,
        out_path: Union[str, Path],
        export_format: str = 'pdf'
):
    """
    This is a pretty thin wrapper around the ``arcgis.geoenrichment.create_report``
    method to make it easier to run reports, specifically infographic reports, using
    the ArcGIS Python API.

    Args:
        study_areas: Either a single Geometry or list of Geometry objects.
        gis: Required instantiated GIS object instance.
        report_id: Web GIS Item id.
        out_path: Path to where the output file will be saved.
        export_format: String for desired output format. Default is 'pdf'.

    Returns:
        Path to where output report is stored.

    """
    # ensure list of geometries if only one geometry inputted
    in_geom = [study_areas] if not isinstance(study_areas, list) else study_areas

    # ensure all inputs are valid geometries
    assert all([isinstance(geom, Geometry) for geom in in_geom])

    # format geometries as list of dicts so create_report leaves alone
    in_geom = [{'geometry': json.loads(geom.JSON)} for geom in in_geom]

    # validate export format
    export_format = export_format.lower()
    assert export_format in ['xlsx', 'pdf', 'html']

    # get the directory and file name from path
    out_folder = str(out_path.parent)
    out_name = str(out_path.name)

    # ensure right extension is used
    if not out_name.endswith(export_format):
        out_name = f'{out_name}.{export_format}'

    # get the report
    out_report = create_report(
        study_areas=in_geom,
        report=report_id,
        export_format=export_format,
        out_folder=out_folder,
        out_name=out_name,
        gis=gis
    )

    return Path(out_report)
