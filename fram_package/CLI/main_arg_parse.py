from os.path    import join 
from os         import getcwd
from argparse   import ArgumentParser
from colorama   import init
from sys        import argv

from fram_package.idiomas           import Idiomas

class ParserClass:

    def __init__(self, lenguaje=None):
        self.lenguaje = lenguaje
        self.parser   = self.init_parser()

    def init_parser(self):
        init()
        self.parser = ArgumentParser(
            prog=__doc__,
            description="""
                        framework en C. 
                        """,
            epilog="",
        )

        self.parser.add_argument(
            "-r",
            "--ruta",
            help="ruta del proyecto que contiene todos los *.c y todos los *.h",
            type=str,
        )

        self.parser.add_argument(
            "-mf",
            "--main-file",
            help    = "ruta o nombre del archivo que contiene la funcion main. main.c por defecto",
            type    = str,
            default = "main.c",
        )

        self.parser.add_argument(
            "-l", "--lenguaje", help="idioma a usar (es_ES) / ", type=str, default="es_ES"
        )

        self.parser.add_argument(
                    "-f",
                    "--gui",        
                    help="activar la gui", 
                    type=bool,
                    default = False,
                )

        if len(argv) <= 1:
                self.parser.print_help()

        self.parser = self.parser.parse_args()
        # establecer el idioma pasado por linea de comandos si el constructor no recibio ningun valor lenguaje
        if self.lenguaje != None: 
            self.lenguaje = self.parser.lenguaje 
        return self.parser

