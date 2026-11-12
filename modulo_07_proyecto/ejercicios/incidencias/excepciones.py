"""Excepciones del gestor de incidencias.

Jerarquía que hay que definir:

    ErrorDeIncidencias (Exception)      base de todos los errores de la aplicación
    ├── DatosNoValidos                  un dato de una incidencia no vale
    ├── IncidenciaNoEncontrada          no existe una incidencia con ese identificador
    ├── TransicionNoValida              el cambio de estado no está permitido
    └── ErrorDeAlmacen                  el fichero de datos no se puede leer

``IncidenciaNoEncontrada(identificador)`` guarda el identificador en el
atributo ``identificador`` y su mensaje es "No existe la incidencia 7".

``TransicionNoValida(actual, nuevo)`` guarda los dos estados en los atributos
``actual`` y ``nuevo`` y su mensaje es "No se puede pasar de cerrada a abierta".
"""

# TODO: define aquí las cinco excepciones
