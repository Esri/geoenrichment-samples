'''
Copyright 2017 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.​
'''


import requests, json

arcpy.GetActivePortalURL()

portal = arcpy.GetActivePortalURL()

arcpy.GetSigninToken()

token = arcpy.GetSigninToken()["token"]

data = {"f":"json", "token":token}

response = requests.post(portal + "sharing/portals/self", data)

response.json()["helperServices"]["geoenrichment"]["url"]

ge_url = response.json()["helperServices"]["geoenrichment"]["url"]

#************** Enrich *************

data = {"f":"json", "token":token, "studyAreas": json.dumps([{"geometry":{"x":-116.53,"y":33.825}}])}
response = requests.post(ge_url + "/Geoenrichment/Enrich", data)
response.text

studyAreasOptions={"areaType":"DriveTimeBuffer","bufferUnits":"esriDriveTimeUnitsMinutes","bufferRadii":[15]}
data = {"f":"json", "token":token, "studyAreas": json.dumps([{"geometry":{"x":-116.53,"y":33.825}}]), "StudyAreasOptions": json.dumps(studyAreasOptions)}
response = requests.post(ge_url + "/Geoenrichment/Enrich", data)
response.text


data = {"f":"json", "token":token, "studyAreas": json.dumps([{"geometry":{"x":-116.53,"y":33.825}}]), "StudyAreasOptions": json.dumps(studyAreasOptions), "returnGeometry":True}
response = requests.post(ge_url + "/Geoenrichment/Enrich", data)
response.text


data = {"f":"json", "token":token, "studyAreas": json.dumps([{"geometry":{"x":-116.53,"y":33.825}}]), "StudyAreasOptions": json.dumps(studyAreasOptions), "analysisVariables":json.dumps(["MP21024a_I", "MP27051h_B", "AVGHINC_CY"])}
response = requests.post(ge_url + "/Geoenrichment/Enrich", data)
response.text


#************** Enrich Std Geo *************
 
studyAreas=[{"sourceCountry":"US","layer":"US.ZIP5","ids":["92373","92262"]}]

data = {"f":"json", "token":token, "studyAreas": json.dumps(studyAreas), "analysisVariables":json.dumps(["MP21024a_I", "MP27051h_B", "AVGHINC_CY"])}
response = requests.post(ge_url + "/Geoenrichment/Enrich", data)
response.text

#********************  Standard Geography Levels ***********************


data = {"f":"json", "token":token}

response = requests.post(ge_url + "/Geoenrichment/Countries", data)
response.json()["countries"][14]
response.json()["countries"][14]["id"]

response = requests.post(ge_url + "/Geoenrichment/StandardGeographyLevels/" + "BE", data)

response.json()["geographyLevels"][0]["hierarchies"][0]["levels"]
response.text

#********************  Standard Geography Query ***********************

data = {"f":"json", "sourceCountry": "BE", "geographylayers": ["BE.Provinces"], "returnGeometry": True, "geographyQuery": "Bruxelles", "generalizationLevel":2, "token":token}

response = requests.post(ge_url + "/StandardGeographyQuery/execute", data)


studyAreas=[{"sourceCountry":"BE","layer":"BE.Provinces","ids":["04000"]}]

data = {"f":"json", "token":token, "studyAreas": json.dumps(studyAreas)}
response = requests.post(ge_url + "/Geoenrichment/Enrich", data)
response.text

