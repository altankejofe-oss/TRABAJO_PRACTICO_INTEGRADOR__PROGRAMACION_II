"""Demostraciones breves de reglas y errores del modelo y los servicios."""
from entidades.enums import Estado, FormaPago, Rol
from excepciones.errores import (CredencialesInvalidasError, DuplicadoError,
                                 OperacionNoPermitidaError, StockInsuficienteError)
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def comprobar(descripcion: str, condicion: bool) -> None:
    if not condicion:
        raise AssertionError(f"Falló: {descripcion}")
    print(f"OK - {descripcion}")


def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio()
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio()

    categoria = categorias.crear("Bebidas", "Bebidas frías")
    producto = productos.crear("Agua", "Botella de agua", 1000, 5,
                               "agua.jpg", True, categoria)
    cliente = usuarios.crear("Luz", "Díaz", "luz@example.com", "1112345678",
                             "clave", Rol.USUARIO)
    comprobar("Se pueden crear entidades", categoria.id > 0 and producto.id > 0)

    try:
        categorias.crear("bebidas", "Repetida")
    except DuplicadoError:
        comprobar("Se rechaza un nombre de categoría repetido", True)

    comprobar("Se autentica un usuario válido",
              usuarios.autenticar("luz@example.com", "clave") == cliente)
    try:
        usuarios.autenticar("luz@example.com", "incorrecta")
    except CredencialesInvalidasError:
        comprobar("Se rechazan credenciales incorrectas", True)

    try:
        pedidos.crear(cliente, FormaPago.EFECTIVO, [(producto, 6)])
    except StockInsuficienteError:
        comprobar("El pedido sin stock suficiente se cancela sin descontar unidades",
                  producto.stock == 5 and len(pedidos.listar()) == 0)

    pedido = pedidos.crear(cliente, FormaPago.TARJETA, [(producto, 2)])
    comprobar("El pedido calcula el total y descuenta stock", pedido.total == 2000 and producto.stock == 3)
    pedidos.cambiar_forma_pago(pedido.id, FormaPago.TRANSFERENCIA)
    comprobar("Se puede actualizar la forma de pago", pedido.forma_pago is FormaPago.TRANSFERENCIA)
    pedidos.cambiar_estado(pedido.id, Estado.CANCELADO)
    comprobar("Al cancelar el pedido se devuelve el stock", producto.stock == 5)
    try:
        pedidos.cambiar_estado(pedido.id, Estado.TERMINADO)
    except OperacionNoPermitidaError:
        comprobar("No se permiten transiciones inválidas", pedido.estado is Estado.CANCELADO)

    print("\nTodas las demostraciones terminaron correctamente.")


if __name__ == "__main__":
    main()
