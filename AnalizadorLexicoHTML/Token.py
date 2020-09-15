from AnalizadorLexicoHTML.TipoToken import TipoToken

class Token:

    def __init__(self, tipoToken, lexema, linea, columna):
        self.tipoToken = tipoToken
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def getTipo(self):
        if self.tipoToken == TipoToken.IDENTIFICADOR:
            return "Identificador"
        elif self.tipoToken == TipoToken.CADENA:
            return "Cadena"
        elif self.tipoToken == TipoToken.CADENA_HTML:
            return "Cadena HTML"
        elif self.tipoToken == TipoToken.IGUAL:
            return "Igual"
        elif self.tipoToken == TipoToken.DIAGONAL:
            return "Diagonal"
        elif self.tipoToken == TipoToken.PALABRA_RESERVADA:
            return "Palabra Reservada"
        elif self.tipoToken == TipoToken.MENOR:
            return "Menor"
        elif self.tipoToken == TipoToken.MAYOR:
            return "Mayor"