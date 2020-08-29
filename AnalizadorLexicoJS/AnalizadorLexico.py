from AnalizadorLexicoJS.Token import *
import os

class AnalizadorLexicoJS:

    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.estado = 0
        self.lexema = ""
        self.palabrasReservadas = ["var","console","log","for","while","do","continue","break","return","constructor","this","pow","true","false", "if", "else"]

    def __agregarToken(self, tipoToken):
        self.listaTokens.append(Token(tipoToken, self.lexema))
        self.estado = 0
        self.lexema = ""
    #END

    def __agregarErrorLexico(self, mensaje):
        self.listaErrores.append(mensaje)
        self.estado = 0
        self.lexema = ""
    #END

    def analizarCadena(self, cadena):
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
                elif caracterActual == '"':
                    self.lexema += caracterActual
                    self.estado = 5
                elif caracterActual == '\'':
                    self.lexema += caracterActual
                    self.estado = 6
                elif caracterActual == '=':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.IGUAL)
                elif caracterActual == '*':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.POR)
                elif caracterActual == ';':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PUNTO_Y_COMA)
                elif caracterActual == '.':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PUNTO)
                elif caracterActual == '/':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.DIVISION)
                elif caracterActual == '+':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MAS)
                elif caracterActual == '(':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PARENTESIS_IZQ)
                elif caracterActual == ')':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PARENTESIS_DER)
                elif caracterActual == '{':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.LLAVE_IZQ)
                elif caracterActual == '}':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.LLAVE_DER)
                elif caracterActual == '-':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MENOS)
                elif caracterActual == '!':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.EXCLAMACION)
                elif caracterActual == '<':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MENOR)
                elif caracterActual == '>':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MAYOR)
                elif caracterActual == '&':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.AND)
                elif caracterActual == '|':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.OR)
                else:
                    if caracterActual == '#':
                        print(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
                    elif caracterActual in (' ','\n','\t'):
                        self.estado = 0
                        self.lexema = ""
                    else:
                        self.__agregarErrorLexico("El caracter {} no es reconocido dentro del lenguaje".format(caracterActual))
            elif self.estado == 1:
                if caracterActual.isalpha() or caracterActual.isdigit():
                    self.estado = 1
                    self.lexema += caracterActual
                else:
                    if self.lexema in self.palabrasReservadas:
                        self.__agregarToken(TipoToken.PALABRA_RESERVADA)
                    else:
                        self.__agregarToken(TipoToken.IDENTIFICADOR)
                    i -= 1
            elif self.estado == 2:
                if caracterActual.isdigit():
                    self.estado = 2
                    self.lexema += caracterActual
                elif caracterActual == '.':
                    self.estado = 3
                    self.lexema += caracterActual
                else:
                    self.__agregarToken(TipoToken.NUMERO_ENTERO)
                    i -= 1
            elif self.estado == 3:
                if caracterActual.isdigit():
                    self.estado = 4
                    self.lexema += caracterActual
                else:
                    self.__agregarErrorLexico("Error Lexico: En el token {} se esperaba un digito y venia {}".format(self.lexema, caracterActual))
                    i -= 1
            elif self.estado == 4:
                if caracterActual.isdigit():
                    self.estado = 4
                    self.lexema += caracterActual
                else:
                    self.__agregarToken(TipoToken.NUMERO_DECIMAL)
                    i -= 1
            elif self.estado == 5:
                if caracterActual == '"':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.CADENA)
                else:
                    self.estado = 5
                    self.lexema += caracterActual
            elif self.estado == 6:
                if caracterActual == '\'':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.CARACTER)
                else:
                    self.lexema += caracterActual
                    self.estado = 7
            elif self.estado == 7:
                if caracterActual == '\'':
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.CARACTER)
                else:
                    self.__agregarErrorLexico("Error Lexico: En el token {} se esperaba una comilla simple y venia {}".format(self.lexema, caracterActual))
                    

            i += 1 
    #END

    def analizarArchivo(self, ruta):  
        if os.path.isfile(ruta):
            archivo = open(ruta, "r")
            self.analizarCadena(archivo.read())
            archivo.close()

        

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
    

