class Idiomas:
    
    def __init__(self, idioma="es_ES"):
        """_summary_

            Por defecto, el idioma es Espanol

        Args:
            idioma (str, optional): _description_. Defaults to "es_ES".

        Raises:
            Exception: _description_
        """
        
        self.es_ES = "es_ES" # Espanol
        self.en_US = "en_US" # Ingles
        self.zh_CN = "zh_CN" # Chino
        self.ru_RU = "ru_RU" # Ruso 
        self.fr_FR = "fr_FR" # Frances(Francia)
        self.ar_EG = "ar_EG" # Arabe Egipto(el mas similar al estandar)
        self.ja_JP = "ja_JP" # Japones
        self.de_DE = "de_DE" # Aleman(Alemania)
        self.esperanto = "esperanto" # esperanto
        
        self.ALL_LENGUAJE = [
            self.es_ES, 
            self.en_US, 
            self.zh_CN,
            self.ru_RU,
            self.fr_FR,
            self.ar_EG,
            self.ja_JP,
            self.de_DE,
            self.esperanto
        ]
        
        self.idioma = idioma
        #print(self.idioma)
        
        if self.es_ES == self.idioma: # Espanol
            # textos de errores:
            self.TextUnknownOS = "No se pudo identificar el OS en el que se esta trabajando."
            
        elif self.en_US == self.idioma: # Ingles
            self.TextUnknownOS = "Could not identify the OS being worked on"
            
        elif self.zh_CN == self.idioma: # Chino
            self.TextUnknownOS = "无法识别正在使用的操作系统"
            
        elif self.ru_RU == self.idioma: # Ruso 
            self.TextUnknownOS = "Не удалось определить ОС, над которой ведется работа"

        elif self.fr_FR == self.idioma: # Frances(Francia)
            self.TextUnknownOS = "Impossible d'identifier le système d'exploitation sur lequel on travaille"
            
        elif self.ar_EG == self.idioma: # Arabe Egipto(el mas similar al estandar)
            self.TextUnknownOS = "تعذر تحديد نظام التشغيل قيد العمل"

        elif self.ja_JP == self.idioma: # Japones
            self.TextUnknownOS = "動作しているOSを特定できませんでした"

        elif self.de_DE == self.idioma: # Aleman(Alemania)
            self.TextUnknownOS = "Das Betriebssystem, an dem gearbeitet wird, konnte nicht identifiziert werden"
      
        elif self.esperanto == self.idioma: # esperanto
            self.TextUnknownOS = "Ne eblis identigi la OS prilaborata"
    
        else:
            raise Exception("Este idioma no se encuentra {}".format(self.idioma))
            
    def setIdioma(self, idioma):
        """_summary_
            Esta funcion cambia de idioma el programa
        Args:r
            idioma (str): se recibe el idioma a cambiar
        """
        print("Cambiando de idioma a:"+idioma)
        self.__init__(idioma)