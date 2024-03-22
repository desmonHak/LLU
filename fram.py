from sys                import exit, argv
from colorama           import Fore, Back, init
from colorama.ansi      import clear_screen, AnsiCursor
from argparse           import ArgumentParser
from os import getcwd
from os.path import isfile

from loads_files import *
from fram_package.ofuscator_call import *

if __name__ == '__main__':
    init()
    parser = ArgumentParser(
                prog = __doc__,
                description = """
                    framework en C. 
                """,
                epilog="""
                """
            )
    parser.add_argument(
                "-r",
                "--ruta",        
                help="ruta del proyecto que contiene todos los *.c y todos los *.h", 
                type=str,
            )
    parser.add_argument(
                "-mf",
                "--main-file",        
                help="ruta o nombre del archivo que contiene la funcion main. main.c por defecto", 
                type=str,
                default="main.c"
            )
    """if len(argv) <= 1:
            parser.print_help()
            exit(1)"""
            
    parser = parser.parse_args()
    
    print_tree(get_directory())
    _FuncFormat = FuncFormat("example.c")
    for func in _FuncFormat.funcs:
        func.print_format()
        func.info_format()
    print(_FuncFormat.create_enum_funcs_name(_FuncFormat.funcs))
    
    