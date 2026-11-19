from typing import Callable, TypeVar

from excepciones.errores import DatoInvalidoError

T = TypeVar("T")


def pedir_texto(mensaje: str, permitir_vacio: bool = False) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or permitir_vacio:
            return valor
        print("El dato no puede estar vacío.")


def pedir_entero(mensaje: str, minimo: int = 0) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"Ingrese un número igual o mayor que {minimo}.")
                continue
            return valor
        except ValueError:
            print("Ingrese un número entero válido.")


def pedir_decimal(mensaje: str, minimo: float = 0.0) -> float:
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))
            if valor < minimo:
                print(f"Ingrese un número igual o mayor que {minimo}.")
                continue
            return valor
        except ValueError:
            print("Ingrese un número válido.")


def pedir_opcion(mensaje: str, opciones: int) -> int:
    return pedir_entero(mensaje, 0) if opciones == 0 else _pedir_rango(mensaje, opciones)


def _pedir_rango(mensaje: str, maximo: int) -> int:
    while True:
        valor = pedir_entero(mensaje, 0)
        if valor <= maximo:
            return valor
        print(f"Elija una opción entre 0 y {maximo}.")


def pedir_si_no(mensaje: str) -> bool:
    while True:
        valor = input(f"{mensaje} (S/N): ").strip().upper()
        if valor in {"S", "N"}:
            return valor == "S"
        print("Responda S o N.")


def pedir_enum(mensaje: str, enum_tipo: type[T]) -> T:
    elementos = list(enum_tipo)
    for indice, elemento in enumerate(elementos, start=1):
        print(f"{indice}. {elemento.name}")
    numero = _pedir_rango(mensaje, len(elementos))
    if numero == 0:
        raise DatoInvalidoError("Debe elegir una opción de la lista.")
    return elementos[numero - 1]
