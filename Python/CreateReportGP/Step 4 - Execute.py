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
        
        features = features_json["features"]
        
        # pass "features" node to Geoenrichment
        self.ge.createReport(features, in_country, in_template, out_pdf)