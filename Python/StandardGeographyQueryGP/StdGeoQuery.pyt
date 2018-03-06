'''
Copyright 2018 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.​
'''

import arcpy
import requests
import tempfile
import json
import functools
import shutil
import ctypes
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "StdGeoQueryToolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [StdGeographyQueryTool]

''' Encapsulates calls to Geoenrichment service'''
class Geoenrichment(object):
    def __init__(self):
        # discover Geoenrichment URL
        portal = arcpy.GetActivePortalURL()
        portal_self_url = portal + "/sharing/portals/self"
        data = {"f":"json", "token":self.getToken()}
        response = requests.post(portal_self_url, data)

        response_json = response.json()

        self.ge_url = response_json["helperServices"]["geoenrichment"]["url"]
        self.username = response_json["user"]["username"]
    
    ''' Returns list of countries available in Geoenrichment service '''
    def getCountries(self):
        countries_url = self.ge_url + "/Geoenrichment/Countries"
        data = {"f":"json", "token":self.getToken()}
        countries_json = requests.post(countries_url, data).json()
        countries_list = countries_json["countries"]
        countries_ids_names = [(c["id"], c["name"]) for c in countries_list]
        return countries_ids_names

    def getGeographyLevels(self, country):
        geo_levels_url = self.ge_url + "/Geoenrichment/StandardGeographyLevels/" + country
        data = {"f":"json", "token":self.getToken()}
        geo_levels_json = requests.post(geo_levels_url, data).json()
        hierarchies_json = geo_levels_json["geographyLevels"][0]["hierarchies"]
        hierarchy_census_json = hierarchies_json[0]
        levels_json = hierarchy_census_json["levels"]
        return [l["id"] for l in levels_json]

    def performGeographyQuery(self, country, level, query):
        std_geo_query_url = self.ge_url + "/StandardGeographyQuery/execute"
        data = {"f":"json", "sourceCountry": country, "geographylayers": [level], "returnGeometry": True, "geographyQuery": query, "generalizationLevel":2, "token":self.getToken()}
        result_json = requests.post(std_geo_query_url, data).json()
        return result_json["results"][0]["value"]



    ''' Displays a Windows message box - for debugging purposes only'''  
    def Mbox(self, text, title = "Sample", style = 0):
        ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
    ''' Returns current Sign In Token from ArcGIS Pro '''    
    def getToken(self):
        token_dictionary = arcpy.GetSigninToken()
        return token_dictionary["token"]

    ''' Returns request in "requests" format (url + data) in "browser" format (endpoint url and parameters in a single url)'''
    def get_request_as_string(self, query_url, data):
        get_request_data = [k + "=" + requests.utils.quote(str(v)) for k, v in data.items()]
        return query_url + "?" + functools.reduce(lambda a,b:a + "&" + b, get_request_data)        

class StdGeographyQueryTool(object):
    def __init__(self):
        self.label = "Generate Standard Geography Layer"
        self.description = ""
        self.canRunInBackground = True
        self.ge = Geoenrichment()

    def getParameterInfo(self):
        # Input Country
        in_country = arcpy.Parameter(
            displayName="Country",
            name="in_country",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # get list of countries from Geoenrichment and set the list of countries IDs
        # as a filter for in_country parameter
        in_country.filter.list = [c for c, _ in self.ge.getCountries()]
        in_country.value = "US"
        
        # Input Geography Level parameter
        in_gl = arcpy.Parameter(
            displayName="Geography Level",
            name="in_gl",
            datatype="GPString",
            parameterType="Required",
            direction="Input")


        # Input Search Query parameter
        in_query = arcpy.Parameter(
            displayName="Search Query",
            name="in_query",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # Input Search Query parameter
        out_fc = arcpy.Parameter(
            displayName="Output FeatureClass",
            name="out_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")
            
        self.params = [in_country, in_gl, in_query, out_fc]
        
        return self.params		

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        country = parameters[0].value
        
        if parameters[0].altered:
            parameters[1].filter.list = self.ge.getGeographyLevels(country)

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        # get parameter values
        in_country =  parameters[0].valueAsText
        in_gl =  parameters[1].valueAsText
        in_query =  parameters[2].valueAsText
        out_fc =  parameters[3].valueAsText
        
        if arcpy.Exists(out_fc):
            arcpy.Delete_management(out_fc)
        
        feature_set_json = self.ge.performGeographyQuery(in_country, in_gl, in_query)
        
        # convert input to JSON
        temp_folder = tempfile.mkdtemp()
        temp_file = os.path.join(temp_folder, "stdgeo.json")
        
        # write feature set
        with open(temp_file, 'w') as json_file:
            json_file.write(json.dumps(feature_set_json))
        
        arcpy.conversion.JSONToFeatures(temp_file, out_fc)

        
        
