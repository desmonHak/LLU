from fram_package.error import UnknownOS
from sys                import platform, version_info

class ThisSysten:
    def __init__(self):
        self.this_platform  = self.get_platform()
        self.splas          = self.get_splas()
        self.version_python = [version_info.major, version_info.minor]

    def get_platform(self) -> str:
        """
                    descripcion
                Args:
                    args1 (type_args1): descripcion args
                    args2 (type_args2, optional): descripcion args.
                    args3 (type_args3, optional): descripcion args

                Raises:
                    UnknownOS: error que ocurre cuando la plataforma no puede identificarse

                Returns:
                    type_return: descripcion del valor retornado
        """
        if platform not in ["win32", "linux"]:
            raise UnknownOS(platform)

        return platform

    def get_splas(self) -> str:
        """
                    descripcion
                Args:
                    args1 (type_args1): descripcion args
                    args2 (type_args2, optional): descripcion args.
                    args3 (type_args3, optional): descripcion args

                Raises:
                    UnknownOS: error que ocurre cuando la plataforma no puede identificarse

                Returns:
                    type_return: descripcion del valor retornado
        """
        return '/' if (self.this_platform == "linux") else '\\'
