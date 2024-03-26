from os                  import getcwd
from os.path             import isfile, join as os_join
from random              import randint
from re                  import MULTILINE, findall
from colorama            import Fore
from pygments            import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers     import get_lexer_by_name
from json                import dumps

from .error import NotFoundThisFile

class FuncFormat:
    def __init__(self, ruta, name_file, idioma=None) -> None:
        self.name_file = name_file
        self.funcs = []
        self.idioma = None
        self.ruta = ruta
        for func in self.get_declaration_funcs(): 
            self.funcs.append(self.Format(func))
    
    class Format:
        def __init__(self, func) -> None:
            self.type_return = func[0]
            self.attributes  = func[1].split(" ")
            while '' in self.attributes: self.attributes.remove('')
            self.name_func   = func[2]
            self.args        = func[3].split(", ")
            while '' in self.args: self.args.remove('')
            
        def print_format(self):
            print_color_c_format(f"{self.type_return} {' '.join(self.attributes)} {self.name_func}({' '.join(self.args)})  ")
            
        def info_format(self):
            print(f"{Fore.LIGHTGREEN_EX}type_return{Fore.WHITE}: {self.type_return}\n{Fore.LIGHTBLUE_EX}attributes{Fore.WHITE}: {self.attributes}\n{Fore.LIGHTMAGENTA_EX}name_func{Fore.WHITE}: {self.name_func}\n{Fore.LIGHTCYAN_EX}args{Fore.WHITE}: {self.args}{Fore.RESET}\n")
            
    def SaveFuncFormatJson(self, dir=".") -> str:
        """
                descripcion
            Args:
                args1 (type_args1): descripcion args
                args2 (type_args2, optional): descripcion args.
                args3 (type_args3, optional): descripcion args

            Raises:
                UnknownOS: error que ocurre cuando la plataforma no puede identificarse

            Returns:
                type_return: descripcion del valor retornado
        """
        with open(f"f_{self.name_file}.json", "w") as file:
            data = {
                "name_file" : self.name_file,
                "funcs"     : {
                },
                "numer_funcs" : str(len(self.funcs))
            }
            for i in range(0, len(self.funcs)): data["funcs"].update({ 
                i : {
                    "type_return" : self.funcs[i].type_return,
                    "attributes"  : self.funcs[i].attributes,
                    "name_func"   : self.funcs[i].name_func,
                    "args"        : self.funcs[i].args
                }
            })
            data = dumps(data, indent=4)
            print(highlight(data, lexer= get_lexer_by_name("json"), formatter=Terminal256Formatter(style="dracula")))
            file.write(data)

        return f"f_{self.name_file}"
        
    def get_declaration_funcs(self) -> str:
        """
                descripcion
            Args:
                args1 (type_args1): descripcion args
                args2 (type_args2, optional): descripcion args.
                args3 (type_args3, optional): descripcion args

            Raises:
                UnknownOS: error que ocurre cuando la plataforma no puede identificarse

            Returns:
                type_return: descripcion del valor retornado
        """
        if isfile(os_join(self.ruta, self.name_file)):
            with open(os_join(self.ruta, self.name_file), 'r') as archivo:
                contenido_archivo = archivo.read()
                return findall(r"^(?!#)*(\w+(?:\s+\w+)*)(?:\**)?\s+(?:\**)?\s*(__attribute__.*\))?\s*(?:\**)?(\w+_?\w+)\s*\((.*\n*)\)\s*{", contenido_archivo, MULTILINE)
        else: raise NotFoundThisFile(os_join(self.ruta, self.name_file))

    def get_funcs_name(self, declaration_funcs) -> list:
        """
                descripcion
            Args:
                args1 (type_args1): descripcion args
                args2 (type_args2, optional): descripcion args.
                args3 (type_args3, optional): descripcion args

            Raises:
                UnknownOS: error que ocurre cuando la plataforma no puede identificarse

            Returns:
                type_return: descripcion del valor retornado
        """
        funcs_name = []
        for funcion in declaration_funcs: funcs_name.append(funcion[2])
        return funcs_name
    
    def create_enum_funcs_name(self, funcs_name) -> str:
        """
                descripcion
            Args:
                args1 (type_args1): descripcion args
                args2 (type_args2, optional): descripcion args.
                args3 (type_args3, optional): descripcion args

            Raises:
                UnknownOS: error que ocurre cuando la plataforma no puede identificarse

            Returns:
                type_return: descripcion del valor retornado
        """
        
        string_enum = str()
        string_enum += "typedef enum %s {\n" % "_".join(self.name_file.split("."))
        for func in funcs_name: 
            string_enum += f"\tf_{'_'.join(self.name_file.split('.'))}_{func.name_func},\n" 
        string_enum += "} enum %s;" % "_".join(self.name_file.split("."))
        return string_enum

def print_color_c_format(data) -> None:
    """
                descripcion
            Args:
                args1 (type_args1): descripcion args
                args2 (type_args2, optional): descripcion args.
                args3 (type_args3, optional): descripcion args

            Raises:
                UnknownOS: error que ocurre cuando la plataforma no puede identificarse

            Returns:
                type_return: descripcion del valor retornado
    """
    print(
        highlight(
            code=data,
            lexer= get_lexer_by_name("nasm"),
            formatter=Terminal256Formatter(style="dracula")
        ), end=''
    )

