from entidades.enums import Rol
from entidades.usuario import Usuario
from excepciones.errores import CredencialesInvalidasError, DuplicadoError
from servicios.base_servicio import BaseServicio


class UsuarioServicio(BaseServicio[Usuario]):
    def crear(self, nombre: str, apellido: str, mail: str, celular: str,
              contrasena: str, rol: Rol) -> Usuario:
        mail = mail.strip().lower()
        if any(u.mail == mail for u in self.listar()):
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        usuario = Usuario(nombre, apellido, mail, celular, contrasena, rol)
        self.agregar(usuario)
        return usuario

    def editar(self, identificador: int, nombre: str, apellido: str, mail: str,
               celular: str, contrasena: str, rol: Rol) -> Usuario:
        usuario = self.buscar_por_id(identificador)
        mail = mail.strip().lower()
        if any(u.id != identificador and u.mail == mail for u in self.listar()):
            raise DuplicadoError("Ya existe un usuario con ese mail.")
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.mail = mail
        usuario.celular = celular
        if contrasena:
            usuario.contrasena = contrasena
        usuario.rol = rol
        return usuario

    def autenticar(self, mail: str, contrasena: str) -> Usuario:
        for usuario in self.listar():
            if usuario.mail == mail.strip().lower() and usuario.verificar_contrasena(contrasena):
                return usuario
        raise CredencialesInvalidasError("Mail o contraseña incorrectos.")

    def eliminar(self, identificador: int, sesion: Usuario) -> Usuario:
        usuario = self.buscar_por_id(identificador)
        if usuario.id == sesion.id:
            from excepciones.errores import OperacionNoPermitidaError
            raise OperacionNoPermitidaError("No puede eliminarse a sí mismo mientras tiene sesión.")
        return self.eliminar_logicamente(identificador)
