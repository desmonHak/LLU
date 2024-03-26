from os.path    import join 
from os         import getcwd
from sys        import argv

from .GUI.main_GUI       import GUI
from .CLI.main_arg_parse import ParserClass

from .load_conf_user    import ConfUser
from .idiomas           import Idiomas
from .disassembly_bytes import print_instrucciones, disassemble_file
from .ofuscator_call    import FuncFormat, print_color_c_format
from .load_conf_user    import ConfUser

def main():
    
    user_conf = ConfUser()                   # cargar la configuracion de usuario
    parser = ParserClass(user_conf.lenguaje) # obtener los parametros de la CLI
    idioma = Idiomas(parser.parser.lenguaje)
    gui = GUI(idioma)

    if parser.parser.gui: # si ejecuto con --gui, iniciar la GUI
        gui.init_GUI() # aun no se definio su comportamiento

    _FuncFormat = FuncFormat(join(getcwd(), "examples"), "example.c")

    for func in _FuncFormat.funcs:
        func.print_format()
        func.info_format()

    print(_FuncFormat.create_enum_funcs_name(_FuncFormat.funcs))

    _FuncFormat = FuncFormat(join(getcwd(), "examples"), "example.c")

    for func in _FuncFormat.funcs:
        func.print_format()
        func.info_format()

    print_color_c_format(_FuncFormat.create_enum_funcs_name(_FuncFormat.funcs))
    print_instrucciones(disassemble_file(join(getcwd(), "examples", "main.o")))
    _FuncFormat.SaveFuncFormatJson()

    from cle.backends.coff import CoffParser

    with open(join(getcwd(), "examples", "main.o"), "rb") as f:
        data = f.read()

    coff_parser = CoffParser(data)
    header      = coff_parser.header
    sections    = coff_parser.sections
    relocations = coff_parser.relocations
    symbols     = coff_parser.symbols
    data        = coff_parser.data
    strings     = coff_parser.strings
    idx_to_symbol_name = coff_parser.idx_to_symbol_name
    symbol_name_to_idx = coff_parser.symbol_name_to_idx
    print(strings)

    # Imprime la información de las secciones
    for section in sections:
        nombre_seccion = bytes(section.Name).decode("utf-8").rstrip("\x00")
        virtual_size           = section.VirtualSize
        virtual_address        = section.VirtualAddress
        size_of_raw_data       = section.SizeOfRawData
        pointer_to_raw_data    = section.PointerToRawData
        pointer_to_relocations = section.PointerToRelocations
        pointer_to_linenumbers = section.PointerToLinenumbers
        num_relocations        = section.NumberOfRelocations
        num_linenumbers        = section.NumberOfLinenumbers
        characteristics        = section.Characteristics

        print("Nombre de la sección:"          , nombre_seccion        )
        print("Tamaño virtual:"                , virtual_size          )
        print("Dirección virtual:"             , virtual_address       )
        print("Tamaño de los datos crudos:"    , size_of_raw_data      )
        print("Puntero a los datos crudos:"    , pointer_to_raw_data   )
        print("Puntero a las reubicaciones:"   , pointer_to_relocations)
        print("Puntero a las líneas de número:", pointer_to_linenumbers)
        print("Número de reubicaciones:"       , num_relocations       )
        print("Número de líneas de número:"    , num_linenumbers       )
        print("Características:"               , characteristics       )
        print()

    for idx, relocs in enumerate(relocations):
        print(f"Reubicaciones de la sección {idx}:")
        for reloc in relocs:
            symbol_index = reloc.SymbolTableIndex
            reloc_type = reloc.Type
            virtual_address = reloc.VirtualAddress

            print(f"Índice del símbolo : {symbol_index}")
            print(f"Tipo de reubicación: {reloc_type}")
            print(f"Dirección  virtual : {virtual_address}")
            print()

    # Imprime la información de los símbolos
    for idx, symbol in enumerate(symbols):
        symbol_name    = coff_parser.get_symbol_name(idx)
        storage_class  = symbol.StorageClass
        section_number = symbol.SectionNumber
        symbol_value   = symbol.Value

        print("Nombre del símbolo:"     , symbol_name   )
        print("Clase de almacenamiento:", storage_class )
        print("Número de sección:"      , section_number)
        print("Valor del símbolo:"      , symbol_value  )
        print()

    print("Encabezado del archivo COFF:")
    print("Machine:"             , header.Machine             )
    print("NumberOfSections:"    , header.NumberOfSections    )
    print("NumberOfSymbols:"     , header.NumberOfSymbols     )
    print("PointerToSymbolTable:", header.PointerToSymbolTable)
    print("SizeOfOptionalHeader:", header.SizeOfOptionalHeader)
    print("TimeDateStamp:"       , header.TimeDateStamp       )

    print("Datos del archivo COFF:"       , coff_parser.data              )
    print("Cadenas del archivo COFF:"     , coff_parser.strings           )
    print("Índice de nombres de símbolos:", coff_parser.idx_to_symbol_name)
    print("Nombre de símbolos al índice:" , coff_parser.symbol_name_to_idx)

    """for i, section in enumerate(sections):
            print(f"Sección {i}:")"""