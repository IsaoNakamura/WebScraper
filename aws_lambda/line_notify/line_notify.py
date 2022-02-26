import json

# pip3 install 
import requests

def lambda_handler(event, context):
    # TODO implement
    access_token = event['access_token']
    url = event['url']
    message = event['message']
    print(message)
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'message': message}
    res = requests.post(url, headers=headers, params=payload)
    return res.status_code