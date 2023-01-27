import argparse
import csv
import json
import requests
import sys

import program_strings
import api_calls_v2
import config


def main():

    print(program_strings.logo)
    print("\n\n\nWell then, here we go... Exciting...")
    APIfalures = 3  # Change how many API falures before the program exits.

    issue_log = []
    csv_file = sys.argv[1]

    headers = _create_my_headers()

    # CSV parsing and API calls
    with open(csv_file, 'r') as file:
        DictReaderFile = csv.DictReader(file)
        for row in DictReaderFile:
            if APIfalures > 0:
                _make_api_calls(row, headers)
            else:
                print("Yikes, there have been a lot of unsuccessful API calls, please review your logs before continuing")
                sys.exit(1)

    print("During exicution the following issues were flagged. Please review:")
    print(issue_log)

def _create_my_headers():
    try:
        access_token = config.access_token
    except ModuleNotFoundError:
        print(
            "Please create a config.py file in this directory conatiaining an API Token. Please see the help menu or the documentation for more information"
        )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    return headers

def _make_api_calls(row, headers):

    domain_name = row["Domain to Purchase"]
    account_id = config.account_id
    IPv4 = config.IPv4

    add_zone_response = api_calls_v2.create_zone(headers, domain_name, account_id)
    zone_identifier = add_zone_response["result"]["id"]

    O365_sender = row["O365 Sender"]
    api_calls_v2.add_dns_rules(headers, zone_identifier, domain_name, IPv4, account_id, O365_sender)

    website = row["Website"]
    api_calls_v2.add_page_rules(headers, domain_name, website, zone_identifier)

main()
print("\n\n\n *** So long, and thanks for all the fish *** ")