from AnalizadorLexicoCSS.TipoToken import TipoToken

class Token:

    def __init__(self, tipoToken, lexema, linea, columna):
        self.tipoToken = tipoToken
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def getTipo(self):
        if self.tipoToken == TipoToken.IDENTIFICADOR:
            return "Identificador"
        elif self.tipoToken == TipoToken.NUMERO:
            return "Numero"
        elif self.tipoToken == TipoToken.NUMERO_HEXADECIMAL:
            return "Numero Hexadecimal"
        elif self.tipoToken == TipoToken.PROPIEDADES:
            return "Propiedades"
        elif self.tipoToken == TipoToken.LLAVE_IZQ:
            return "Llave Izquierda"
        elif self.tipoToken == TipoToken.LLAVE_DER:
            return "Llave Derecha"
        elif self.tipoToken == TipoToken.DOS_PUNTOS:
            return "Dos Puntos"
        elif self.tipoToken == TipoToken.PUNTO_Y_COMA:
            return "Punto y Coma"
        elif self.tipoToken == TipoToken.ASTERISCO:
            return "Asterisco"
        elif self.tipoToken == TipoToken.NUMERAL:
            return "Numeral"
        elif self.tipoToken == TipoToken.PUNTO:
            return "Punto"
        elif self.tipoToken == TipoToken.PORCENTAJE:
            return "Porcentaje"
        elif self.tipoToken == TipoToken.COMA:
            return "Coma"
        elif self.tipoToken == TipoToken.PARENTESIS_IZQ:
            return "Parentesis Izquierda"
        elif self.tipoToken == TipoToken.PARENTESIS_DER:
            return "Parentesis Derecha"
        elif self.tipoToken == TipoToken.IGUAL:
            return "Igual"
        elif self.tipoToken == TipoToken.CADENA:
            return "Cadena"
        elif self.tipoToken == TipoToken.UNIDADES:
            return "Unidades"
        elif self.tipoToken == TipoToken.DIVISION:
            return "Divison"
        elif self.tipoToken == TipoToken.RESTA:
            return "Resta"
        elif self.tipoToken == TipoToken.SUMA:
            return "Suma"
        elif self.tipoToken == TipoToken.MAYOR:
            return "Mayor"
        elif self.tipoToken == TipoToken.MENOR:
            return "Menor"
