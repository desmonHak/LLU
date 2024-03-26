from os.path import join
from os import getcwd
from argparse import ArgumentParser
from colorama import init
from sys import argv

from fram_package.idiomas import Idiomas


class ParserClass:

    def __init__(self, lenguaje=None):
        init()
        self.lenguaje = lenguaje
        self.parser = self.init_parser(lenguaje=lenguaje)

    def init_parser(self, lenguaje=None):
    
        idioma = Idiomas() if (lenguaje is None) else Idiomas(lenguaje)# cargar el idioma deseado

        self.parser = ArgumentParser(
            prog=__doc__,
            description=idioma.idioma_data["main_arg_parse.py"]["ArgumentParser"][
                "description"
            ],
            epilog=idioma.idioma_data["main_arg_parse.py"]["ArgumentParser"]["epilog"],
        )

        self.parser.add_argument(
            idioma.idioma_data["main_arg_parse.py"]["1"]["flag_s"],
            idioma.idioma_data["main_arg_parse.py"]["1"]["flag_l"],
            help=idioma.idioma_data["main_arg_parse.py"]["1"]["help"],
            type=str,
        )

        self.parser.add_argument(
            idioma.idioma_data["main_arg_parse.py"]["2"]["flag_s"],
            idioma.idioma_data["main_arg_parse.py"]["2"]["flag_l"],
            help=idioma.idioma_data["main_arg_parse.py"]["2"]["help"],
            type=str,
            default="main.c",
        )

        self.parser.add_argument(
            "-l",
            "--lenguaje",
            help="idioma a usar (es_ES) / ",
            type=str,
            default="es_ES",
        )

        self.parser.add_argument(
            idioma.idioma_data["main_arg_parse.py"]["4"]["flag_s"],
            idioma.idioma_data["main_arg_parse.py"]["4"]["flag_l"],
            help=idioma.idioma_data["main_arg_parse.py"]["4"]["help"],
            type=bool,
            default=False,
        )

        if len(argv) == 1 or (len(argv) == 3 and argv[1] == '-l' and self.lenguaje == argv[2]):            
            self.parser.print_help()
        elif len(argv) == 3 and argv[1] == '-l' and self.lenguaje != argv[2]: # ['llu.py', '-l', 'en_US']
            self.lenguaje = argv[2]
            del(self.parser)
            return self.init_parser(lenguaje=argv[2]) # volevr a ejecutarse a si misma con el nuevo idioma

        self.parser = self.parser.parse_args()
        # establecer el idioma pasado por linea de comandos si el constructor no recibio ningun valor lenguaje
        if self.lenguaje != None:
            self.lenguaje = self.parser.lenguaje
        return self.parser
