from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.errores import DatoInvalidoError, DuplicadoError
from servicios.base_servicio import BaseServicio


class ProductoServicio(BaseServicio[Producto]):
    def crear(self, nombre: str, descripcion: str, precio: float, stock: int,
              imagen: str, disponible: bool, categoria: Categoria) -> Producto:
        if categoria.eliminado:
            raise DatoInvalidoError("La categoría está dada de baja.")
        producto = Producto(nombre, descripcion, precio, stock, imagen, disponible, categoria)
        self.agregar(producto)
        return producto

    def editar(self, identificador: int, nombre: str, descripcion: str, precio: float,
               stock: int, imagen: str, disponible: bool, categoria: Categoria) -> Producto:
        producto = self.buscar_por_id(identificador)
        if categoria.eliminado:
            raise DatoInvalidoError("La categoría está dada de baja.")
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock = stock
        producto.imagen = imagen
        producto.disponible = disponible
        producto.categoria = categoria
        return producto

    def eliminar(self, identificador: int) -> None:
        self.eliminar_logicamente(identificador)

    def listar_para_cliente(self, categoria_id: int | None = None) -> list[Producto]:
        return [p for p in self.listar() if p.disponible and p.stock > 0
                and (categoria_id is None or p.categoria.id == categoria_id)]
