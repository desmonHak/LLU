from sys import platform, version_info

from fram_package.error import UnknownOS

class ThisSysten:
    def __init__(self) -> None:
        self.this_platform  = None
        self.splas          = None
        self.version_python = [version_info.major, version_info.minor]
        self.get_platform()
        self.get_splas()

    def get_platform(self):
        if   platform == "win32":                         self.this_platform = "win32"
        elif platform == "linux" or platform == "linux2": self.this_platform = "linux"
        else:                                             raise UnknownOS(platform)
        return self.this_platform

    def get_splas(self):
        if   self.this_platform == None:    self.get_platform()
        if   self.this_platform == "win32": self.splas = "\\"
        elif self.this_platform == "linux": self.splas = "/"
        return self.splas


