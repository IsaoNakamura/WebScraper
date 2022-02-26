import json
import boto3
import os
from base64 import b64decode

# pip3 install 
import requests

def lambda_handler(event, context):
    # TODO implement
    #access_token = event['access_token']
    access_token_cipher = os.environ.get('LINE_ACCESS_TOKEN')
    access_token = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(access_token_cipher),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    #url = event['url']
    url_cipher = os.environ.get('LINE_ENDPOINT')
    url = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(url_cipher),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    message = event['message']
    print(message)
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'message': message}
    res = requests.post(url, headers=headers, params=payload)
    return { 'StatusCode': res.status_code }
