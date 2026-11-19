from datetime import date

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from entidades.enums import Estado, FormaPago
from entidades.producto import Producto
from entidades.usuario import Usuario
from excepciones.errores import DatoInvalidoError, OperacionNoPermitidaError, StockInsuficienteError


class Pedido(Base, Calculable):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario.eliminado:
            raise DatoInvalidoError("No se puede crear un pedido para un usuario dado de baja.")
        self.__usuario = usuario
        self.__fecha = date.today()
        self.__estado = Estado.PENDIENTE
        self.__total = 0.0
        self.__forma_pago = forma_pago
        self.__detalles: list[DetallePedido] = []

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @property
    def total(self) -> float:
        return self.__total

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        if self.estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se pueden agregar productos a un pedido pendiente.")
        if producto.eliminado or not producto.disponible:
            raise DatoInvalidoError("El producto no está disponible.")
        actual = self.buscar_detalle_por_producto(producto)
        cantidad_total = cantidad + (actual.cantidad if actual else 0)
        if cantidad_total <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
        if cantidad_total > producto.stock:
            raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}.")
        if actual:
            actual.sumar_cantidad(cantidad)
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        for detalle in self.__detalles:
            if detalle.producto == producto:
                self.__detalles.remove(detalle)
                return

    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)

    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        transiciones = {
            Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
            Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
            Estado.TERMINADO: set(),
            Estado.CANCELADO: set(),
        }
        if nuevo_estado not in transiciones[self.estado]:
            raise OperacionNoPermitidaError(
                f"No se permite pasar de {self.estado.name} a {nuevo_estado.name}."
            )
        self.__estado = nuevo_estado

    def cambiar_forma_pago(self, forma_pago: FormaPago) -> None:
        if self.estado not in {Estado.PENDIENTE, Estado.CONFIRMADO}:
            raise OperacionNoPermitidaError("No se cambia el pago de un pedido terminado o cancelado.")
        self.__forma_pago = forma_pago

    def __str__(self) -> str:
        return (f"{self.id} - {self.usuario.nombre} {self.usuario.apellido} | "
                f"{self.estado.name} | {self.forma_pago.name} | ${self.total:.2f} | {self.fecha}")
