from settings import Settings
from datetime import datetime
import requests
import json
import sys


class APICalls:
    def __init__(self, flare_program):

        self.settings = Settings(flare_program)
        self.flare = flare_program

    def _add_domain(my_headers, domain_name, account_id):
        """Make API call to Cloudflare to add a domain, needs to return result id for dns record request"""

        parameters = {
            "name": f"{domain_name}",
            "account": {
                "id": f"{account_id}",
            },
            "jump_start": True,
            "type": "full",
        }

        # Jumpstart and type are optional, ask Jon

        response = requests.post(
            "https://api.cloudflare.com/client/v4/zones",
            headers=my_headers,
            params=parameters,
        )

        response = json.loads(response.text)

        if self.settings.quiet == False:
            print(
                f"[*] API call to add domain {domain_name}, success: {response['success']}status code: {response.status_code}, errors: {response['errors']}"
            )

        if response["success"] == False:
            print(f"[WARNING] API call to add domain {domain_name} failed.")
            self.settings.APIfalures -= 1
            self.flare.issue_log.append(
                f"API call to DNS rule for {domain_name} failed."
            )

        if self.settings.log == True:
            success_code = response["success"]
            result_information = (response["result"]["name"], response["errors"])
            url = "https://api.cloudflare.com/client/v4/zones"
            opstring = "to create a zone for"
            _log_request(url, domain_name)
            _log_response(success_code, result_information, opstring)

        if self.settings.troubleshoot_log == True:
            url = "https://api.cloudflare.com/client/v4/zones"
            _troubleshoot_log_func(parameters, my_headers, url, response)

        _response_code_handler(response)

        return response

    def _create_dns_record(my_headers, domain_name, content, zone_identifier):
        """Make API call to create DNS records for the added domain."""

        parameters = {
            "type": "A",
            "name": f"{domain_name}",
            "content": f"{content}",
            "ttl": 3600,
            "priority": 10,
            "proxied": False,
        }

        # priority and proxied are optional

        response = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records",
            headers=my_headers,
            params=parameters,
        )

        response = json.loads(response.text)

        if self.settings.quiet == False:
            print(
                f"[*] API call to add DNS rule for {domain_name}, success: {response['success']}status code: {response.status_code}, errors: {response['errors']}"
            )

        if response["success"] == False:
            print(f"[WARNING] API call to DNS rule for {domain_name} failed.")
            self.flare.issue_log.append(
                f"API call to create DNS rule for {domain_name} failed."
            )
            self.settings.APIfalures -= 1

        if self.settings.log == True:
            success_code = response["success"]
            result_information = (response["result"]["name"], response["errors"])
            url = f"https://api.cloudflare.com/client/v4/zones/<obfuscated>/dns_records"
            opstring = "create a DNS record for"
            _log_request(url, domain_name)
            _log_response(success_code, result_information, opstring)

        if self.settings.troubleshoot_log == True:
            url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/dns_records"
            _troubleshoot_log_func(parameters, my_headers, url, response)

        _response_code_handler(response)

        return response

    def _create_page_rule():
        """Make an API call to create page rules."""

        parameters = {
            "targets": [
                {
                    "target": "url",
                    "constraint": {
                        "operator": "matches",
                        "value": "*example.com/images/*",
                    },
                },
            ],
            "actions": [
                {
                    "id": "browser_check",
                    "value": "on",
                },
            ],
            "priority": 1,
            "status": "active",
        }

        response = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/pagerules",
            headers=my_headers,
            params=parameters,
        )

        response = json.loads(response.text)

        if self.settings.quiet == False:
            print(
                f"[*] API call to add page rule, success: {response['success']}status code: {response.status_code}, errors: {response['errors']}"
            )

        if response["success"] == False:
            print(
                f"[WARNING] API call to add a page rule for zone {zone_identifier} failed."
            )
            self.settings.APIfalures -= 1
            self.flare.issue_log.append(
                f"API call to create page rule for {zone_identifier} failed."
            )

        if self.settings.log == True:
            success_code = response["success"]
            result_information = (response["result"]["name"], response["errors"])
            url = f"https://api.cloudflare.com/client/v4/zones/<obfuscated>/dns_records"
            opstring = "add a page rule for"
            _log_request(url, domain_name, opstring)
            _log_response(success_code, result_information)

        if self.settings.troubleshoot_log == True:
            url = f"https://api.cloudflare.com/client/v4/zones/{zone_identifier}/pagerules"
            _troubleshoot_log_func(parameters, my_headers, url, response)

        _response_code_handler(response)

        return response

    def _log_request(url, domain_name, opstring):
        with open(self.settings.log_file, "a") as file:
            timestamp = datetime.now()
            file.write(
                f"{timestamp}\nA request was made to {url} to {opstring} {domain_name}\n"
            )

    def _log_response(success_code, result_information):
        with open(self.settings.log_file, "a") as file:
            file.write(
                f"Success code recieved: {success_code}\nErrors recieved: {result_information[2]} for request for {result_information[1]}\n\n\n"
            )

    def _troubleshoot_log_func(parameters, my_headers, url, response):
        with open(self.settings.troubleshoot_file, "a") as file:
            timestamp = datetime.now()
            file.write(
                f"{timestamp}\nRequest: {url}\n{my_headers}\n{parameters}\n\nResponse:\n{response}\n\n\n\n"
            )

    def _response_code_handler(response):
        if response.status_code == 400:
            print(
                "Oops, 400 error, bad request. Change request format before trying again. Exiting..."
            )
            sys.exit()
        if response.status_code == 401:
            print(
                "Oops, 401 error, unauthorized. Check your API token, if repeated errors check header format. Exiting..."
            )
            sys.exit()
        if response.status_code == 403:
            print(
                "Oops, 403 error, forbidden. Check your API token. If repeated errors with a valid API token, check API token permissions."
            )
            sys.exit()


"""
example curl requests:
add a domain:
curl -X POST "https://api.cloudflare.com/client/v4/zones" \
     -H "X-Auth-Email: user@example.com" \
     -H "X-Auth-Key: c2547eb745079dac9320b638f5e225cf483cc5cfdda41" \
     -H "Content-Type: application/json" \
     --data '{"name":"example.com","account":{"id":"01a7362d577a6c3019a474fd6f485823"},"jump_start":true,"type":"full"}'

create a DNS record:
curl -X POST "https://api.cloudflare.com/client/v4/zones/023e105f4ecef8ad9ca31a8372d0c353/dns_records" \
     -H "X-Auth-Email: user@example.com" \
     -H "X-Auth-Key: c2547eb745079dac9320b638f5e225cf483cc5cfdda41" \
     -H "Content-Type: application/json" \
     --data '{"type":"A","name":"example.com","content":"127.0.0.1","ttl":3600,"priority":10,"proxied":false}
ttl can be 1 for automatic


create a page rule: 
curl -X POST "https://api.cloudflare.com/client/v4/zones/023e105f4ecef8ad9ca31a8372d0c353/pagerules" \
     -H "X-Auth-Email: user@example.com" \
     -H "X-Auth-Key: c2547eb745079dac9320b638f5e225cf483cc5cfdda41" \
     -H "Content-Type: application/json" \
     --data '{"targets":[{"target":"url","constraint":{"operator":"matches","value":"*example.com/images/*"}}],"actions":[{"id":"browser_check","value":"on"}],"priority":1,"status":"active"}


  """
