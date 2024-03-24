from os import getcwd
from os.path import isfile, join as os_join
from random import randint
from re import MULTILINE, findall
from colorama           import Fore, Back, init
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import get_lexer_by_name

class FuncFormat:
    def __init__(self, ruta, name_file) -> None:
        self.name_file = name_file
        self.funcs = []
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
            
    def SaveFuncFormatJson(self, dir="."):
        file = open(f"f_{self.name_file}.json", "w")
        data =  """{
    "name_file" : \""""+self.name_file+"""\",
    "funcs"     : {"""

        for i in range(0, len(self.funcs)):
            data += f"""
        "{i}" : """ + """{"""+ f"""
            "type_return" : "{self.funcs[i].type_return}",
            "attributes"  : """+str(self.funcs[i].attributes).replace("'", '"')+f""",
            "name_func"   : "{self.funcs[i].name_func}",
            "args"        : """+str(self.funcs[i].args).replace("'", '"')+"""
            }"""
            if i != len(self.funcs)-1: data += ","
        data += """
        },
    "numer_funcs" : """+str(len(self.funcs))+"""
}
"""
        print(data)
        file.write(data)
        file.close()
        return f"f_{self.name_file}"
        
    def get_declaration_funcs(self):
        if isfile(os_join(self.ruta, self.name_file)):
            with open(os_join(self.ruta, self.name_file), 'r') as archivo:
                contenido_archivo = archivo.read()
                return findall(r"^(?!#)*(\w+(?:\s+\w+)*)(?:\**)?\s+(?:\**)?\s*(__attribute__.*\))?\s*(?:\**)?(\w+_?\w+)\s*\((.*\n*)\)\s*{", contenido_archivo, MULTILINE)
        else: raise Exception(f"Error no existe el archivo {os_join(self.ruta, self.name_file)}")
        # crear error personalizado

    def get_funcs_name(self, declaration_funcs):
        funcs_name = []
        for funcion in declaration_funcs: funcs_name.append(funcion[2])
        return funcs_name

    
    def create_enum_funcs_name(self, funcs_name):
        string_enum = str()
        string_enum += "typedef enum %s {\n" % "_".join(self.name_file.split("."))
        for func in funcs_name: 
            string_enum += f"\tf_{'_'.join(self.name_file.split('.'))}_{func.name_func},\n" 
        string_enum += "} enum %s;" % "_".join(self.name_file.split("."))
        return string_enum

def print_color_c_format(data):
    print(
        highlight(
            code=data,
            lexer= get_lexer_by_name("nasm"),
            formatter=Terminal256Formatter(style="dracula")
        ), end=''
    )

def ofucator_call(name_file, enum, range):
    if isfile(name_file):
        funciones = list()
        
        encontrado = False
        value = 0
        with open(name_file, 'r') as archivo:
            for linea in archivo:
                if f"enum {argv[2]}" in linea:
                    encontrado = True
                    print("// Enum encontrado:")
                    print("/*\n * typedef enum %s {" % argv[2])
                elif encontrado and "}" in linea:
                    break
                elif encontrado:
                    linea_valor = linea.strip().split("=")
                    if len(linea_valor) == 1:
                        print(f" * \t{linea.strip().split(',')[0]} = {hex(value)},")
                        if linea.strip()[:2] != "f_":
                            print(f"Este valor( {linea.strip()} ) no sigue la convencion {linea.strip()[:2]}")
                            exit(-1)
                        else: 
                            funciones.append(linea.strip().split(",")[0][2:])
                    else:
                        value = int(linea_valor[1].strip().split(",")[0])
                        print(f" * \t{linea_valor[0]} = {hex(value)}")
                        if linea_valor.strip()[0][:2] != "f_":
                            print("Este valor no sigue la convencion")
                            exit(-1)
                        else:
                            funciones.append(linea_valor.strip()[0][2:])
                    value+=1
        archivo.close()
        if not encontrado: print(f"El enum {argv[2]} no se encontro en {file_c}")
        else: print(" * }\n */")
        
        for funcion in funciones:
            try:
                print(f"#define OFFSET_RAND_{funcion} {hex(randint(int(argv[3]), int(argv[4])))}")
            except ValueError:
                print(f"#define OFFSET_RAND_{funcion} {hex(randint(int(argv[3], 16), int(argv[4], 16)))}")
            print(f"// f_{funcion}")
