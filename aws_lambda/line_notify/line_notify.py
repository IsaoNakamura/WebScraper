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
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    # return { 'StatusCode': res.status_code }
    return json.dumps(res)