from os         import getcwd, mkdir
from os.path    import exists, join
from getpass    import _raw_input
from ast        import literal_eval

from fram_package.get_info_system   import ThisSysten
from fram_package.idiomas           import Idiomas
from fram_package.error             import UnknownOS

class ConfUser:
    def __init__(self):
        self.info_system = ThisSysten()
        self.lenguaje    = None # establecer en None, esto permite a la clase ParserClass
                                # determinar el lenguaje a usar por defecto
        self.__conf_file_user__ = join(getcwd(), "conf", "init.json")
        self.data_conf   = self.loadConfFile()
        
    def createConfFileInit(self, file_path):
        print(file_path)
        if self.info_system.this_platform == "linux":
            from os import mknod
            mknod(file_path) # ?
            
        with open(file_path) as file:
            file.write("{}")

    def loadDefaultValue(self):
        # self.lenguaje = Idiomas()
        self.lenguaje = "es_ES"
        
    def loadConfFile(self):
        data_conf = None
        if exists(join(getcwd(), "conf")):
            if not exists(self.__conf_file_user__):
                # si no existe el archivo init.json crearlo
                if "y" in _raw_input( "desea crear un archivo de configuracion init.json?(y/n): " ).lower().split(" "):
                    self.createConfFileInit(self.__conf_file_user__)
            else:
                # si existe cargarlo
                with open(self.__conf_file_user__) as file:
                    try: 
                        data_conf = literal_eval(file.read())
                        
                    except SyntaxError:
                        print(f"El archivo {self.__conf_file_user__} no contiene una sintaxis correcta.\nCorigalo o borre el archivo. Cargando los valores por defecto")
                        # self.loadDefaultValue()
                        return False  # error
                    
                #try: self.lenguaje = Idiomas(data_conf["lenguaje"])  
                try: self.lenguaje = data_conf["lenguaje"] 
                except KeyError: print(f"No se establecido ningun lenguaje en {self.__conf_file_user__}") # self.loadDefaultValue()
        else:
            print(f"Creando el directorio: {join(getcwd(), 'conf')}")
            mkdir(join(getcwd(), "conf"))
            self.createConfFileInit(self.__conf_file_user__)
            self.loadConfFile()  # volver a cargar el archivo de configuracion una vez creado
    
        self.data_conf = data_conf
        return data_conf
                
