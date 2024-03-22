from .idiomas import Idiomas

class UnknownOS(Exception):
    def __init__(self, ThisOs, msg=None, idioma=Idiomas()):
        self.idioma = idioma
        if msg == None: self.msg = self.idioma.TextUnknownOS
        else: self.msg = msg
        
        self.ThisOS = ThisOs
        super().__init__(self.ThisOS)