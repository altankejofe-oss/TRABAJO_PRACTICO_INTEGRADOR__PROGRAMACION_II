from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar


class Base(ABC):
    """Atributos que comparten las entidades principales."""

    _proximo_id: ClassVar[int] = 1

    def __init__(self) -> None:
        self.__id: int = Base._proximo_id
        Base._proximo_id += 1
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    def dar_de_baja(self) -> None:
        self.__eliminado = True

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    @abstractmethod
    def __str__(self) -> str:
        """Devuelve una descripción para mostrar en consola."""
        raise NotImplementedError

    def __eq__(self, otro: object) -> bool:
        return isinstance(otro, Base) and self.id == otro.id

    def __hash__(self) -> int:
        return hash(self.id)
