from os      import walk, path
from hashlib import md5

from fram_package.get_info_system import ThisSysten

excluir_directorios = [
    # directorios a excluir de la recopilacion
    "__pycache__",
    ".dist",
    ".vscode",
    ".git",
    "fram_package",
]
excluir_archivos = [
    # archivos a excluir de la recopilacion
    "__init__.py",
    "file.json",
    "get_hash.py",
    "file_check_update.json",
    "fram.py",
    "loads_files.py"
]

def add_file_excluir(filename): excluir_archivos.append(filename)
def add_dir_excluir  (dirname): excluir_directorios.append(dirname)

def get_directory(ruta=".", debug=False, excluir_dir=excluir_directorios):

    """_summary_

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
    """_summary_
        Imprimimos la ruta y cada archivo de un arbol en formato diccionaario
    Args:
        tree_dir (dict): arbol diccionario con archivos y rutas
    """
    for ruta in tree_dir.keys():
        #print("-> {}".format(ruta))
            for archivo in tree_dir[ruta]:
                if excluir_files and archivo not in excluir_files:
                    print("[*] ruta -> ({}) archivo -> ({})".format(ruta, archivo))

def get_hash(tree_dir, debug=False, excluir_files=excluir_archivos):
    """_summary_
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
            print(archivo, archivo in excluir_files)
            if (archivo not in excluir_files):
                # si el archivo no se encuentra en la lista de archivos a excluir lo anadimos

                _file_ = path.join(ruta, archivo)

                with open(_file_, "rb") as file:
                    hashString = md5(file.read()).hexdigest()

                    if debug:
                        print("hash del archivo ({}): {}".format(_file_, hashString))

                dict_hash_dir.update({_file_:hashString})
                print(dict_hash_dir)

    return dict_hash_dir

def print_dict_hash_dir(dict_hash_dir):
    """_summary_
        Se imprime un diccionario de hash's y archivos
    Args:
        dict_hash_dir (dict): diccionario de hash's y archivos
    """
    for _hash in dict_hash_dir.keys():
        print("hash -> ({}) ruta -> ({})".format(_hash, dict_hash_dir[_hash]))

def write_dict_hash_dir(dict_hash_dir, file_name="file.json"):
    """_summary_
        Se escribe los datos de un diccionario hash's y archivos en formato json,
        por defecto en un archivo llamado "file.json"
    Args:
        dict_hash_dir (dict): diccionario de hash's y archivos
        file_name (str, optional): nombre del archivo .json de salida. Defaults to "file.json".
    """
    _file = open(file_name, "w")
    _file.write(str(dict_hash_dir))
    _file.close()

if __name__ == "__main__":

    tree_dir = get_directory(debug=False)
    print_tree(tree_dir, excluir_files=excluir_archivos)

    dict_hash_dir = get_hash(tree_dir)
    print_dict_hash_dir(dict_hash_dir)
    write_dict_hash_dir(dict_hash_dir)
