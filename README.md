# Food Store - TPI Programación

Sistema de consola para administrar categorías, productos, usuarios y pedidos.
Videos introductorio individual - https://www.youtube.com/watch?v=yXD7XFERdFw

## Ejecución

Desde la carpeta `TPI_FoodStore`, ejecutar:

```bash
python main.py
```

El sistema carga un usuario administrador inicial:

- Mail: `admin@foodstore.com`
- Contraseña: `admin123`
- Cliente de demostración: `cliente@foodstore.com` / `cliente123`

Se puede usar la opción de usuarios para crear cuentas cliente. La contraseña no se muestra al listar usuarios ni al consultar los datos propios.

## Pruebas de demostración

```bash
python pruebas.py
```

El archivo ejecuta ejemplos de creación de entidades, validaciones, autenticación, stock y transiciones de estado.

## Organización

- `entidades/`: clases del modelo y enumerados.
- `servicios/`: operaciones y reglas del negocio.
- `consola/`: menús, entrada validada y presentación.
- `excepciones/`: errores de negocio.
- `main.py`: creación de datos de ejemplo y arranque.
- `pruebas.py`: demostraciones automáticas de casos válidos y de error.
