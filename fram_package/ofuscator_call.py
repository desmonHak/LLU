from os import getcwd
from os.path import isfile
from random import randint
from re import MULTILINE, findall
from colorama           import Fore, Back, init

class FuncFormat:
    def __init__(self, name_file) -> None:
        self.name_file = name_file
        self.funcs = []
        for func in self.get_declaration_funcs(self.name_file): 
            self.funcs.append(self.Format(func))
    
    class Format:
        def __init__(self, func) -> None:
            self.type_return = func[0]
            self.attributes  = func[1].split(" ")
            self.name_func   = func[2]
            self.args        = func[3].split(", ")
            
        def print_format(self):
            print(f"{Fore.LIGHTGREEN_EX}{self.type_return} {Fore.LIGHTBLUE_EX}{' '.join(self.attributes)} {Fore.LIGHTMAGENTA_EX}{self.name_func}{Fore.WHITE}({Fore.LIGHTCYAN_EX}{' '.join(self.args)}{Fore.WHITE}) {Fore.RESET} ")
            
        def info_format(self):
            print(f"{Fore.LIGHTGREEN_EX}type_return{Fore.WHITE}: {self.type_return}\n{Fore.LIGHTBLUE_EX}attributes{Fore.WHITE}: {self.attributes}\n{Fore.LIGHTMAGENTA_EX}name_func{Fore.WHITE}: {self.name_func}\n{Fore.LIGHTCYAN_EX}args{Fore.WHITE}: {self.args}{Fore.RESET}\n")
    
    def get_declaration_funcs(self, name_file):
        if isfile(name_file):
            with open(name_file, 'r') as archivo:
                contenido_archivo = archivo.read()
                return findall(r"^(?!#)*(\w+(?:\s+\w+)*)(?:\**)?\s+(?:\**)?\s*(__attribute__.*\))?\s*(?:\**)?(\w+_?\w+)\s*\((.*\n*)\)\s*{", contenido_archivo, MULTILINE)

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
