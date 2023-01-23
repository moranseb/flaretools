import requests
import json
import config


domain_name = ""
account_id = config.account_id
access_token = config.access_token

my_headers = {
    'Content-Type' : 'application/json', 
    'Authorization' : f'Bearer {access_token}'
    }


parameters = {
            'name': f'{domain_name}',
            'account': {
                'id': f'{account_id}',
            },
            'jump_start': True,
            'type': 'full',
}


# Jumpstart and type are optional, ask Jon

response = requests.post('https://api.cloudflare.com/client/v4/zones', 
            headers=my_headers, params=parameters)

print(response.text)
print(response.status_code)

response = json.loads(response.text)

print(response)
zone_identifier = response["result"]["id"]