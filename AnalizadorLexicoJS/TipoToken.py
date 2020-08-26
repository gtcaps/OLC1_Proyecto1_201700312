from enum import Enum

class TipoToken(Enum):
    IDENTIFICADOR = 1
    CADENA = 2
    CARACTER = 3
    IGUAL = 4
    POR = 5
    PUNTO_Y_COMA = 6
    PUNTO = 7
    DIVISION = 8
    MAS = 9
    MENOS = 10
    PARENTESIS_IZQ = 11
    PARENTESIS_DER = 12
    LLAVE_IZQ = 13
    LLAVE_DER = 14
    EXCLAMACION = 15
    MENOR = 16
    MAYOR = 17
    AND = 18
    OR = 19 
    PALABRA_RESERVADA = 20
    NUMERO_ENTERO = 21
    NUMERO_DECIMAL = 22
