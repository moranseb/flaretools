import argparse
import csv
from datetime import datetime
import json
import requests
import sys

from api_calls import APICalls
import program_strings
from settings import Settings


class Main:
    """Main loop of program"""

    def __init__(self):
        print(program_strings.logo)
        self._arg_parser()
        self.settings = Settings(self)
        self.api_calls = APICalls(self)
        if self.settings.troubleshoot_log == True:
            _troubleshoot_log_warning()
        self.issue_log = []
        
    def run_program(self):
        """Currently for testing only"""

        self._user_input()
        self._create_my_headers()

        #CSV parsing and API calls
        """with open(self.csv, 'r') as file:
            DictReaderFile = csv.DictReader(file)
            for row in DictReaderFile:
                if self.settings.APIfalures > 0:
                    self._make_api_calls(row)
                else:
                    print("Yikes, there have been a lot of unsuccessful API calls, please review your logs before continuing")
                    sys.exit()"""

        print("During exicution the following issues were flagged. Please review:")
        print(self.issue_log)

        #Print to test your code!!

        if self.settings.quiet == True:
            print("The program is set to quiet")
        if self.settings.quiet == False:
            print("The program is set to verbose")
        if self.settings.log == True:
            print("The program log is on")
        if self.settings.log == False:
            print("The program log is off")
        print(self.settings.log_file)
        print(self.my_headers)
        print(self.csv)
        print(self.account_id)
        print(self.access_token)


    def _user_input(self):

        if self.args.token:
            self.access_token = self.args.token
        else:
            self.access_token = input("\nPlease enter your API token:\n")
            #if len(self.access_token) != 40:
             #   print("Sorry, your API token was not the right length, please try again...\nexiting...")
              #  sys.exit()

        if self.args.id:
            self.account_id = self.args.id
        else:
            self.account_id = input("\nPlease enter your organization's Cloudflare account ID:\n")
            #if len(self.organization_id) != 32:
             #   print("Sorry, your organization's Cloudflare account ID was the wrong length, please try again...\nexiting...")
              #  sys.exit()

        if self.args.csv:
            self.csv = self.args.csv
        else:
            self.csv = input("\nPlease enter the absolute or relative path to the excel file:\n")


    def _create_my_headers(self):
        self.my_headers= {
            'Content-Type' : 'application/json',
            'Authorization' : f'Bearer {self.access_token}'
            }

    def _arg_parser(self):
        """Function to parse the command line arguments."""

        parser = argparse.ArgumentParser(description=program_strings.help_string)

        parser.add_argument('--csv', help="Specify the path to a csv file instead of providing it after program startup.")
        parser.add_argument('--file', type=str, help="Specify a file to store the program logs if not using the default file from settings.py.")
        parser.add_argument('--id', help="Add your organization's Cloudflare account ID from the command line instead of as input once the program starts")
        parser.add_argument('-l', '--log', action='store_true', help="Enable logging")
        parser.add_argument('-nl', '--nologs', action='store_true', help="Disable logging")
        parser.add_argument('-q', '--quiet', action='store_true', help="Decrese program output to only show important errors and messages.")
        parser.add_argument('--token', help="Add your API token at the command line instead of as input once the program starts.")
        parser.add_argument('--troubleshoot', action='store_true', help="This will turn on troubleshooting logging, which will log complete API responses")
        parser.add_argument('-v', '--verbose', action='store_true', 
            help="Increase program output to print more information to the console if quiet is set to True in settings.py.")

        self.args = parser.parse_args()

    def _troubleshoot_log_warning(self):
        answer = input("""WARNING: troubleshoot_log is enabled, this will create a log with full API responses that should be deleted after use.\n
            Do you wish to continue? (y/n)""")
        if answer == "y":
            pass 
        if answer == "n":
            print("Check you settings.py file to make sure the troubleshoot_log is disabled by default,\n and make sure not to enable it at the command line")
            sys.exit()
        else:
            print("Invalid input, exiting...")
            sys.exit()


#API functions here

    def _make_api_calls(row):

        #Add the domain
        domain_name = row['Domain']
        add_domain_response = self.api_calls._add_domain(self.my_headers, domain_name, 
            self.account_id)
        zone_identifier = add_domain_response["result"]["id"]

        #Add DNS rules, this part there are too many fields that I don't understand, ask Jon, especially type and content

        first_content = row['DNSRule1Content']
        first_dns_response = self.api_calls._create_dns_record(self.my_headers, 
            domain_name, first_content, zone_identifier)
        second_content = row['DNSRule2Content']
        second_dns_response = self.api_calls._create_dns_record(self.my_headers, 
            domain_name, second_content, zone_identifier)

        #Add page rules handling with Jon


if __name__ == '__main__':
    # Make an instance, and run the program.
    flare = Main()
    flare.run_program()



"""
to do:

test everything but api calls 
meet with jon and iron out api calls
    type and content on create_dns_record
    configure page rule api call

"""
