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


import requests

arcpy.GetActivePortalURL()

portal = arcpy.GetActivePortalURL()

portal_self_url = portal + "sharing/portals/self"

arcpy.GetSigninToken()

token = arcpy.GetSigninToken()["token"]

data = {"f":"json", "token":token}

response = requests.post(portal_self_url, data)

response.json()

response.json()["helperServices"]["geoenrichment"]["url"]

ge_url = response.json()["helperServices"]["geoenrichment"]["url"]


*******************************************

countries_url = ge_url + "/Geoenrichment/Countries"

response = requests.post(countries_url, data)

response.json()["countries"][20]

response.json()["countries"][20]["id"]


******************************************

bg_reports_url = ge_url + "/Geoenrichment/Reports/BG"

response = requests.post(bg_reports_url, data)

******************************************
import functools
def get_request_as_string(query_url, data):
	get_request_data = [k + "=" + str(v) for k, v in data.items()]
	return query_url + "?" + functools.reduce(lambda a,b:a + "&" + b, get_request_data)

get_request_as_string(bg_reports_url, data)
		
		


