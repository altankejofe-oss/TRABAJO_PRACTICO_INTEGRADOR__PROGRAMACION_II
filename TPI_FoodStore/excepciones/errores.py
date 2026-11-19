class FoodStoreError(Exception):
    """Clase base para los errores esperados del negocio."""


class EntidadNoEncontradaError(FoodStoreError):
    pass


class DatoInvalidoError(FoodStoreError):
    pass


class PrecioInvalidoError(DatoInvalidoError):
    pass


class StockInsuficienteError(FoodStoreError):
    pass


class DuplicadoError(FoodStoreError):
    pass


class OperacionNoPermitidaError(FoodStoreError):
    pass


class CredencialesInvalidasError(FoodStoreError):
    pass
