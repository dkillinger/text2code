import argparse
import sys

'''
******************************************************************
The Help_Formatter class changes the format of the 
ArgumentParser's help menu (accessed via -h) to NOT show the 
metavar instead of showing it after every flag. Useful for visual 
clarity, and maintains metavar for access.
'''
class Help_Formatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default = self._get_default_metavar_for_optional(action)
        return ', '.join(action.option_strings)

'''
******************************************************************
The Argv_Parser class stores all of the flags used on the command 
line by using an ArgumentParser. Also adds flag information which 
can be accessed when entering the -h or --help flag on the command
line.
'''
class Argv_Parser:
    def __init__(self):
        # lambda for formatting help menu in argparser
        fmt = lambda prog: Help_Formatter(prog)
        self.parser = argparse.ArgumentParser(usage=sys.argv[0] + ' -r [file options] -t [prog params] [prog options]', description='A collection of flags used by ' + sys.argv[0] + ' for the command line interface.', formatter_class=fmt)
        self.parser._optionals.title = 'arguments' # risky line of code, can break ArgumentParser in a future update
        
        # flags for file arguments, stored as string values
        self.parser.add_argument('-g', '--game-directory', dest='GAME', help='(REQUIRED) set the Ren\'Py project game directory', required=True)
        self.parser.add_argument('-w', '--write-file', dest='WRITE', help='(REQUIRED) set file program will write to AND code label (must be unique)', required=True)
        self.parser.add_argument('-r', '--read-file', dest='READ', help='(REQUIRED) set file program will read from', required=True)
        