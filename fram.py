from sys                import exit, argv
from colorama           import Fore, Back, init
from colorama.ansi      import clear_screen, AnsiCursor
from argparse           import ArgumentParser
from os                 import getcwd, mkdir
from os.path            import isfile, exists, join as os_join
from getpass            import _raw_input
from ast                import literal_eval

from loads_files import *
from fram_package.ofuscator_call import *
from fram_package.disassembly_bytes import *
from fram_package.idiomas import Idiomas

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
    parser.add_argument(
                "-l",
                "--lenguaje",        
                help="idioma a usar (es_ES) / ", 
                type=str,
                default="es_ES"
            )
    """parser.add_argument(
                "-f",
                "--gui",        
                help="activar la gui", 
                type=str,
            )"""
    """if len(argv) <= 1:
            parser.print_help()
            exit(1)"""
            
    parser = parser.parse_args()
    
    info_system = ThisSysten()
    data_conf   = None
    idioma = None
    
    def createConfFileInit(ruta):
        print(ruta)
        file = open(ruta, "w")
        file.close()
    def loadDefaultValue():
        idioma = Idiomas(parser.lenguaje)
    def loadConfFile():
        
        if exists(os_join(getcwd(), "conf")):
            if exists(os_join(getcwd(), "conf", "init.json")) == False:
                # si no existe el archivo init.json crearlo
                if "y" in _raw_input("desea crear un archivo de configuracion init.json?(y/n): ").lower().split(" "):
                    createConfFileInit(os_join(getcwd(), "conf", "init.json"))
            else:
                # si existe cargarlo
                file = open(os_join(getcwd(), "conf", "init.json"))
                try: data_conf = literal_eval(file.read())
                except SyntaxError: 
                    print(f"El archivo {os_join(getcwd(), 'conf')}init.json no contiene una sintaxis correcta.\nCorigalo o borre el archivo. Cargando los valores por defecto")
                    loadDefaultValue()
                    return False # error
                file.close()
                idioma = Idiomas(data_conf["idioma"])
        else: 
            print(f"Creando el directorio: {os_join(getcwd(), 'conf')}")
            mkdir(os_join(getcwd(), "conf"))
            
            createConfFileInit(os_join(getcwd(), 'conf', "init.json"))
            loadConfFile() # volver a cargar el archivo de configuracion una vez creado
        return True # todo ok

    loadConfFile()
    print_tree(get_directory())
    
    
    _FuncFormat = FuncFormat(os_join(getcwd(), "examples"), "example.c")
    for func in _FuncFormat.funcs:
        func.print_format()
        func.info_format()
    print(_FuncFormat.create_enum_funcs_name(_FuncFormat.funcs))
    _FuncFormat = FuncFormat(os_join(getcwd(), "examples"), "example.c")
    for func in _FuncFormat.funcs:
        func.print_format()
        func.info_format()
    print_color_c_format(_FuncFormat.create_enum_funcs_name(_FuncFormat.funcs))
    print_instrucciones(disassemble_file(os_join(getcwd(), "examples", "main.o")))
    _FuncFormat.SaveFuncFormatJson()


    from cle.backends.coff import CoffParser

    with open(os_join(getcwd(), "examples", "main.o"), 'rb') as f:
        data = f.read()
    coff_parser = CoffParser(data)
    header = coff_parser.header
    sections = coff_parser.sections
    relocations = coff_parser.relocations
    symbols = coff_parser.symbols
    data = coff_parser.data
    strings = coff_parser.strings
    idx_to_symbol_name = coff_parser.idx_to_symbol_name
    symbol_name_to_idx = coff_parser.symbol_name_to_idx
    print(strings)
    
# Imprime la información de las secciones
for section in sections:
    nombre_seccion = bytes(section.Name).decode('utf-8').rstrip('\x00')
    virtual_size = section.VirtualSize
    virtual_address = section.VirtualAddress
    size_of_raw_data = section.SizeOfRawData
    pointer_to_raw_data = section.PointerToRawData
    pointer_to_relocations = section.PointerToRelocations
    pointer_to_linenumbers = section.PointerToLinenumbers
    num_relocations = section.NumberOfRelocations
    num_linenumbers = section.NumberOfLinenumbers
    characteristics = section.Characteristics
    print("Nombre de la sección:", nombre_seccion)
    print("Tamaño virtual:", virtual_size)
    print("Dirección virtual:", virtual_address)
    print("Tamaño de los datos crudos:", size_of_raw_data)
    print("Puntero a los datos crudos:", pointer_to_raw_data)
    print("Puntero a las reubicaciones:", pointer_to_relocations)
    print("Puntero a las líneas de número:", pointer_to_linenumbers)
    print("Número de reubicaciones:", num_relocations)
    print("Número de líneas de número:", num_linenumbers)
    print("Características:", characteristics)
    print()

for idx, relocs in enumerate(relocations):
    print(f"Reubicaciones de la sección {idx}:")
    for reloc in relocs:
        symbol_index = reloc.SymbolTableIndex
        reloc_type = reloc.Type
        virtual_address = reloc.VirtualAddress
        print(f"Índice del símbolo: {symbol_index}")
        print(f"Tipo de reubicación: {reloc_type}")
        print(f"Dirección virtual: {virtual_address}")
        print()

# Imprime la información de los símbolos
for idx, symbol in enumerate(symbols):
    symbol_name = coff_parser.get_symbol_name(idx)
    storage_class = symbol.StorageClass
    section_number = symbol.SectionNumber
    symbol_value = symbol.Value
    print("Nombre del símbolo:", symbol_name)
    print("Clase de almacenamiento:", storage_class)
    print("Número de sección:", section_number)
    print("Valor del símbolo:", symbol_value)
    print()
    
print("Encabezado del archivo COFF:")
print("Machine:", header.Machine)
print("NumberOfSections:", header.NumberOfSections)
print("NumberOfSymbols:", header.NumberOfSymbols)
print("PointerToSymbolTable:", header.PointerToSymbolTable)
print("SizeOfOptionalHeader:", header.SizeOfOptionalHeader)
print("TimeDateStamp:", header.TimeDateStamp)

print("Datos del archivo COFF:", coff_parser.data)
print("Cadenas del archivo COFF:", coff_parser.strings)
print("Índice de nombres de símbolos:", coff_parser.idx_to_symbol_name)
print("Nombre de símbolos al índice:", coff_parser.symbol_name_to_idx)

"""for i, section in enumerate(sections):
        print(f"Sección {i}:")
        print(f"Nombre: {coff_parser.sections}")
        print(f"Tamaño de datos crudos: {coff_parser.sections.SizeOfRawData}")
        print(f"Dirección virtual: 0x{coff_parser.sections.VirtualAddress:08X}")
        print(f"Tamaño virtual: 0x{coff_parser.sections.VirtualSize:08X}")
        print()"""
