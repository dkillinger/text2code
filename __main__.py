from src.renpy.args import *
from src.renpy.read import *

def main():
    print('starting program...')
    argv = argv_parse.Argv_Parser()
    args = argv.parser.parse_args()
    arg_obj = args_obj.Args_Object()
    arg_obj.argparse_populate(args)
    arg_obj.print()

if __name__ == '__main__':
    main()