# After completing with Jon, remeber to add edits to the main program.

import requests
import json
import config

account_id = config.account_id
access_token = config.access_token
zone_identifier = ""
domain = ""
real_site = "" # Pull from csv header <Website>

my_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
}

parameters = {
    "targets": [
        {
            "target": "url",
            "constraint": {
                "operator": "matches",
                "value": f"*{domain}",
            },
        },
    ],
    "actions": [
        {
            "id": "forwarding_url",
            "value": {
                "url": f"http://{real_site}",
                "status_code": 301
            },
        },
    ],
    "status": "active",
}

response = requests.post(
    f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/pagerules",
    headers=my_headers,
    json=parameters,
)

print(response.text)
print(response.status_code)

response = json.loads(response.text)

print(response)

with open('logs.txt', 'a') as f:
    f.write(f"page rules response: \n {response} \n\n\n")