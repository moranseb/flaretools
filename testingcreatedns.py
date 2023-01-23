import requests
import json
import config

domain_name = ""
account_id = config.account_id
access_token = config.access_token
content = ""
zone_identifier = ""

my_headers = {
    'Content-Type' : 'application/json', 
    'Authorization' : f'Bearer {access_token}'
}

parameters = {
    'type': 'A',
    'name': f'{domain_name}',
    'content': f'{content}',
    'ttl': 3600,
    'priority': 10,
    'proxied': False,
}

#priority and proxied are optional

response = requests.post(f'https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records', 
    headers=my_headers, params=parameters)

print(response.text)
print(response.status_code)

response = json.loads(response.text)

