import json
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

def fetch_application_count(headers):

    application_url = "https://api.mashery.com/v3/rest/applications"
    # headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    print("Getting offset count")
    application_count = requests.head(application_url, headers=headers).headers['X-Total-Count']
    loop_count = int(application_count) // 1000
    if int(application_count) % 1000:
        loop_count += 1
    return loop_count

def fetch_applications(loopCount, headers):

    application_name_id = {}
    # headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    print("Getting application metadata using limits and offsets")
    for x in range(loopCount):
        application_get_all = requests.get(f"https://api.mashery.com/v3/rest/applications?limit=1000&offset={x}", headers=headers)
        print(f"Offset count in progress: {x}")
        for x in application_get_all.json():
            application_name_id[x['id']] = x['name']
    return application_name_id

def fetch_application_metadata(appids, headers):

    # headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    count = 1
    output_list = []
    application_name_ids = appids
    print(f"Number of application ids fetched: {len(application_name_ids)}")
    for id in application_name_ids:
    
        application_metadata = requests.get(f"https://api.mashery.com/v3/rest/applications/{id}/packageKeys?fields=apikey,member.username,application.name,package.name,plan.name,secret", headers=headers)
        print(f"Application id in progress: {id}")
        application_metadata_list = application_metadata.json()
        
        if not application_metadata_list:
            output_list.append({'Application Name': application_name_ids[id],
            'API Key': 'None'})

        for apps in application_metadata_list:
            output_list.append({'Application Name': apps['application']['name'], 
            'Username': apps['member']['username'], 
            'API Key': apps['apikey'],
            'Secret': apps['secret'],
            'Package Name': apps['package']['name'],
            'Plan Name': apps['plan']['name']})
        
        print(f"Value of count is: {count}")
        count += 1
    return output_list

def main():
    oauth_token = authenticate()
    headers = {'Authorization': f'Bearer {oauth_token}', 'Content-Type': 'application/json'}
    app_count = fetch_application_count(headers)
    application_ids = fetch_applications(app_count, headers)
    output_list = fetch_application_metadata(application_ids, headers)

    json_object = json.dumps(output_list , indent=4)
    with open("acme_applications.json", "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    main()




