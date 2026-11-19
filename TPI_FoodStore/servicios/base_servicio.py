from typing import Generic, TypeVar

from entidades.base import Base
from excepciones.errores import EntidadNoEncontradaError

T = TypeVar("T", bound=Base)


class BaseServicio(Generic[T]):
    def __init__(self) -> None:
        self._elementos: list[T] = []

    def listar(self, incluir_eliminados: bool = False) -> list[T]:
        if incluir_eliminados:
            return list(self._elementos)
        return [elemento for elemento in self._elementos if not elemento.eliminado]

    def buscar_por_id(self, identificador: int) -> T:
        for elemento in self._elementos:
            if elemento.id == identificador and not elemento.eliminado:
                return elemento
        raise EntidadNoEncontradaError(f"No se encontró el elemento con id {identificador}.")

    def agregar(self, elemento: T) -> None:
        self._elementos.append(elemento)

    def eliminar_logicamente(self, identificador: int) -> T:
        elemento = self.buscar_por_id(identificador)
        elemento.dar_de_baja()
        return elemento
