import hashlib
import time
import requests, json
from requests.auth import HTTPBasicAuth
import credentials

apiKey = credentials.api_key
sharedSecret = credentials.secret

def get_hash(apiKey,sharedSecret):
    authHash = hashlib.md5()
    temp = str.encode(apiKey + sharedSecret + repr(int(time.time())))
    authHash.update(temp)
    return authHash.hexdigest()


def get_token():
    url = 'https://api.mashery.com/v3/token'
    payload = {'grant_type':'password','username': credentials.username,'password': credentials.password,'scope': credentials.scope}
    res = requests.post(url, auth=HTTPBasicAuth(apiKey, sharedSecret), data=payload)
    return res.json()['access_token']


