"""
Default settings and option handling for flaretool.
"""


class Settings:
    """Class to store and initialize settings."""

    def __init__(self, flare_program):
        """Initialize settings"""

        # Edit these to change the default settings
        self.quiet = False  # Change to control if the default program output is quiet or verbose.
        self.log = True  # Change to control if the program logs by default.
        self.APIfalures = 3  # Change how many API falures before the program exits.
        self.log_file = "flaretool_logs.txt"  # Change this to control where logs are added. Remeber to keep it wrapped in "" marks.
        self.troubleshoot_log = False  # WARNING - This will log complete API responses which contain sensitive information,
        #   delete log file after use.
        self.troubleshoot_file = "flare_troublshooting.txt"  # Change this to change the name of the troubleshooting log.

        # Don't change this
        self.args = flare_program.args
        self._initialize_user_settings()

    def _initialize_user_settings(self):
        """Initilize settings entered at the command line"""

        if self.args.quiet:
            self.quiet = True
        if self.args.file:
            self.log_file = self.args.file
        if self.args.nologs == True:
            self.log = False
        if self.args.log == True:
            self.log = True
        if self.args.verbose:
            self.quiet = False
        if self.args.troubleshoot == True:
            self.troubleshoot_log = self.args.troubleshoot
