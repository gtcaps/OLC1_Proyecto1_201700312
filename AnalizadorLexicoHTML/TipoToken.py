from enum import Enum, auto

class TipoToken(Enum):
    CADENA = auto()
    CADENA_HTML = auto()
    DIAGONAL = auto()
    IGUAL = auto()
    IDENTIFICADOR = auto()
    PALABRA_RESERVADA = auto()
    MENOR = auto()
    MAYOR = auto()