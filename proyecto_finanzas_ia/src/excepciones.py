class ErrorFinanzas(Exception):
    """Excepción base para errores de la aplicación financiera."""


class ImporteInvalidoError(ErrorFinanzas):
    """Se lanza cuando un movimiento tiene un importe menor o igual a cero."""


class ErrorFormatoArchivo(ErrorFinanzas):
    """Se lanza cuando el archivo CSV no tiene las columnas requeridas."""