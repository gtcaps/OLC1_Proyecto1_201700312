from enum import Enum, auto

class TipoToken(Enum):
    SUMA = auto()
    RESTA = auto()
    MULTIPLICACION = auto()
    DIVISION = auto()
    PARENTESIS_IZQ = auto()
    PARENTESIS_DER = auto()
    VARIABLE = auto()
    NUMERO = auto()