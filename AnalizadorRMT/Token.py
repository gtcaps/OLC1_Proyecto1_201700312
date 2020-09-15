from AnalizadorRMT.TipoToken import TipoToken

class Token:

    def __init__(self, tipoToken, lexema, linea, columna):
        self.tipoToken = tipoToken
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def getTipo(self):
        if self.tipoToken is TipoToken.SUMA:
            return "Suma"
        elif self.tipoToken is TipoToken.RESTA:
            return "Resta"
        elif self.tipoToken is TipoToken.MULTIPLICACION:
            return "Multiplicacion"
        elif self.tipoToken is TipoToken.DIVISION:
            return "Division"
        elif self.tipoToken is TipoToken.PARENTESIS_IZQ:
            return "Parentesis Izquierdo"
        elif self.tipoToken is TipoToken.PARENTESIS_DER:
            return "Parentesis Derecho"
        elif self.tipoToken is TipoToken.VARIABLE:
            return "Variable"
        elif self.tipoToken is TipoToken.NUMERO:
            return "Numero"        

