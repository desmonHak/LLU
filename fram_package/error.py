from .idiomas import Idiomas

class UnknownOS(Exception):
    def __init__(self, ThisOs, msg=None, idioma=Idiomas()):
        self.idioma = idioma

        self.msg = self.idioma.TextUnknownOS if (msg is None) else msg

        self.ThisOS = ThisOs
        super().__init__(self.ThisOS)
        
class ErrorDeConexion(Exception):
    def __init__(self, msg=None, idioma=Idiomas()):
        self.idioma = idioma
        if msg == None: self.msg = self.idioma.TextErrorDeConexion
        else: self.msg = msg
        
        super().__init__()
        
class NotFoundThisFile(Exception):
    def __init__(self, file, msg=None, idioma=Idiomas()):
        self.idioma = idioma
        if msg == None: self.msg = self.idioma.TextNotFoundThisFile
        else: self.msg = msg
        
        self.file = file
        super().__init__(self.file)