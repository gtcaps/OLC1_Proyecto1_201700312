from AnalizadorLexicoJS.Token import *

class AnalizadorLexicoJS:

    def __init__(self):
        self.listaTokens = []
        self.estado = 0
        self.lexema = ""

    def agregarToken(self, tipoToken):
        self.listaTokens.append(Token(tipoToken, self.lexema))
        self.estado = 0
        self.lexema = ""
    #END

    def analizar(self, cadena):
        cadenaEntrada = cadena + "#"
        
        for i in range(0, len(cadenaEntrada)):
            caracterActual = cadenaEntrada[i]


            if self.estado == 0:
                if caracterActual == '=':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.IGUAL)
                else:
                    if caracterActual == '#':
                        print(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
    #END

    def imprimirTokens(self):
        for token in self.listaTokens:
            print("=====================================================")
            print('TOKEN => {}     LEXEMA => {}'.format(token.getTipo(), token.lexema))
            print("=====================================================")
    

