'''
Copyright 2017 Esri

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

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [CreateReportTool]

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
    
    ''' Returns list of countries available in Geoenrichment service '''
    def getCountries(self):
        countries_url = self.ge_url + "/Geoenrichment/Countries"
        data = {"f":"json", "token":self.getToken()}
        countries_json = requests.post(countries_url, data).json()
        countries_list = countries_json["countries"]
        countries_ids_names = [(c["id"], c["name"]) for c in countries_list]
        return countries_ids_names

    ''' Returns list of report templates available for the given country '''
    def getReportTemplates(self, country):
        reports_url = self.ge_url + "/Geoenrichment/Reports/" + country
        data = {"f":"json", "token":self.getToken()}
        reports_json = requests.post(reports_url, data).json()
        reports_list = reports_json["reports"]
        reports_ids_names = [(r["reportID"], r["metadata"]["name"]) for r in reports_list]
        return reports_ids_names

    ''' Executes the given report template for the given country for the given input features '''
    def createReport(self, features, country, template, pdf):
        create_report_url = self.ge_url + "/Geoenrichment/CreateReport"
        study_areas = json.dumps(features)
        data = {
            "studyAreas": study_areas,
            "f":"bin",
            "format":"PDF",
            "report":template,
            "appID":"createreportgp",
            "token":self.getToken()
        }
        
        response = requests.post(create_report_url, data)
        
        # log request into Geoprocessing Messages
        arcpy.AddMessage(self.get_request_as_string(create_report_url, data))
        
        # there are cases when you get 200 status code and "error" json in the body
        # this can be addressed by checking the content-type
        if  response.status_code == 200 and response.headers["content-type"] == "application/pdf;charset=UTF-8":
            with open(pdf, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            arcpy.AddError("Server response: " + response.text)

    ''' Displays a Windows message box - for debugging purposes only'''  
    def Mbox(self, title, text, style):
        ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
    ''' Returns current Sign In Token from ArcGIS Pro '''    
    def getToken(self):
        token_dictionary = arcpy.GetSigninToken()
        return token_dictionary["token"]

    ''' Returns request in "requests" format (url + data) in "browser" format (endpoint url and parameters in a single url)'''
    def get_request_as_string(self, query_url, data):
        get_request_data = [k + "=" + requests.utils.quote(str(v)) for k, v in data.items()]
        return query_url + "?" + functools.reduce(lambda a,b:a + "&" + b, get_request_data)        

class CreateReportTool(object):
    def __init__(self):
        self.label = "Create Reports Tool"
        self.description = ""
        self.canRunInBackground = True
        self.ge = Geoenrichment()

    def getParameterInfo(self):
        
        # Input Features parameter
        in_features = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

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

        # Input Template
        in_template = arcpy.Parameter(
            displayName="Report Template",
            name="in_template",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        # Output PDF
        out_pdf = arcpy.Parameter(
            displayName="Output PDF file",
            name="out_pdf",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")
        
        out_pdf.filter.list = ["pdf"]

        self.params = [in_features, in_country, in_template, out_pdf]
        
        return self.params		

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):

        country = parameters[1].value
        
        if parameters[1].altered:
            parameters[2].filter.list = [id for id,_ in self.ge.getReportTemplates(country)]

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        # get parameter values
        in_features = parameters[0].valueAsText
        in_country =  parameters[1].valueAsText
        in_template =  parameters[2].valueAsText
        out_pdf =  parameters[3].valueAsText

        # convert input to JSON
        temp_folder = tempfile.mkdtemp()
        temp_file = temp_folder + "createReport.json"
        arcpy.conversion.FeaturesToJSON(in_features, temp_file, "NOT_FORMATTED", "NO_Z_VALUES", "NO_M_VALUES", "NO_GEOJSON")
        
        # read and parse resulsts of FeaturesToJSON
        with open(temp_file, 'r') as content_file:
            content = content_file.read()
        
        features_json = json.loads(content)
        
        spatial_reference = features_json["spatialReference"]
        
        features = features_json["features"]
        
        # make sure each feature "knows" it's spatial reference
        for f in features:
            f["spatialReference"] = spatial_reference
        
        # pass "features" node to Geoenrichment
        self.ge.createReport(features, in_country, in_template, out_pdf)
