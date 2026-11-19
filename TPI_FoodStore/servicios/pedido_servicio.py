from entidades.enums import Estado, FormaPago
from entidades.pedido import Pedido
from entidades.producto import Producto
from entidades.usuario import Usuario
from excepciones.errores import DatoInvalidoError, OperacionNoPermitidaError, StockInsuficienteError
from servicios.base_servicio import BaseServicio


class PedidoServicio(BaseServicio[Pedido]):
    def crear(self, usuario: Usuario, forma_pago: FormaPago,
              lineas: list[tuple[Producto, int]]) -> Pedido:
        """Valida todas las líneas antes de guardar el pedido o tocar el stock."""
        if not lineas:
            raise DatoInvalidoError("El pedido debe tener al menos un producto.")
        cantidades: dict[int, int] = {}
        productos: dict[int, Producto] = {}
        for producto, cantidad in lineas:
            if cantidad <= 0:
                raise DatoInvalidoError("La cantidad debe ser mayor que cero.")
            if producto.eliminado or not producto.disponible:
                raise DatoInvalidoError(f"{producto.nombre} no está disponible.")
            cantidades[producto.id] = cantidades.get(producto.id, 0) + cantidad
            productos[producto.id] = producto
        for identificador, cantidad in cantidades.items():
            producto = productos[identificador]
            if cantidad > producto.stock:
                raise StockInsuficienteError(f"Stock insuficiente para {producto.nombre}.")

        pedido = Pedido(usuario, forma_pago)
        for identificador, cantidad in cantidades.items():
            pedido.agregar_detalle(cantidad, productos[identificador])
        pedido.calcular_total()
        for identificador, cantidad in cantidades.items():
            producto = productos[identificador]
            producto.stock -= cantidad
        self.agregar(pedido)
        return pedido

    def cambiar_estado(self, identificador: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(identificador)
        pedido.cambiar_estado(nuevo_estado)
        if nuevo_estado is Estado.CANCELADO:
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
        return pedido

    def cambiar_forma_pago(self, identificador: int, forma_pago: FormaPago) -> Pedido:
        pedido = self.buscar_por_id(identificador)
        pedido.cambiar_forma_pago(forma_pago)
        return pedido

    def eliminar(self, identificador: int) -> Pedido:
        pedido = self.buscar_por_id(identificador)
        if pedido.estado not in {Estado.TERMINADO, Estado.CANCELADO}:
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
            pedido.cambiar_estado(Estado.CANCELADO)
        pedido.dar_de_baja()
        for detalle in pedido.detalles:
            detalle.dar_de_baja()
        return pedido

    def listar_de_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [pedido for pedido in self.listar() if pedido.usuario == usuario]

    def ver_detalles(self, identificador: int, usuario: Usuario | None = None) -> Pedido:
        pedido = self.buscar_por_id(identificador)
        if usuario is not None and pedido.usuario != usuario:
            raise OperacionNoPermitidaError("El pedido indicado no pertenece a este usuario.")
        return pedido
