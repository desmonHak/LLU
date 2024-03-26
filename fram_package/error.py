from .idiomas import Idiomas

class UnknownOS(Exception):
    def __init__(self, ThisOs, msg=None, idioma=Idiomas()):
        self.idioma = idioma
        
        self.msg = self.idioma.idioma_data["error.py"]["TextUnknownOS"] if (msg is None) else msg

        self.ThisOS = ThisOs
        super().__init__(self.msg)
        
class ConnectionError(Exception):
    def __init__(self, msg=None, idioma=Idiomas()):
        self.idioma = idioma
        self.msg = self.idioma.idioma_data["error.py"]["ConnectionError"] if (msg is None) else msg
        
        super().__init__(self.msg)
        
class NotFoundThisFile(Exception):
    def __init__(self, file, msg=None, idioma=Idiomas()):
        self.idioma = idioma
        self.msg = self.idioma.idioma_data["error.py"]["NotFoundThisFile"] if (msg is None) else msg
        self.msg = self.msg.format(file)
        
        self.file = file
        super().__init__(self.msg)
        
class KeyValueErrorConfUser(Exception):
    def __init__(self, key, file_conf_user, msg="La key {} no se encontro en {}", idioma=Idiomas()):
        self.idioma = idioma

        self.file_conf_user = file_conf_user
        self.key = key

        self.msg = self.idioma.idioma_data["error.py"]["NotFoundThisFile"] if (msg is None) else msg
        self.msg = self.msg.format(self.key, self.file_conf_user)

        super().__init__(self.msg)