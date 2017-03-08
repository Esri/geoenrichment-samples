'''
Copyright 2017 Esri

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.​
'''


import requests

arcpy.GetActivePortalURL()

portal = arcpy.GetActivePortalURL()

arcpy.GetSigninToken()

token = arcpy.GetSigninToken()["token"]

data = {"f":"json", "token":token}

response = requests.post(portal + "sharing/portals/self", data)

response.json()["helperServices"]["geoenrichment"]["url"]

ge_url = response.json()["helperServices"]["geoenrichment"]["url"]


#*******************************************

response = requests.post(ge_url + "/Geoenrichment/Countries", data)

response.json()["countries"][20]

response.json()["countries"][20]["id"]


#******************************************

response = requests.post(ge_url + "/Geoenrichment/Reports/BG", data)

#******************************************
import functools
def get_request_as_string(query_url, data):
	get_request_data = [k + "=" + str(v) for k, v in data.items()]
	return query_url + "?" + functools.reduce(lambda a,b:a + "&" + b, get_request_data)

get_request_as_string(ge_url + "/Geoenrichment/Reports/BG", data)
		
#**************************************
# Custom Reports samples

search_data = {"f":"json", 
    "token":token, 
    "q":'type:"Report Template" AND typekeywords:esriWebReport',
    "num":100,
    "sortOrder":"asc",
    "sortField":"title",
    "start":1
    }
response = requests.post(portal + "/sharing/rest/search", search_data)


report_data = {"f":"json",
    "token":token,
    "report":'{"itemid":"305c391fdbda4ee49414fc095432ef8c"}',
    "studyAreas":'[{"featureSet":{"fields":[{"name":"OBJECTID","alias":"Object ID","type":"esriFieldTypeOID"},{"name":"AREA_DESC","alias":"AREA_DESC","type":"esriFieldTypeString","length":8,"nullable":true},{"name":"AREA_DESC2","alias":"AREA_DESC2","type":"esriFieldTypeString","length":19,"nullable":true}],"spatialReference":{"wkid":102100,"latestWkid":3857},"geometryType":"esriGeometryPolygon","features":[{"geometry":{"rings":[[[-13046162.4581862,4038479.8221407],[-13046028.5581138,4038475.17549524],[-13045895.2964613,4038461.25772474],[-13045763.3085999,4038438.13522072],[-13044428.7885244,4037406.11887813],[-13046162.4581862,4046281.68115603]]],"spatialReference":{"wkid":102100,"latestWkid":3857}},"attributes":{"AREA_DESC":"5 milhas","AREA_DESC2":"Anéis: 5 milha raio","OBJECTID":3}}]}}]'}

response = requests.post(ge_url + "/Geoenrichment/CreateReport", report_data)
    