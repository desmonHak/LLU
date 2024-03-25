from fram_package.error import UnknownOS
from sys                import platform, version_info

class ThisSysten:
    def __init__(self):
        self.this_platform  = self.get_platform()
        self.splas          = self.get_splas()
        self.version_python = [version_info.major, version_info.minor]

    def get_platform(self):
        if platform not in ["win32", "linux"]:
            raise UnknownOS(platform)

        return platform

    def get_splas(self):
        return '/' if (self.this_platform == "linux") else '\\'
