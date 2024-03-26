from os       import walk, path
from hashlib  import md5
from random   import randint
from requests import request, ConnectionError
from colorama import Fore
from json     import dumps

from pygments            import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers     import get_lexer_by_name

from fram_package.get_info_system import ThisSysten
from fram_package.error           import ConnectionError, NotFoundThisFile
from fram_package.load_conf_user  import literal_eval

excluir_directorios = [
    # directorios a excluir de la recopilacion
    "__pycache__",
    ".dist",
    ".vscode",
    ".git",
]
excluir_archivos = [
    # archivos a excluir de la recopilacion
    "__init__.py",
    "file_check_update.json",
    "file.json"
]

def load_file(file):
    """
        Cargamos el archivo json y lo formateamos a un dict
    Args:
        file (str): Nombre del archivo .json
    """
    
    try:
        file = open(file, "r")
        # convertimos el json en un ficionario
        _file = literal_eval(file.read())
        # cerrar el archivo 
        file.close()
    
        return _file
    except FileNotFoundError: 
        print("Archivo de configuracion no encontrado: {}".format(file))
        raise NotFoundThisFile(file)

def add_file_excluir(filename): excluir_archivos.append(filename)
def add_dir_excluir  (dirname): excluir_directorios.append(dirname)

def formater_to_json(data):
    return dumps(data, indent=4)

def get_directory(ruta=".", debug=False, excluir_dir=excluir_directorios):

    """

        Esta funcion obtiene la ruta de los archivos, y los
        archivos de forma recursiva y lo retorna en forma de diccionario
    Args:
        ruta (str, optional): Defaults to ".". ruta desde donde comenzar a listar
        debug (bool, optional): modo debug. Defaults to False. Permite activar el modo debug
        excluir_dir (list, optional): lista de directorios a excluir

    Raises:
        UnknownOS: Error que se lanza cuando la plataforma no puede ser identificada

    Returns:
        dict: diccionario con las rutas y los archivos, ruta:lista_archivos
    """

    arbol_directorios = dict()
    dire = list(walk(ruta, topdown=False))

    _ThisSysten = ThisSysten()
    for carpeta in dire:
        estado = 0 # variable para controlar cuando anadir o no cambios al diccionario
        # ('./.git/logs/refs/remotes/origin', [], ['HEAD'])

        ruta_format_list = carpeta[0].split(_ThisSysten.splas)
        # (".", "frames", "__pycache__")

        for carpetaAExcluir in excluir_dir:
            if carpetaAExcluir in ruta_format_list:
                estado = 1 # si se encontro el nombre de la carpeta a excluir en la ruta, se pone
                # la variable estado a 1 para no anadirlo al bucle
                break

        if estado == 0:
            arbol_directorios.update({carpeta[0]:carpeta[2]})

    return arbol_directorios

def print_tree(tree_dir, excluir_files=False):
    """
        Imprimimos la ruta y cada archivo de un arbol en formato diccionaario
    Args:
        tree_dir (dict): arbol diccionario con archivos y rutas
    """
    for ruta in tree_dir.keys():
        #print("-> {}".format(ruta))
            for archivo in tree_dir[ruta]:
                if excluir_files and archivo not in excluir_files:
                    print(f"[*] ruta -> ({Fore.LIGHTMAGENTA_EX}{ruta}{Fore.RESET}) archivo -> ({Fore.LIGHTGREEN_EX}{archivo}{Fore.RESET})")

def get_hash(tree_dir, debug=False, excluir_files=excluir_archivos):
    """
        Esta funcion obtiene los hash's de los archivos de un arbol de archivos
        y los almacena en un dicionario
    Args:
        tree_dir (dict): arbol de directorios
        debug (bool, optional): modo debug. Defaults to False.
        excluir_files (list, optional): lista de archivos a excluir

    Raises:
        UnknownOS: error que ocurre cuando la plataforma no puede identificarse

    Returns:
        dict: se retorna un diccionario con los hash y la ruta mas el archivo, hash:archivo_ruta
    """
    dict_hash_dir = dict()
    # _ThisSysten = ThisSysten()

    for ruta in tree_dir.keys():
        for archivo in tree_dir[ruta]:
            #print(archivo, archivo in excluir_files)
            if (archivo not in excluir_files):
                # si el archivo no se encuentra en la lista de archivos a excluir lo anadimos

                _file_ = path.join(ruta, archivo)

                with open(_file_, "rb") as file:
                    hashString = md5(file.read()).hexdigest()

                    if debug:
                        print(f"hash del archivo ({Fore.LIGHTMAGENTA_EX}{_file_}{Fore.RESET}): {Fore.LIGHTGREEN_EX}{hashString}{Fore.RESET}")

                dict_hash_dir.update({_file_:hashString})
    print(highlight(formater_to_json(dict_hash_dir), lexer= get_lexer_by_name("json"), formatter=Terminal256Formatter(style="dracula")))

    return dict_hash_dir

def print_dict_hash_dir(dict_hash_dir):
    """
        Se imprime un diccionario de hash's y archivos
    Args:
        dict_hash_dir (dict): diccionario de hash's y archivos
    """
    for _hash in dict_hash_dir.keys():
        print(f"hash -> ({Fore.LIGHTGREEN_EX}{_hash}{Fore.RESET}) ruta -> ({Fore.LIGHTMAGENTA_EX}{dict_hash_dir[_hash]}{Fore.RESET})")

def write_dict_hash_dir(dict_hash_dir, file_name="file.json"):
    """
        Se escribe los datos de un diccionario hash's y archivos en formato json,
        por defecto en un archivo llamado "file.json"
    Args:
        dict_hash_dir (dict): diccionario de hash's y archivos
        file_name (str, optional): nombre del archivo .json de salida. Defaults to "file.json".
    """
    _file = open(file_name, "w")
    _file.write(str(dict_hash_dir))
    _file.close()

def check_updates(users=["desmonHak"], url="https://raw.githubusercontent.com/{}/LLU/main/file.json", filename="file_check_update.json", debug=False, fileCheck="file.json"):
    
    _file = None
    for user in users:
        
        try:
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
            response = request("GET", url.format(user), headers = headers)
            
            _file = open(filename, "w")
            _file.write(response.text)
            _file.close()
            
            _file = response.text
            
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
                
                print(f'Datos nuevos: {highlight(formater_to_json(dataDownload), lexer= get_lexer_by_name("json"), formatter=Terminal256Formatter(style="dracula"))}\nDatos antiguos: {highlight(formater_to_json(dataOriginal), lexer= get_lexer_by_name("json"), formatter=Terminal256Formatter(style="dracula"))}\nA habido cambios en el tamano de los archivos de hash\'h, por lo que hay actualizacion.')
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
            
            break
        except ConnectionError:
            print("No se pudo obtener los datos desde ({})".format(url.format(user)))
        
    if _file != None: return _file
    else: raise ConnectionError

if __name__ == "__main__":

    tree_dir = get_directory(debug=False)
    print_tree(tree_dir, excluir_files=excluir_archivos)

    dict_hash_dir = get_hash(tree_dir)
    print_dict_hash_dir(dict_hash_dir)
    write_dict_hash_dir(dict_hash_dir)
