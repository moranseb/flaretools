#!python3
import csv
import json
import requests
import sys
import tkinter
from tkinter import filedialog
import os

import program_strings
import config

def main():

    print(program_strings.logo)

    global APIfalures
    APIfalures = 50  # Change how many API falures before the program exits.

    global issue_log
    issue_log = []

    headers = _create_my_headers()

    try:
        csv_file = sys.argv[1]
    except IndexError:
        csv_file = get_file()

    #CSV parsing and API calls
    with open(csv_file, 'r') as file:
        DictReaderFile = csv.DictReader(file)
        for row in DictReaderFile:
            if APIfalures > 0:
                _make_api_calls(row, headers)
            else:
                print("Yikes, there have been a lot of unsuccessful API calls, please review before continuing")
                x = input("Press ENTER to exit:\n")
                sys.exit(1)

    print("During exicution the following issues were flagged. Please review:")
    print(issue_log)

def create_config():
    print("Your config.py file is not setup, please complete the following steps, then re-run the program.\n")
    with open("config.py", "w") as f:
        token = input("Please enter your Cloudflare API token:\n").strip()
        org_id = input("Plase enter your organization's Cloudflare ID:\n").strip()
        IPv4 = input("Please enter the IP address needed in your DNS rules:\n").strip()
        f.write(f'access_token = "{token}"\naccount_id = "{org_id}"\nIPv4 = "{IPv4}"')
        x = input("Press ENTER to exit:\n")
        sys.exit()

def _create_my_headers():
    try:
        if not config.access_token:
            create_config()
    except (ModuleNotFoundError, AttributeError):
        create_config()

    access_token = config.access_token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers

def get_file():
    root = tkinter.Tk()
    root.withdraw() #use to hide tkinter window

    currdir = os.getcwd()
    filename = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a CSV file')

    return filename

def _make_api_calls(row, headers):

    domain_name = row["Domain to Purchase"]
    account_id = config.account_id
    IPv4 = config.IPv4

    add_zone_response = create_zone(headers, domain_name, account_id)
    if add_zone_response["success"] == False:
        pass
    else:
        zone_identifier = add_zone_response["result"]["id"]

        O365_sender = row["0365 Sender"]
        add_dns_rules(headers, zone_identifier, domain_name, IPv4, account_id, O365_sender)

        website = row["Website "]
        add_page_rules(headers, domain_name, website, zone_identifier)



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

    for item in (401, 403):
        if response.status_code == item:
            print(f"\n\n[WARNING] You recieved a {response.status_code} error, please check your Cloudflare API token.")
            print("Note: This may mean your Cloudflare token may have expired. Please verify. To replace token, edit config.py or delete config.py and re-run this program to replace.")
            print(f"[WARNING] API call to add domain {domain_name} failed.\n")
            x = input("Press ENTER to exit:\n")
            sys.exit()
    response = json.loads(response.text)

    if response["success"] == True:
        print(
            f"[*] API call to add domain {domain_name} succeeded, errors: {response['errors']}"
        )

    if response["success"] == False:
        print(f"\n[WARNING] API call to add domain {domain_name} failed.\n")
        print(response)
        global APIfalures
        APIfalures -= 1
        issue_log.append(f"API call to add {domain_name} failed.")

    return response

def add_dns_rules(headers, zone_identifier, domain_name, IPv4, account_id, O365_sender):

    for i in range(5):

        url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records"

        type_list= ("A", "CNAME", "CNAME", "CNAME", "TXT")
        dns_type = type_list[i]

        name_list= ("@", "www", "selector1._domainkey", "selector2._domainkey", "_dmarc")
        name = name_list[i]

        content_list = [f"{IPv4}", "@", f"selector1-{domain_name}-com._domainkey.cmgmsco.onmicrosoft.com", 
            f"selector2-{domain_name}-com._domainkey.cmgmsco.onmicrosoft.com", f"v=DMARC1; p=none; pct=100; rua={O365_sender}; ruf=mailto:{O365_sender}; fo=1"]
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
                "type": dns_type,
                "name": name,
                "content": content,
                "ttl": ttl
            }

        else:
            parameters = {
                "type": dns_type,
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
                f"[*] API call to add DNS rule {str(i+1)} for {domain_name} succeeded, errors: {response['errors']}"
            )

        if response["success"] == False:
            print(f"\n[WARNING] API call to add DNS rule {str(i+1)} for {domain_name} failed.\n")
            global APIfalures
            APIfalures -= 1
            issue_log.append(f"API call to add DNS {str(i+1)} rule for {domain_name} failed.")

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

    response = json.loads(response.text)

    if response["success"] == True:
        print(
            f"[*] API call to add a page rule for {domain_name} succeeded, errors: {response['errors']}"
        )

    if response["success"] == False:
        print(f"\n[WARNING] API call to add a page rule for {domain_name} failed.\n")
        global APIfalures
        APIfalures -= 1
        issue_log.append(f"API call to add a page rule for {domain_name} failed.")

main()
x = input("Press ENTER to exit:\n")
#So long, and thanks for all the fish