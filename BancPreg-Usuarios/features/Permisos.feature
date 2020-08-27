Feature: Permisos

Scenario Outline: Reconocer Permisos
  Given un <name> para definir
  When se obtiene el permiso
  Then el <greet> corresponde al nombre

  Examples: nombres
  | name        | greet                                 |
  | juan        | Permisos de juan (docente)            |
  | maria       | Permisos de maria (docente)           |
  | ana         | Permisos de ana (docente)             |
  | admin       | Permisos de administrador concedidos  |

Scenario Outline: Crear Registro
  Given un <user> para crear
  When se solicita insertarlo en la db
  Then el <message> corresponde

  Examples: user
  | user        | message |
  | juan        | Exito al insertar [Usuario juan] |
  | juan        | ErrorYa existe ese email de usuario |
  | maria       | Exito al insertar [Usuario maria] |
  | ana         | Exito al insertar [Usuario ana] |
  | admin       | Exito al insertar [Usuario admin] |
  | ana         | ErrorYa existe ese email de usuario |

Scenario Outline: Iniciar Sesion
  Given un <user> con su <key>
  When intenta validar su identidad
  Then se le da un <uphold>

  Examples: user
  | user     | key        | uphold                                     |
  | 1        | juan144000 | Permisos de juan (docente)                 |
  | 1        | juan144001 | No existe un usuario con los datos pedidos |