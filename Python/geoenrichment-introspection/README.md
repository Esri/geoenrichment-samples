# Geoenrichment-Introspection

ArcGIS Python API Geoenrichment module introspection examples using both local and remote sources for enrichment.

## Requirements

- [ArcGIS Python API](https://developers.arcgis.com/python/) 1.9.1 or greater

You will need a Python Environment with the ArcGIS Python API 1.9.1 or greater installed. This is the only hard requirement. Enrichemnt can be performed using either local or remote resources. Local enrichment requires ArcGIS Pro with Business Analyst and at least one country's data pack. Remote resources can be accessed through an Esri Web GIS with geoenrichment configured. This Web GIS can be either ArcGIS Online or ArcGIS Enterprise (Portal with Business Analyst Server). Of note, if using ArcGIS Online, enriching data _will_ use ArcGIS Online credits.

## Getting Started

If you have ArcGIS Pro 2.9 installed, you already have the ArcGIS Python API 1.9.1 installed. If you also have the Business Analyst extension with a country's dataset installed locally, you can run the local introspection and enrichment notebook.

This however, is _not_ a requirement for the Web GIS Notebooks. The only requirement for these notebooks is access to a Web GIS with the geoenrichment configured. This Web GIS can be either ArcGIS Enterprise or ArcGIS Online. If ArcGIS Enterprise, geoenrichemnt must be configured. ArcGIS Enterprise can use either a licensed and configured ArcGIS Business Analyst Server, or it can use ArcGIS Online. Also, you can connect to ArcGIS Online directly.

## Using Make - common commands

Based on the pattern provided in the [Cookiecutter Data Science template by Driven Data](https://drivendata.github.io/cookiecutter-data-science/) this template streamlines a number of commands using the `make` command pattern.

- `make env` - This will quickly create an Conda environment named `geoenrichment` for you to run the included notebooks. If in a Windows environment, this command will asssume you are working in a Python environment included with ArcGIS Pro. Whether in Windows or *nix (Linux or macOS), this command will create a new Conda environment ready to run the example notebooks in the `notebook` directory.

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
