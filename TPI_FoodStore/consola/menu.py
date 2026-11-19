from abc import ABC, abstractmethod
from typing import Callable

from entidades.categoria import Categoria
from entidades.enums import Estado, FormaPago, Rol
from entidades.producto import Producto
from entidades.usuario import Usuario
from excepciones.errores import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.pedido_servicio import PedidoServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from consola.entrada import pedir_decimal, pedir_entero, pedir_enum, pedir_si_no, pedir_texto


class Menu(ABC):
    def __init__(self, usuario: Usuario, categorias: CategoriaServicio,
                 productos: ProductoServicio, usuarios: UsuarioServicio,
                 pedidos: PedidoServicio) -> None:
        self.usuario = usuario
        self.categorias = categorias
        self.productos = productos
        self.usuarios = usuarios
        self.pedidos = pedidos

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra opciones. True cierra sesión y False termina el programa."""
        raise NotImplementedError

    def ejecutar_seguro(self, accion: Callable[[], None]) -> None:
        try:
            accion()
        except FoodStoreError as error:
            print(f"Error: {error}")
        except ValueError:
            print("El dato ingresado no tiene un formato válido.")

    def listar_categorias(self) -> None:
        elementos = self.categorias.listar()
        if not elementos:
            print("No hay categorías cargadas.")
        for elemento in elementos:
            print(elemento)

    def listar_productos_admin(self) -> None:
        elementos = self.productos.listar()
        if not elementos:
            print("No hay productos cargados.")
        for elemento in elementos:
            print(elemento)

    def seleccionar_categoria(self) -> Categoria:
        self.listar_categorias()
        return self.categorias.buscar_por_id(pedir_entero("Id de categoría: ", 1))

    def seleccionar_producto(self) -> Producto:
        self.listar_productos_admin()
        return self.productos.buscar_por_id(pedir_entero("Id de producto: ", 1))

    def seleccionar_usuario(self) -> Usuario:
        for usuario in self.usuarios.listar():
            print(usuario)
        return self.usuarios.buscar_por_id(pedir_entero("Id de usuario: ", 1))


class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - ADMINISTRADOR ({self.usuario.nombre}) ===")
            print("1. Categorías\n2. Productos\n3. Usuarios\n4. Pedidos\n9. Cerrar sesión\n0. Salir")
            opcion = pedir_entero("Seleccione: ", 0)
            if opcion == 0:
                return False
            if opcion == 9:
                return True
            acciones = {1: self.menu_categorias, 2: self.menu_productos,
                        3: self.menu_usuarios, 4: self.menu_pedidos}
            accion = acciones.get(opcion)
            if accion:
                self.ejecutar_seguro(accion)
            else:
                print("Opción inexistente.")

    def menu_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver")
            opcion = pedir_entero("Seleccione: ", 0)
            if opcion == 0:
                return
            if opcion == 1:
                self.listar_categorias()
            elif opcion == 2:
                creada = self.categorias.crear(pedir_texto("Nombre: "), pedir_texto("Descripción: "))
                print(f"Categoría creada con id {creada.id}.")
            elif opcion == 3:
                self.listar_categorias()
                identificador = pedir_entero("Id a editar: ", 1)
                actual = self.categorias.buscar_por_id(identificador)
                nombre = pedir_texto(f"Nombre [{actual.nombre}]: ", True) or actual.nombre
                descripcion = pedir_texto(f"Descripción [{actual.descripcion}]: ", True) or actual.descripcion
                self.categorias.editar(identificador, nombre, descripcion)
                print("Categoría actualizada.")
            elif opcion == 4:
                self.listar_categorias()
                identificador = pedir_entero("Id a eliminar: ", 1)
                if pedir_si_no("¿Confirma la baja lógica?"):
                    self.categorias.eliminar(identificador, self.productos.listar(incluir_eliminados=True))
                    print("Categoría dada de baja.")

    def menu_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver")
            opcion = pedir_entero("Seleccione: ", 0)
            if opcion == 0:
                return
            if opcion == 1:
                self.listar_productos_admin()
            elif opcion == 2:
                self.listar_categorias()
                categoria = self.seleccionar_categoria()
                creado = self.productos.crear(
                    pedir_texto("Nombre: "), pedir_texto("Descripción: "),
                    pedir_decimal("Precio: "), pedir_entero("Stock: "),
                    pedir_texto("Imagen (ruta o descripción): ", True),
                    pedir_si_no("¿Está disponible?"), categoria)
                print(f"Producto creado con id {creado.id}.")
            elif opcion == 3:
                producto = self.seleccionar_producto()
                nombre = pedir_texto(f"Nombre [{producto.nombre}]: ", True) or producto.nombre
                descripcion = pedir_texto(f"Descripción [{producto.descripcion}]: ", True) or producto.descripcion
                texto_precio = pedir_texto(f"Precio [{producto.precio}]: ", True)
                precio = float(texto_precio.replace(",", ".")) if texto_precio else producto.precio
                texto_stock = pedir_texto(f"Stock [{producto.stock}]: ", True)
                stock = int(texto_stock) if texto_stock else producto.stock
                imagen = pedir_texto(f"Imagen [{producto.imagen}]: ", True) or producto.imagen
                disponible = pedir_si_no("¿Cambiar disponibilidad? (S=disponible, N=no disponible)")
                categoria = self.seleccionar_categoria()
                self.productos.editar(producto.id, nombre, descripcion, precio, stock,
                                      imagen, disponible, categoria)
                print("Producto actualizado.")
            elif opcion == 4:
                producto = self.seleccionar_producto()
                if pedir_si_no("¿Confirma la baja lógica? (S/N)"):
                    self.productos.eliminar(producto.id)
                    print("Producto dado de baja.")

    def menu_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---\n1. Listar\n2. Crear\n3. Editar\n4. Eliminar\n0. Volver")
            opcion = pedir_entero("Seleccione: ", 0)
            if opcion == 0:
                return
            if opcion == 1:
                lista = self.usuarios.listar()
                if not lista:
                    print("No hay usuarios cargados.")
                for usuario in lista:
                    print(usuario)
            elif opcion == 2:
                creado = self.usuarios.crear(
                    pedir_texto("Nombre: "), pedir_texto("Apellido: "),
                    pedir_texto("Mail: "), pedir_texto("Celular: "),
                    pedir_texto("Contraseña: "), pedir_enum("Rol: ", Rol))
                print(f"Usuario creado con id {creado.id}.")
            elif opcion == 3:
                usuario = self.seleccionar_usuario()
                nombre = pedir_texto(f"Nombre [{usuario.nombre}]: ", True) or usuario.nombre
                apellido = pedir_texto(f"Apellido [{usuario.apellido}]: ", True) or usuario.apellido
                mail = pedir_texto(f"Mail [{usuario.mail}]: ", True) or usuario.mail
                celular = pedir_texto(f"Celular [{usuario.celular}]: ", True) or usuario.celular
                contrasena = pedir_texto("Nueva contraseña (vacía conserva la actual): ", True)
                rol = pedir_enum("Rol nuevo: ", Rol)
                self.usuarios.editar(usuario.id, nombre, apellido, mail, celular, contrasena, rol)
                print("Usuario actualizado.")
            elif opcion == 4:
                usuario = self.seleccionar_usuario()
                if pedir_si_no("¿Confirma la baja lógica? (S/N)"):
                    self.usuarios.eliminar(usuario.id, self.usuario)
                    print("Usuario dado de baja.")

    def menu_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---\n1. Listar\n2. Crear con detalles\n3. Cambiar estado o pago\n4. Eliminar\n0. Volver")
            opcion = pedir_entero("Seleccione: ", 0)
            if opcion == 0:
                return
            if opcion == 1:
                lista = self.pedidos.listar()
                if not lista:
                    print("No hay pedidos cargados.")
                for pedido in lista:
                    print(pedido)
            elif opcion == 2:
                usuarios_activos = [u for u in self.usuarios.listar() if u.rol is Rol.USUARIO]
                if not usuarios_activos:
                    print("Primero debe crear un usuario cliente.")
                    continue
                for usuario in usuarios_activos:
                    print(usuario)
                cliente = self.usuarios.buscar_por_id(pedir_entero("Id del cliente: ", 1))
                if cliente.rol is not Rol.USUARIO:
                    print("El pedido se debe asociar a un cliente.")
                    continue
                forma_pago = pedir_enum("Forma de pago: ", FormaPago)
                lineas = []
                while True:
                    self.listar_productos_admin()
                    producto = self.seleccionar_producto()
                    cantidad = pedir_entero("Cantidad: ", 1)
                    lineas.append((producto, cantidad))
                    if not pedir_si_no("¿Agregar otro producto?"):
                        break
                creado = self.pedidos.crear(cliente, forma_pago, lineas)
                print(f"Pedido {creado.id} creado. Total: ${creado.total:.2f}.")
            elif opcion == 3:
                for pedido in self.pedidos.listar():
                    print(pedido)
                identificador = pedir_entero("Id del pedido: ", 1)
                pedido = self.pedidos.buscar_por_id(identificador)
                print("1. Cambiar estado\n2. Cambiar forma de pago")
                tipo = pedir_entero("Seleccione: ", 0)
                if tipo == 1:
                    estado = pedir_enum("Seleccione estado: ", Estado)
                    self.pedidos.cambiar_estado(identificador, estado)
                elif tipo == 2:
                    forma = pedir_enum("Seleccione forma de pago: ", FormaPago)
                    self.pedidos.cambiar_forma_pago(identificador, forma)
                else:
                    print("Opción inexistente.")
                    continue
                print("Pedido actualizado.")
            elif opcion == 4:
                for pedido in self.pedidos.listar():
                    print(pedido)
                pedido = self.pedidos.buscar_por_id(pedir_entero("Id a eliminar: ", 1))
                if pedir_si_no("¿Confirma la baja lógica? (S/N)"):
                    self.pedidos.eliminar(pedido.id)
                    print("Pedido dado de baja.")


class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE - CLIENTE ({self.usuario.nombre}) ===")
            print("1. Ver categorías\n2. Ver productos disponibles\n3. Mis pedidos\n4. Mis datos\n9. Cerrar sesión\n0. Salir")
            opcion = pedir_entero("Seleccione: ", 0)
            if opcion == 0:
                return False
            if opcion == 9:
                return True
            acciones = {1: self.listar_categorias, 2: self.ver_productos,
                        3: self.ver_mis_pedidos, 4: self.ver_mis_datos}
            accion = acciones.get(opcion)
            if accion:
                self.ejecutar_seguro(accion)
            else:
                print("Opción inexistente.")

    def ver_productos(self) -> None:
        self.listar_categorias()
        filtro = pedir_texto("Id de categoría (Enter para todas): ", True)
        categoria_id = int(filtro) if filtro else None
        elementos = self.productos.listar_para_cliente(categoria_id)
        if not elementos:
            print("No hay productos disponibles con stock para mostrar.")
        for elemento in elementos:
            print(elemento)

    def ver_mis_pedidos(self) -> None:
        lista = self.pedidos.listar_de_usuario(self.usuario)
        if not lista:
            print("No hay pedidos cargados.")
        for pedido in lista:
            print(pedido)
        if lista and pedir_si_no("¿Consultar el detalle de un pedido?"):
            pedido = self.pedidos.ver_detalles(pedir_entero("Id del pedido: ", 1), self.usuario)
            for detalle in pedido.detalles:
                print(detalle)
            print(f"Total: ${pedido.total:.2f}")

    def ver_mis_datos(self) -> None:
        print(f"Nombre: {self.usuario.nombre} {self.usuario.apellido}")
        print(f"Mail: {self.usuario.mail}\nCelular: {self.usuario.celular}\nRol: {self.usuario.rol.name}")


def crear_menu(usuario: Usuario, categorias: CategoriaServicio,
               productos: ProductoServicio, usuarios: UsuarioServicio,
               pedidos: PedidoServicio) -> Menu:
    argumentos = (usuario, categorias, productos, usuarios, pedidos)
    if usuario.rol is Rol.ADMIN:
        return MenuAdministrador(*argumentos)
    return MenuCliente(*argumentos)
