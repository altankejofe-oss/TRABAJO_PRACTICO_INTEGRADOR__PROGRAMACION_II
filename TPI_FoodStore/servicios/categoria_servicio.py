from entidades.categoria import Categoria
from entidades.producto import Producto
from excepciones.errores import DuplicadoError
from servicios.base_servicio import BaseServicio


class CategoriaServicio(BaseServicio[Categoria]):
    def crear(self, nombre: str, descripcion: str) -> Categoria:
        if any(c.nombre.casefold() == nombre.strip().casefold() for c in self.listar()):
            raise DuplicadoError("Ya existe una categoría con ese nombre.")
        categoria = Categoria(nombre, descripcion)
        self.agregar(categoria)
        return categoria

    def editar(self, identificador: int, nombre: str, descripcion: str) -> Categoria:
        categoria = self.buscar_por_id(identificador)
        if any(c.id != identificador and c.nombre.casefold() == nombre.strip().casefold()
               for c in self.listar()):
            raise DuplicadoError("Ya existe una categoría con ese nombre.")
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        return categoria

    def eliminar(self, identificador: int, productos: list[Producto]) -> None:
        categoria = self.buscar_por_id(identificador)
        activos = [p for p in productos if not p.eliminado and p.categoria == categoria]
        if activos:
            raise DuplicadoError(f"La categoría tiene {len(activos)} producto(s) activo(s).")
        self.eliminar_logicamente(identificador)
