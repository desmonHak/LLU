from os  import getcwd, path
from ast import literal_eval
from sys import platform

class Idiomas:
    def __init__(self, idioma="es_ES"):
        """_summary_

            Por defecto, el idioma es Espanol

        Args:
            idioma (str, optional): _description_. Defaults to "es_ES".

        Raises:
            Exception: _description_
        """
        
        if idioma == None: self.idioma = "es_ES"
        else: self.idioma      = idioma

        self.es_ES = "es_ES"  # Espanol
        self.en_US = "en_US"  # Ingles
        self.zh_CN = "zh_CN"  # Chino
        self.ru_RU = "ru_RU"  # Ruso
        self.fr_FR = "fr_FR"  # Frances(Francia)
        self.ar_EG = "ar_EG"  # Arabe Egipto(el mas similar al estandar)
        self.ja_JP = "ja_JP"  # Japones
        self.de_DE = "de_DE"  # Aleman(Alemania)
        self.esperanto = "esperanto"  # esperanto

        self.ALL_LENGUAJE = [
            self.es_ES, self.en_US, self.zh_CN,
            self.ru_RU, self.fr_FR, self.ar_EG,
            self.ja_JP, self.de_DE, self.esperanto,
        ]

        self.idioma_data = self.loadLenguaje()
        self.ruta        = None
        # print(self.idioma)

    def getValKeyIdioma(self, key):
        try: return self.idioma_data[key]
        except KeyError: raise Exception("la key {} no se encuentra en {}".format( self.ruta + self.idioma + ".json" ))

    def loadLenguaje(self, ruta : dict = [getcwd() , "fram_package", "idiomas"]):
        
        # if platform == "win32" or platform == "linux":
        if platform in ["win32", "linux", "linux2"]: ruta = path.join(*ruta)
        else: Exception("Su sistema no pudo ser identificado {}".format(self.idioma))

        file = path.join(ruta, self.idioma + ".json")

        if not path.isfile(file): raise Exception("El archivo '{}' no se encuentra.".format(file))
        
        self.ruta = ruta
        
        with open(file, 'r') as file:
            try:
                return literal_eval(file.read())
            except SyntaxError:
                raise Exception("El archivo '{}' no tiene la sintaxis correcta".format(file))

    def setIdioma(self, idioma):
        """_summary_
            Esta funcion cambia de idioma el programa
        Args:r
            idioma (str): se recibe el idioma a cambiar
        """
        print("Cambiando de idioma a:" + idioma)
        self.__init__(idioma)
