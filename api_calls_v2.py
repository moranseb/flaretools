import requests
import json

import flaretools

def create_zone(headers, domain_name, account_id):
    parameters = {
        "name": f"{domain_name}",
        "account": {
            "id": f"{account_id}",
        },
        "jump_start": "false",
        "type": "full",
    }

    response = requests.post(
        "https://api.cloudflare.com/client/v4/zones", headers=headers, json=parameters
    )

    response = json.loads(response.text)

    if response["success"] == True:
        print(
            f"[*] API call to add domain {domain_name}, success: {response['success']}status code: {response.status_code}, errors: {response['errors']}"
        )

    if response["success"] == False:
        print(f"[WARNING] API call to add domain {domain_name} failed.")
        flaretools.APIfalures -= 1
        flaretools.issue_log.append(f"API call to add {domain_name} failed.")
        print(response.text)
        print(response.status_code)

    return response

def add_dns_rules(headers, zone_identifier, domain_name, IPv4, account_id, O365_sender):

    for i in range(5):

        url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records"

        type_list= ("A", "CNAME", "CNAME", "CNAME", "TXT")
        type = type_list[i]

        name_list= ("@", "www", "selector1._domainkey", "selector2._domainkey", "_dmarc")
        name = name_list[i]

        content_list = [f"{IPv4}", "@", f"selector1-{domain_name}-com._domainkey.abstraktmktg.onmicrosoft.com", 
            f"selector2-{domain_name}-com._domainkey.abstraktmktg.onmicrosoft.com", f"v=DMARC1; p=none; pct=100; rua={O365_sender}; ruf=mailto:{O365_sender}; fo=1"]
        content = content_list[i]

        ttl_tuple = (1, 1, 120, 120, 120)
        ttl= ttl_tuple[i]

        proxied_tuple = (True, True, False, False)
        if i == 4:
            pass
        else:
            proxied = proxied_tuple[i]

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

    response = requests.post(
        url,
        headers=headers,
        json=parameters
    )

    response = json.loads(response.text)

    if response["success"] == True:
        print(
            f"[*] API call to add DNS rule {str(i+1)} for {domain_name}, success: {response['success']}status code: {response.status_code}, errors: {response['errors']}"
        )

    if response["success"] == False:
        print(f"[WARNING] API call to add DNS rule {str(i+1)} for {domain_name} failed.")
        flaretools.APIfalures -= 1
        flaretools.issue_log.append(f"API call to add DNS {str(i+1)} rule for {domain_name} failed.")
        print(response.text)
        print(response.status_code)

def add_page_rules(headers, domain_name, website, zone_identifier):

    parameters = {
        "targets": [
            {
                "target": "url",
                "constraint": {
                    "operator": "matches",
                    "value": f"*{domain_name}",
                },
            },
        ],
        "actions": [
            {
                "id": "forwarding_url",
                "value": {
                    "url": f"http://{website}",
                    "status_code": 301
                },
            },
        ],
        "status": "active",
    }

    response = requests.post(
        f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/pagerules",
        headers=headers,
        json=parameters,
    )

    if response["success"] == True:
        print(
            f"[*] API call to add a page rule for {domain_name}, success: {response['success']}status code: {response.status_code}, errors: {response['errors']}"
        )

    if response["success"] == False:
        print(f"[WARNING] API call to add a page rule for {domain_name} failed.")
        flaretools.APIfalures -= 1
        flaretools.issue_log.append(f"API call to add a page rule for {domain_name} failed.")
        print(response.text)
        print(response.status_code)