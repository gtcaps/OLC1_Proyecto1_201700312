from AnalizadorLexicoJS.TipoToken import TipoToken

class Token:

    def __init__(self, tipoToken, lexema):
        self.tipoToken = tipoToken
        self.lexema = lexema

    def getTipo(self):
        if self.tipoToken is TipoToken.IDENTIFICADOR:
            return "Identificador"
        elif self.tipoToken is TipoToken.CADENA:
            return "Cadena"
        elif self.tipoToken is TipoToken.CARACTER:
            return "Caracter"
        elif self.tipoToken is TipoToken.IGUAL:
            return "Igual"
        elif self.tipoToken is TipoToken.POR:
            return "Por"
        elif self.tipoToken is TipoToken.PUNTO_Y_COMA:
            return "Punto y Coma"
        elif self.tipoToken is TipoToken.PUNTO:
            return "Punto"
        elif self.tipoToken is TipoToken.DIVISION:
            return "Division"
        elif self.tipoToken is TipoToken.MAS:
            return "Mas"
        elif self.tipoToken is TipoToken.PARENTESIS_IZQ:
            return "Parentesis Izquierdo"
        elif self.tipoToken is TipoToken.PARENTESIS_DER:
            return "Parentesis Derecho"
        elif self.tipoToken is TipoToken.LLAVE_IZQ:
            return "Llave Izquierda"
        elif self.tipoToken is TipoToken.LLAVE_DER:
            return "Llave Derecha"
        elif self.tipoToken is TipoToken.MENOS:
            return "Menos"
        elif self.tipoToken is TipoToken.EXCLAMACION:
            return "Exclamacion"
        elif self.tipoToken is TipoToken.MAYOR:
            return "Mayor"
        elif self.tipoToken is TipoToken.MENOR:
            return "Menor"
        elif self.tipoToken is TipoToken.OR:
            return "Or"
        elif self.tipoToken is TipoToken.PALABRA_RESERVADA:
            return "Palabra Reservada"
        elif self.tipoToken is TipoToken.NUMERO_ENTERO:
            return "Numero Entero"
        elif self.tipoToken is TipoToken.NUMERO_DECIMAL:
            return "Numero Decimal"
        else:
            return "AND"

