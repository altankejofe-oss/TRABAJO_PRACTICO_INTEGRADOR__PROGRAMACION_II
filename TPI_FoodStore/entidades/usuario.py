from entidades.base import Base
from entidades.enums import Rol
from excepciones.errores import DatoInvalidoError


class Usuario(Base):
    def __init__(self, nombre: str, apellido: str, mail: str, celular: str,
                 contrasena: str, rol: Rol) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasena = ""
        self.contrasena = contrasena
        self.rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        mail = valor.strip().lower()
        if not mail or "@" not in mail or "." not in mail.split("@")[-1]:
            raise DatoInvalidoError("El mail debe tener un formato básico válido.")
        self.__mail = mail

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El celular no puede estar vacío.")
        self.__celular = valor.strip()

    @property
    def contrasena(self) -> str:
        raise AttributeError("La contraseña no tiene acceso de lectura.")

    @contrasena.setter
    def contrasena(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("La contraseña no puede estar vacía.")
        self.__contrasena = valor

    def verificar_contrasena(self, contrasena: str) -> bool:
        return self.__contrasena == contrasena

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        if not isinstance(valor, Rol):
            raise DatoInvalidoError("El rol elegido no es válido.")
        self.__rol = valor

    def __str__(self) -> str:
        return f"{self.id} - {self.nombre} {self.apellido} | {self.mail} | {self.rol.name}"
