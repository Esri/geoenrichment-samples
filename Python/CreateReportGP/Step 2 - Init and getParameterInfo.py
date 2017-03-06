   '''
   Copyright 2017 Esri

   Licensed under the Apache License, Version 2.0 (the "License");

   you may not use this file except in compliance with the License.

   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software

   distributed under the License is distributed on an "AS IS" BASIS,

   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

   See the License for the specific language governing permissions and

   limitations under the License.​
   '''
		
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