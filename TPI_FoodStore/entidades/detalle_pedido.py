from entidades.base import Base
from entidades.producto import Producto
from excepciones.errores import DatoInvalidoError


class DetallePedido(Base):
    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        self.__cantidad = cantidad
        self.__producto = producto
        self.__precio_unitario = producto.precio

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def subtotal(self) -> float:
        return self.__cantidad * self.__precio_unitario

    def sumar_cantidad(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        self.__cantidad += cantidad

    def __str__(self) -> str:
        return f"{self.producto.nombre} x {self.cantidad} = ${self.subtotal:.2f}"
