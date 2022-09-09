# Please read before using the script
# * This is a python script that writes the name, public domain and systemdomains to a file for all the endpoints in a given area.
# * File is created in the directory the script is excuted from.
# * Everytime this script is executed it generates a new oauth token for authentication against API Management APIs.
# * This script has a for loop that makes call to the API based on the number of services created in the area.
# * Number of calls made on this script will be counted against the daily quota allocated to the API Management issued api key.
# * This is a boiler plate script that can be modified as per requirement.
# * API calls used in this script are documented on https://developer.mashery.com/docs
# * Details required to run this script api_key_issued, api_key_secret, admin_username, admin_password and area_scope. For reference, 
# these are mentioned on https://developer.mashery.com/docs/read/mashery_api/30/Authentication.

import requests
from requests.auth import HTTPBasicAuth
import time
import credentials

def authenticate():

	api_key = credentials.api_key
	secret = credentials.secret
	url = "https://api.mashery.com/v3/token"
	basic = HTTPBasicAuth(api_key,secret)
	payload = {'grant_type': 'password', 'username': credentials.username, 'password': credentials.password, 'scope': credentials.scope}
	response = requests.post(url, auth=basic, data=payload)

	return response.json()["access_token"]

def fetch_service(headers):
    service_url = "https://api.mashery.com/v3/rest/services"
    # By default the get call returns 100 items. You can change the limit value to be more than 100.
    parameters = {'limit': 1000}
    service_json = requests.get(service_url, headers=headers, params=parameters)
    print(f'Number of services returned {len(service_json.json())}. Which means total number of API calls executed on this script run will be {len(service_json.json()) + 1}. Unless interrupted.')
    return service_json.json()


def print_endpoint_names(service_metadata, headers):
    headers = {'Authorization': f'Bearer {authenticate()}', 'Content-Type': 'application/json'}
    f = open('endpoints_list.txt', 'w')
    for x in service_metadata:
        # print(x['name'])
        Endpoints = requests.get(f"https://api.mashery.com/v3/rest/services/{x['id']}/endpoints?fields=name,publicDomains,systemDomains", headers=headers)
        # print(Endpoints.json())
        # file is written in the format <Service_name>: <Endpoint_metadata>
        f.write(x['name'] + ":" + str(Endpoints.json()) + "\n\n")
        # Adding a sleep time to avoid developer over rate errors
        time.sleep(1)
    f.close()

def main():
    token = authenticate()
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    services_json = fetch_service(headers)
    print_endpoint_names(services_json, headers)

if __name__ == "__main__":
    main()