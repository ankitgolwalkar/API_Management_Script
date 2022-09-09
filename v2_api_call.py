import requests
import json
import hashlib
import time
import credentials


apiKey = credentials.api_key
sharedSecret = credentials.secret
f = open("output.txt",'w')

def buildAuthParams():
    authHash = hashlib.md5()
    temp = str.encode(apiKey + sharedSecret + repr(int(time.time())))
    authHash.update(temp)
    return authHash.hexdigest()

initial_payload = { "method": "object.query", "params": [ "SELECT email, first_name, last_name from members WHERE area_status = 'active' PAGE 1 ITEMS 50" ], "id": 1}
initial_res = requests.post(f'https://api.mashery.com/v2/json-rpc/{credentials.area_id}?apikey={apiKey}&sig={buildAuthParams()}',data=json.dumps(initial_payload))

index = int(initial_res.json()['result']['total_pages']) #Get total number of pages for results to run a for loop
time.sleep(2)

for x in range(1,index+1):
    payload = { "method": "object.query", "params": [ f"SELECT email, first_name, last_name from members WHERE area_status = 'active' PAGE {x} ITEMS 50" ], "id": 1}
    res = requests.post(f'https://api.mashery.com/v2/json-rpc/{credentials.area_id}?apikey={apiKey}&sig={buildAuthParams()}',data=json.dumps(payload))
    # print(res.status_code) #print status code of the API call on every request
    f.write(res.text)
    time.sleep(2)
    if res.status_code != 200:	#In case one of the call fails break the look and exit
    	print(res.status_code)
    	print(res.text)
    	break
f.close()

