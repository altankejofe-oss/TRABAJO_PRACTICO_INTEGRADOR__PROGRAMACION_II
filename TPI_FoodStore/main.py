from consola.menu import crear_menu
from entidades.enums import FormaPago, Rol
from entidades.usuario import Usuario
from excepciones.errores import CredencialesInvalidasError, FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio


def cargar_datos_iniciales(categorias: CategoriaServicio,
                           productos: ProductoServicio,
                           usuarios: UsuarioServicio) -> None:
    """Crea datos de ejemplo en memoria para poder probar el menú."""
    categoria = categorias.crear("Platos", "Comidas principales")
    productos.crear("Hamburguesa clásica", "Carne, lechuga y tomate", 4500, 10,
                    "hamburguesa.jpg", True, categoria)
    productos.crear("Ensalada fresca", "Verduras de estación", 3200, 6,
                    "ensalada.jpg", True, categoria)
    usuarios.crear("Ana", "Pérez", "admin@foodstore.com", "1100000000",
                   "admin123", Rol.ADMIN)
    usuarios.crear("Juan", "Gómez", "cliente@foodstore.com", "1199999999",
                   "cliente123", Rol.USUARIO)


def iniciar_sesion(usuarios: UsuarioServicio) -> Usuario | None:
    print("\n=== FOOD STORE - INICIO DE SESIÓN ===")
    for intento in range(1, 4):
        mail = input("Mail: ").strip()
        contrasena = input("Contraseña: ").strip()
        try:
            usuario = usuarios.autenticar(mail, contrasena)
            print(f"\nBienvenido/a, {usuario.nombre} {usuario.apellido} [{usuario.rol.name}]")
            return usuario
        except CredencialesInvalidasError:
            print("Mail o contraseña incorrectos.")
            if intento == 3:
                print("Se agotaron los tres intentos. El programa termina.")
                return None
    return None


def main() -> None:
    categorias = CategoriaServicio()
    productos = ProductoServicio()
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio()
    cargar_datos_iniciales(categorias, productos, usuarios)

    while True:
        usuario = iniciar_sesion(usuarios)
        if usuario is None:
            break
        menu = crear_menu(usuario, categorias, productos, usuarios, pedidos)
        try:
            continuar = menu.mostrar()
        except FoodStoreError as error:
            print(f"Error: {error}")
            continuar = True
        if not continuar:
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()
