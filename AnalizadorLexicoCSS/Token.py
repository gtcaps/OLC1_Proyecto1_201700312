from AnalizadorLexicoCSS.TipoToken import TipoToken

class Token:

    def __init__(self, tipoToken, lexema):
        self.tipoToken = tipoToken
        self.lexema = lexema

    def getTipo(self):
        if self.tipoToken is TipoToken.IDENTIFICADOR:
            return "Identificador"
        elif self.tipoToken is TipoToken.PROPIEDAD:
            return "Propiedad"
        elif self.tipoToken is TipoToken.NUMERO_ENTERO:
            return "Numero Entero"
        elif self.tipoToken is TipoToken.NUMERO_DECIMAL:
            return "Numero Decimal"
        elif self.tipoToken is TipoToken.NUMERO_HEXADECIMAL:
            return "Numero Hexadecimal"
        elif self.tipoToken is TipoToken.CADENA:
            return "Cadena"
        elif self.tipoToken is TipoToken.LLAVE_IZQ:
            return "Llave Izquierda"
        elif self.tipoToken is TipoToken.LLAVE_DER:
            return "Llave Derecha"
        elif self.tipoToken is TipoToken.PARENTESIS_IZQ:
            return "Parentesis Izquierda"
        elif self.tipoToken is TipoToken.PARENTESIS_DER:
            return "Parentesis Derecho"
        elif self.tipoToken is TipoToken.PUNTO:
            return "Punto"
        elif self.tipoToken is TipoToken.DOS_PUNTOS:
            return "Dos Puntos"
        elif self.tipoToken is TipoToken.PUNTO_Y_COMA:
            return "Punto y coma"
        elif self.tipoToken is TipoToken.COMA:
            return "Coma"
        elif self.tipoToken is TipoToken.ASTERISCO:
            return "Asterisco"
        elif self.tipoToken is TipoToken.NUMERAL:
            return "Numeral"
        elif self.tipoToken is TipoToken.PORCENTAJE:
            return "Porcentaje"

