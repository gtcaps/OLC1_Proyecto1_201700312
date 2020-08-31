from enum import Enum, auto

class TipoToken(Enum):
    IDENTIFICADOR = auto()
    PROPIEDAD = auto()
    NUMERO_ENTERO = auto()
    NUMERO_DECIMAL = auto()
    NUMERO_HEXADECIMAL = auto()
    CADENA = auto()
    LLAVE_IZQ = auto()
    LLAVE_DER = auto()
    PARENTESIS_IZQ = auto()
    PARENTESIS_DER = auto()
    PUNTO = auto()
    DOS_PUNTOS = auto()
    PUNTO_Y_COMA = auto()
    COMA = auto()
    ASTERISCO = auto()
    NUMERAL = auto()
    PORCENTAJE = auto()

