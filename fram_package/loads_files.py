if __name__ == "__main__":
    from os.path import dirname, abspath
    from sys import path
    path.append(dirname(dirname(abspath(__file__))))

from pathlib             import Path
from colorama            import Fore
from typing              import Generator, Union
from hashlib             import md5
from random              import randint
from requests            import request

from pygments            import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers     import get_lexer_by_name


from fram_package.get_info_system import ThisSysten
from fram_package.error           import NotFoundThisFile

import re
import json

exclusion_patterns:dict = {
    # directorios a ignorar
    "directories": [
        [".git"]
    ],
    # archivos a ignorar
    "files": [
        [".gitignore"]
    ],
    # ignorar cualquiera cosa cosa con este nombre
    "*": [
        # "*.so",
        # "*.exe",
        # "__pycache__"
    ],
}

def load_file(filename) -> None:
    """
    """
    try:
        with open(filename, 'r') as file:
            return json.loads(file.read())

    except FileNotFoundError:
        print("Archivo de configuracion no encontrado: " + filename)
        raise NotFoundThisFile(filename)

def add_exclusion_pattern(exclusion_dict:dict = exclusion_patterns, exclusion: Union[str, list[str]] = None, category:str = None) -> None:
    """
        Añadir los archivos/directorios a excluir
    Args:
        exclusion_dict(dict): Defaults to exclusion_patterns, diccionario donde se guardan
            las exclusiones (valores a los cuales no se les calculara el hash)

        exclusion(str|dict[str]): Defaults to None, exclusion que el cual se añaira a exclusion_dict

        category(str): Defaults to None, esta sera la categoria en que entra exclusion para poderse
            ignorar (directrios | archivo | *).
    """

    if exclusion is None or category is None:
        return

    separator = ThisSysten().get_separator()

    match category:
        case "directories":
            exclusion_dict["directories"].append(exclusion)
        case "files":
            exclusion_dict["files"].append(exclusion)
        case "*":
            if isinstance(exclusion, list):
                exclusion = separator.join(exclusion)

            exclusion_dict["*"].append(exclusion)
        case _: return  # noqa: E701

def format_to_json(data) -> str:
    return json.dumps(data, indent=4, ensure_ascii=False)

def load_gitignore ( gitignore: Path = Path(".gitignore"), exclude_patterns: dict = exclusion_patterns ) -> None:
    """
        Utiliza archivos y directorios del .gitignore añadiendolos al hashes_ignore
        los cuales seran excluidos al calcular el hash para comprobar las actualizaciones
    Args:
        gitignore(Path): Defaults to Path(".gitignore"): ruta del .gitignore
        exclude_hashes(dict): Defaults to hashes_ignore, variable del diccionario
            que es utilizara para guardar los valores del gitignore y que se ignoren
            al calcular el hash para las actualizaciones
    """

    if not gitignore.exists():
        return

    with open(gitignore, "r") as file:
        for line in file.readlines():
            line = line.strip()
            if line and not line.startswith("#"):
                add_exclusion_pattern(exclude_patterns, re.escape(line).replace("\\*", ".*"), "*")

def tree_directories ( path: Path = Path('.'), exclude_hashes: dict = exclusion_patterns, separator:chr = None, debug:bool = False) -> Generator:
    """
        Esta funcion retorna un generador el cual muestra todos los archivos
        que existen en el proyecto de forma recursiva, ignorando todo lo que
        este en exclude_hashes.

    Args:
        path(Path): Defaults to Path('.'), ruta desde donde inicia la busqueda
        exclude_hashes(dict): Defaults to hashes_ignore, diccionario que contiene
            los directorios y archivos a las cuales no se les calcurara el hash
        separator(char): Defaults to '/', separador del sistema, siendo '/' para linux
            y '\\' para windows
    """

    if separator is None:
        separator = ThisSysten().get_separator()

    for element in path.iterdir():
        split_element = str(element).split(separator)

        if any(re.match(pattern, str(element)) for pattern in exclude_hashes["*"]):
            continue

        if element.is_dir() and split_element not in exclude_hashes["directories"]:
            yield from tree_directories(element, exclude_hashes, separator)

        elif element.is_file() and split_element not in exclude_hashes["files"]:
            yield element

def get_hashes(tree_directories: Generator[Path, None, None] = tree_directories(), debug=False) -> dict:
    """
        Esta funcion obtiene los hashes de los archivos que devuelva el generador
        de tree_directories
    Args:
        tree_directories(Generador): Defaults to tree_directories(), este generador
            sera el que devuelva todos los archivos a los cuales se les tiene que calcular el hash
            los cuales serviran para verificar las actualizaciones
        debug(boolean): Defaults to False, esta bandera es para mostrar los archivos con sus
            respectivos hashes que se van generando.
    Returns:
        dict: diccionario con las las rutas(archivos) y sus respectivos hashes
    """
    hashes = {}
    for element in tree_directories:
        content = element.read_bytes()
        hash_string = md5(content).hexdigest()

        hashes.update({str(element): hash_string})

        if debug:
            print(f"hash del archivo ({Fore.LIGHTMAGENTA_EX}{element}{Fore.RESET}): {Fore.LIGHTGREEN_EX}{hash_string}{Fore.RESET}")

    return hashes

def print_tree (tree_directories: Generator[Path, None, None] = tree_directories()) -> None:
    for element in tree_directories:
        path = element.parent
        file = element.name
        print(f"[*] ruta -> ({Fore.LIGHTMAGENTA_EX}{path}{Fore.RESET}) archivo -> ({Fore.LIGHTGREEN_EX}{file}{Fore.RESET})")

def write_hashes(hashes:dict = None, file_name:str = "file.json") -> None:
    if hashes is None:
        return

    with open(file_name, 'w') as file:
        file.write(json.dumps(hashes, indent=4, ensure_ascii=False))

def check_updates(user="desmonHak", url="https://raw.githubusercontent.com/{}/LLU/main/file.json", filename="file_check_update.json", debug=False, fileCheck="file.json"):

    file = None
    useragents = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
        "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
        "Opera/9.20 (Windows NT 6.0; U; en)",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)",
        "Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
        "Mozilla/5.0 (compatible; Yahoo! Slurp/3.0; http://help.yahoo.com/help/us/ysearch/slurp)",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101209 Firefox/3.6.13"
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0b; Windows 98)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.8) Gecko/20100804 Gentoo Firefox/3.6.8",
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
        "Mozilla/5.0 (compatible; Googlebot/2.1; http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
        "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)"
    ]

    headers = {
        "User-Agent": useragents[randint(0, len(useragents)-1)],
        "accept": "*/*",
        "accept-encoding": "gzip;deflate;br"
    }

    try:
        response = request("GET", url.format(user), headers = headers)

        with open(filename, 'w') as file:
            file.write(response.text)

        file = response.text

        """carpetaDescargas = "{}{}{}".format(getcwd(), splas, tempDir)
        print(carpetaDescargas)
        archivo = ZipFile(BytesIO(response.content))
        archivo.extractall(carpetaDescargas)
        print(dir(archivo)    )
        if debug: print(archivo.printdir())


        # obtenemos el nombre de la carpeta donde esta todos los archivos descargados:
        file_name = archivo.infolist()[0].filename"""

        dataDownload = load_file(filename)
        dataOriginal = load_file(fileCheck)

        if len(dataDownload) != len(dataOriginal):

            print(f'Datos nuevos: {highlight(format_to_json(dataDownload), lexer= get_lexer_by_name("json"), formatter=Terminal256Formatter(style="dracula"))}\nDatos antiguos: {highlight(format_to_json(dataOriginal), lexer= get_lexer_by_name("json"), formatter=Terminal256Formatter(style="dracula"))}\nHubo cambios en el tamano de los archivos de hash\'h, por lo que hay actualizacion.')
            # son diferentes, retornar True, hay actualizacion
            return True
        else:
            for _hash in dataOriginal.keys():
                if _hash in dataDownload:
                    print(f"El hash ({Fore.LIGHTMAGENTA_EX}{dataDownload[_hash]}{Fore.RESET}) del archivo ({Fore.LIGHTGREEN_EX}{_hash}{Fore.RESET}) es correcto")
                else:
                    print("Al parecer hubo cambios de esta version ({})".format(_hash))
                    return True # hay hash's diferentes, actualizacion
            return False # si no se detecto hash's diferenetes y el diccionario es el mismo, no hay actualizacion

    except ConnectionError:
        print("No se pudo obtener los datos desde ({})".format(url.format(user)))

    if file is None:
        return file
    else:
        raise ConnectionError

if __name__ == "__main__":
    load_gitignore()
    print_tree()
    dict_hash_dir = get_hashes()
    write_hashes(dict_hash_dir)

