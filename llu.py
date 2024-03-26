from sys import argv

from fram_package.main           import main
from fram_package.load_conf_user import literal_eval
from fram_package.loads_files    import *

with open("information.json", "r") as file:
    information = literal_eval(file.read())

__version__ = information["version"]
__doc__ = information["doc"]
__autor__ =  information["autor"]
__contribuidores__ = information["contribuidores"]

if __name__ == "__main__":

    tree_dir = get_directory(debug=False)
    
    if len(argv) <= 1:
        print_tree(tree_dir)
        dict_hash_dir = get_hash(tree_dir)
        write_dict_hash_dir(dict_hash_dir)

    if check_updates(): print("Hay una nueva version de este software!!!")

    main()

    
