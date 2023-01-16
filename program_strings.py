logo = """
        ____  ______   ____  _______  _____   ____    _     _  _______  
      /  _ ||  __  | /  ___||__   __||  _  | /  _ \\   \\ \\  | ||__   __|
     / / | || |  | | | |       | |   | | | | | | | |   \\ \\ | |   | |  
    / /  | || |__| / | |___    | |   | | | | | |_| |    \\ \\| |   | |  
   / /___| ||  __  | |___  |   | |   | |_| | |  _  |    / /| |   | | 
  / _____  || |  | |     | |   | |   |    /  | | | |   / / | |   | | 
 / /     | || |__| |  ___| |   | |   | |\\ \\  | | | |  / /  | |   | | 
/_/      |_||______| |_____|   |_|   |_| \\_\\ |_| |_| /_/   |_|   |_| 
 _______  _      _____  _____  ____  _______  _____  _____  _
|  _____|| |    /  _  \\|  _  ||  __||__   __|/  _  \\/  _  \\| |
| |____  | |    | | | || | | || |      | |   | | | || | | || |
|  ____| | |    | |_| || | | || |__    | |   | | | || | | || |
| |      | |    |  _  || |_| ||  __|   | |   | | | || | | || |
| |      | |    | | | ||    / | |      | |   | | | || | | || |
| |      | |___ | | | || |\\ \\ | |__    | |   | |_| || |_| || |____
|_|      |_____||_| |_||_| \\_\\|____|   |_|   \\_____/\\_____/|______|

"""

help_string = """

The program takes a CSV file, parses it, and adds the domain names, DNS rules
and page rules to Cloudflare using the Cloudflare API. You must provide:\n

1) A valid Cloudflare API token in the config.py file\n
2) A valid organization ID\n
3) A path to a CSV file\n

"""

        #CSV parsing and API calls
"""
        with open(self.csv, 'r') as file:
            DictReaderFile = csv.DictReader(file)
            for row in DictReaderFile:
                if self.settings.APIfalures > 0:
                    self._make_api_calls(row)
                else:
                    print("Yikes, there have been a lot of unsuccessful API calls, please review your logs before continuing")
                    sys.exit()
"""
