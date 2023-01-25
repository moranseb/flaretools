# After completing with Jon, remeber to add edits to the main program.

import requests
import json
import config

#This will be passed in from the previous call
zone_identifier = ""

#Type changes between calls, this call will be made 5 times. Domain needs to be passed into these calls
domain = "" # Pull from csv header <Domain to Purchase>

# username will be passed in from the csv
username="" # Pull from csv header <O365 Sender>

for i in range(5):

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records"

    type_list= ("A", "CNAME", "CNAME", "CNAME", "TXT")
    type = type_list[i]

    name_list= ("@", "www", "selector1._domainkey", "selector2._domainkey", "_dmarc")
    name = name_list[i]

    content_list = [f"{config.IPv4}", "@", f"selector1-{domain}-com._domainkey.abstraktmktg.onmicrosoft.com", 
        f"selector2-{domain}-com._domainkey.abstraktmktg.onmicrosoft.com", f"v=DMARC1; p=none; pct=100; rua={username}; ruf=mailto:{username}; fo=1"]
    content = content_list[i]

    ttl_tuple = (1, 1, 120, 120, 120)
    ttl= ttl_tuple[i]

    proxied_tuple = (True, True, False, False)
    if i == 4:
        pass
    else:
        proxied = proxied_tuple[i]

    account_id = config.account_id
    access_token = config.access_token

    my_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    if i == 4:
        parameters = {
            "type": type,
            "name": name,
            "content": content,
            "ttl": ttl
        }

    else:
        parameters = {
            "type": type,
            "name": name,
            "content": content,
            "ttl": ttl,
            "proxied": proxied
        }

    # priority and proxied are optional

    response = requests.post(
        url,
        headers=my_headers,
        json=parameters,
    )

    print(response.text)
    print(response.status_code)

    response = json.loads(response.text)

    print(response)

    with open('logs.txt', 'a') as f:
        f.write(f"creating dns response: \n {response} \n\n\n")