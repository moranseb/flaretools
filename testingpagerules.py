import requests
import json
import config

account_id = config.account_id
access_token = config.access_token
zone_identifier = ""

my_headers = {
    'Content-Type' : 'application/json', 
    'Authorization' : f'Bearer {access_token}'
}

parameters = {
    'targets': [
        {
            'target': 'url',
            'constraint': {
                'operator': 'matches',
                'value': '*example.com/images/*',
            },
        },
    ],
    'actions': [
        {
            'id': 'browser_check',
            'value': 'on',
        },
    ],
    'priority': 1,
    'status': 'active',
}

response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{zone_identifier}/pagerules', 
    headers=my_headers, params=parameters)

print(response.text)
print(response.status_code)

response = json.loads(response.text)

print(response)
zone_identifier = response["result"]["id"]