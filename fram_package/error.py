from .idiomas import Idiomas

class UnknownOS(Exception):
    def __init__(self, ThisOs, msg=None, idioma=Idiomas()):
        self.idioma = idioma

        self.msg = self.idioma.TextUnknownOS if (msg is None) else msg

        self.ThisOS = ThisOs
        super().__init__(self.ThisOS)