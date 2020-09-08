from AnalizadorLexicoJS.Token import *
import os
import subprocess

class AnalizadorLexicoJS:

    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.__tknsGrafica = []
        self.entradaLimpia = ""
        self.estado = 0
        self.lexema = ""
        self.linea = 1
        self.columna = 1
        self.palabrasReservadas = ["var","console","log","for","while","do","continue","break","return","constructor","this","pow","true","false", "if", "else"]

    def __agregarToken(self, tipoToken):
        token = Token(tipoToken, self.lexema, self.linea, self.columna)
        self.entradaLimpia += self.lexema
        self.listaTokens.append(token)
        self.estado = 0
        self.lexema = ""
        

        if token.getTipo() not in self.__tknsGrafica and token.getTipo() != "Palabra Reservada":
            self.__tknsGrafica.append(token.getTipo())
    #END

    def __agregarErrorLexico(self, mensaje):
        self.listaErrores.append(mensaje)
        self.estado = 0
        self.lexema = ""
    #END

    def analizarCadena(self, cadena):
        cadenaEntrada = cadena + "#"
        col = 0
        i = 0

        while i < len(cadenaEntrada):
            caracterActual = cadenaEntrada[i]
            
            if caracterActual == '\n':
                self.linea += 1
                col = 0

            if self.estado == 0:
                if caracterActual.isalpha() or caracterActual == '_': #SI ES LETRA
                    self.lexema += caracterActual
                    self.estado = 1
                    self.columna = col
                elif caracterActual.isdigit(): #SI ES DIGITO
                    self.lexema += caracterActual
                    self.estado = 2
                    self.columna = col
                elif caracterActual == '"':
                    self.lexema += caracterActual
                    self.estado = 5
                    self.columna = col
                elif caracterActual == '\'':
                    self.lexema += caracterActual
                    self.estado = 6
                    self.columna = col
                elif caracterActual == '=':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.IGUAL)
                elif caracterActual == '*':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.POR)
                elif caracterActual == ';':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PUNTO_Y_COMA)
                elif caracterActual == '.':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PUNTO)
                elif caracterActual == '/':
                    self.lexema += caracterActual
                    self.estado = 7
                elif caracterActual == '+':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MAS)
                elif caracterActual == '(':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PARENTESIS_IZQ)
                elif caracterActual == ')':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.PARENTESIS_DER)
                elif caracterActual == '{':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.LLAVE_IZQ)
                elif caracterActual == '}':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.LLAVE_DER)
                elif caracterActual == '-':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MENOS)
                elif caracterActual == ',':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.COMA)
                elif caracterActual == '!':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.EXCLAMACION)
                elif caracterActual == '<':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MENOR)
                elif caracterActual == '>':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.MAYOR)
                elif caracterActual == '&':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.AND)
                elif caracterActual == ':':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.DOS_PUNTOS)
                elif caracterActual == '|':
                    self.columna = col
                    self.lexema += caracterActual
                    self.__agregarToken(TipoToken.OR)
                else:
                    if caracterActual == '#' and i == (len(cadenaEntrada) - 1):
                        print(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
                    elif caracterActual in ('\n',' ', '\t'):
                        self.estado = 0
                        self.lexema = ""
                        self.entradaLimpia += caracterActual
                    else:
                        self.__agregarErrorLexico("El caracter {} no es reconocido dentro del lenguaje".format(caracterActual))
            elif self.estado == 1:
                if caracterActual.isalpha() or caracterActual.isdigit() or caracterActual == '_':
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
                    self.estado = 6
            elif self.estado == 7:
                if caracterActual == '/':
                    self.lexema += caracterActual
                    self.estado = 8
                elif caracterActual == '*':
                    self.lexema += caracterActual
                    self.estado = 9
                else:
                    self.__agregarToken(TipoToken.DIVISION)
                    i -= 1
            elif self.estado == 8:
                if caracterActual == '\n' or i == (len(cadenaEntrada) - 1):
                    # COMENTARIO DE UNA LINEA
                    print("ESTE ES UN COMENTARIO DE UNA LINEA => " + self.lexema)
                    self.entradaLimpia += self.lexema
                    self.lexema = ""
                    self.estado = 0
                    if "Comentario Unilinea" not in self.__tknsGrafica:
                        self.__tknsGrafica.append("Comentario Unilinea")
                else:
                    self.lexema += caracterActual
                    self.estado = 8
            elif self.estado == 9:
                if caracterActual == '*':
                    self.lexema += caracterActual
                    self.estado = 10
                else:
                    self.lexema += caracterActual
                    self.estado = 9
            elif self.estado == 10:
                if caracterActual == '/':
                    #COMENTARIO MULTILINEA
                    print("ESTE ES UN COMENTARIO MULTILINEA => \n" + self.lexema)
                    self.entradaLimpia += self.lexema
                    self.lexema = ""
                    self.estado = 0
                    if "Comentario Multilinea" not in self.__tknsGrafica:
                        self.__tknsGrafica.append("Comentario Multilinea")
                else:
                    self.lexema += caracterActual
                    self.estado = 9

                    

            i += 1 
            col += 1
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

    def __verificarDirectorioReportes(self):
        if not os.path.isdir("reportes/"):
            os.mkdir("reportes/")

    def generarReporteErrores(self):
        self.__verificarDirectorioReportes()

        file = open("reportes/erroresjs.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Errores</title>\n")
        file.write("    <style>")
        file.write("        *{margin:0; padding:0; box-sizing: border-box;}\n")
        file.write("        h1{text-align: center; margin: 30px 0;}\n")
        file.write("        table{border-collapse: collapse; margin: 0 auto; width: 40%;}\n")
        file.write("        td, th{border: 1px solid black; padding: 10px;}\n")
        file.write("       th{background: black; color: white}\n")
        file.write("    </style>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("    <h1>Reporte de Errores Lexicos </h1>\n")
        file.write("    <table>\n")
        file.write("        <thead>\n")
        file.write("            <tr>\n")
        file.write("                <th>#</th>\n")
        file.write("                <th>Error</th>\n")
        file.write("            </tr>\n")
        file.write("        </thead>\n")
        file.write("        <tbody>")

        if len(self.listaErrores) != 0:
            i = 1
            for error in self.listaErrores:
                file.write("            <tr>")
                file.write("                <td>{}</td>".format(i))
                file.write("                <td>{}</td>".format(error))
                file.write("            </tr>")
                i += 1
        else:
            file.write("            <tr>")
            file.write("                <td>0</td>")
            file.write("                <td>El archivo no tiene errores lexico :D</td>")
            file.write("            </tr>")

        file.write("        </tbody>")
        file.write("    </table>\n")
        file.write("</body>\n")
        file.write("</html>")
        file.close()

        os.system("start ./reportes/erroresjs.html")
    #END

    def generarReporteArbol(self):
        self.__verificarDirectorioReportes()
        file = open("reportes/arboljs.dot", "w")
        file.write("digraph G{\n")
        file.write("    rankdir=LR;\n")
        file.write("    node[shape=circle];\n")
        file.write("    node0[label=\"0\"];\n")

        i = 1
        for tkn in self.__tknsGrafica:
            if tkn == "Identificador":
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - ID\"];\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"Letra | _"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"Letra | Digito | _"))
            elif tkn == "Cadena":
                file.write("    node{0}[label=\"{0}\"];\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"\\\""))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"*"))
                i += 1
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - Cadena\"];\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"\\\""))
            elif tkn == "Caracter":
                file.write("    node{0}[label=\"{0}\"];\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"\\'"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"*"))
                i += 1
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - Caracter\"];\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"\\'"))
            elif tkn == "Numero Entero":
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - Entero\"];\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"Digito"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"Digito"))
            elif tkn == "Numero Decimal":
                file.write("    node{0}[label=\"{0}\"];\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"Digito"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"Digito"))
                i += 1
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - Decimal\"];\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"Punto"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"Digito"))
            elif tkn == "Comentario Unilinea":
                file.write("    node{0}[label=\"{0}\"]\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"/"))
                i += 1
                file.write("    node{0}[label=\"{0}\"]\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"/"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"*"))
                i += 1
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - Coment Uni\"]\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"\\\\n"))
            elif tkn == "Comentario Multilinea":
                file.write("    node{0}[label=\"{0}\"]\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,"/"))
                i += 1
                file.write("    node{0}[label=\"{0}\"]\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"(*)"))
                file.write("    node{0}->node{0}[label=\"{1}\"];\n".format(i,"*"))
                i += 1
                file.write("    node{0}[label=\"{0}\"]\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"(*)"))
                i += 1
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0} - Coment Multi\"]\n".format(i))
                file.write("    node{}->node{}[label=\"{}\"];\n".format(i-1,i,"/"))
            else:
                file.write("    node{0}[shape=\"doublecircle\", label=\"{0}\"];\n".format(i))
                file.write("    node0->node{}[label=\"{}\"];\n".format(i,tkn))
            i += 1

        file.write("}")
        file.close()

        os.system("dot -Tpng ./reportes/arboljs.dot -o ./reportes/arboljs.png")
        os.system("start ./reportes/arboljs.png")

    #END
    

