from AnalizadorLexicoJS.Token import *
import re

class AnalizadorLexicoJS:

    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.estado = 0
        self.lexema = ""
        self.palabrasReservadas = ["var","console","log","for","while","do","continue","break","return","constructor","this","pow","true","false"]

    def agregarToken(self, tipoToken):
        self.listaTokens.append(Token(tipoToken, self.lexema))
        self.estado = 0
        self.lexema = ""
    #END

    def agregarErrorLexico(self, mensaje):
        self.listaErrores.append(mensaje)
        self.estado = 0
        self.lexema = ""
    #END

    def analizar(self, cadena):
        cadenaEntrada = cadena + "#"
        i = 0

        while i < len(cadenaEntrada):
            caracterActual = cadenaEntrada[i]


            if self.estado == 0:
                if caracterActual.isalpha(): #SI ES LETRA
                    self.lexema += caracterActual
                    self.estado = 1
                elif caracterActual.isdigit(): #SI ES DIGITO
                    self.lexema += caracterActual
                    self.estado = 2
                elif caracterActual == '=':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.IGUAL)
                elif caracterActual == '*':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.POR)
                elif caracterActual == ';':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.PUNTO_Y_COMA)
                elif caracterActual == '.':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.PUNTO)
                elif caracterActual == '/':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.DIVISION)
                elif caracterActual == '+':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.MAS)
                elif caracterActual == '(':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.PARENTESIS_IZQ)
                elif caracterActual == ')':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.PARENTESIS_DER)
                elif caracterActual == '{':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.LLAVE_IZQ)
                elif caracterActual == '}':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.LLAVE_DER)
                elif caracterActual == '-':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.MENOS)
                elif caracterActual == '!':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.EXCLAMACION)
                elif caracterActual == '<':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.MENOR)
                elif caracterActual == '>':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.MAYOR)
                elif caracterActual == '&':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.AND)
                elif caracterActual == '|':
                    self.lexema += caracterActual
                    self.agregarToken(TipoToken.OR)
                else:
                    if caracterActual == '#':
                        print(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
            elif self.estado == 1:
                if caracterActual.isalpha() or caracterActual.isdigit():
                    self.estado = 1
                    self.lexema += caracterActual
                else:
                    if self.lexema in self.palabrasReservadas:
                        self.agregarToken(TipoToken.PALABRA_RESERVADA)
                    else:
                        self.agregarToken(TipoToken.IDENTIFICADOR)
                    i -= 1
            elif self.estado == 2:
                if caracterActual.isdigit():
                    self.estado = 2
                    self.lexema += caracterActual
                elif caracterActual == '.':
                    self.estado = 3
                    self.lexema += caracterActual
                else:
                    self.agregarToken(TipoToken.NUMERO_ENTERO)
                    i -= 1
            elif self.estado == 3:
                if caracterActual.isdigit():
                    self.estado = 4
                    self.lexema += caracterActual
                else:
                    self.agregarErrorLexico("Error Lexico: En el token {} se esperaba un digito y venia {}".format(self.lexema, caracterActual))
                    i -= 1
            elif self.estado == 4:
                if caracterActual.isdigit():
                    self.estado = 4
                    self.lexema += caracterActual
                else:
                    self.agregarToken(TipoToken.NUMERO_DECIMAL)
                    i -= 1



            i += 1 

    #END

    def imprimirTokens(self):
        for token in self.listaTokens:
            print("=====================================================")
            print('TOKEN => {}     LEXEMA => {}'.format(token.getTipo(), token.lexema))
            print("=====================================================")
    #END

    def imprimirErrores(self):
        for error in self.listaErrores:
            print("\n\n;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
            print(error)
            print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
    #END
    

