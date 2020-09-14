from AnalizadorLexicoCSS.Token import *
import os, re, pathlib


class AnalizadorLexicoCSS:

    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.entradaLimpia = ""
        self.estado = 0
        self.lexema = ""
        self.linea = 1
        self.columna = 1
        self.bitacora = []
        self.comentarios = []
        self.cadenas = []
        self.numeros = []
        self.palabrasReservadasPropiedades = ["color","border","text-align","font-weight","padding-left","padding-top","line-height","margin-top","margin-left","display","top","float","min-width","background-color","opacity","font-family","font-size","padding-right","padding","width","margin-right","margin","position","right","url","background-image","background","font-style","font","height","margin-bottom","border-style","bottom","left","max-width","min-height","rgb","rgba"]
        self.palabrasReservadasUnidades = ["em","px","in","vh","vw","cm","mm","pt","pc","rem"]
    #END -------

    def __agregarToken(self, tipoToken):
        token = Token(tipoToken, self.lexema, self.linea, self.columna)
        self.entradaLimpia += self.lexema
        self.listaTokens.append(token)
        self.estado = 0
        self.lexema = ""
    #END -------

    def __agregarErrorLexico(self, mensaje):
        self.listaErrores.append(mensaje)
        self.estado = 0
        self.lexema = ""
    #END -------

    def __agregarBitacora(self, token = None):
        self.bitacora.append("| Estado {} | Lexema -> {} ".format(self.estado, self.lexema))
        if token is not None:
            self.bitacora.append("  -> Aceptando el token {}\n".format(token))
    #END -------


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
                self.__agregarBitacora()
                if caracterActual.isalpha() or caracterActual == '_':
                    self.lexema += caracterActual
                    self.estado = 1
                    self.columna = col
                    self.__agregarBitacora()
                elif caracterActual.isdigit():
                    self.lexema += caracterActual
                    self.estado = 2
                    self.columa = col
                    self.__agregarBitacora()
                elif caracterActual == '-':
                    self.lexema += caracterActual
                    self.estado = 5
                    self.columna = col
                    self.__agregarBitacora()
                elif caracterActual == '#':
                    if i == (len(cadenaEntrada) - 1):
                        self.bitacora.append(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
                        print(">>>>>>>>>>>> Fin del Analisis Lexico <<<<<<<<<<<<<")
                    else:
                        self.lexema += caracterActual
                        self.estado = 6  
                        self.columna = col
                        self.__agregarBitacora()
                elif caracterActual == '"':
                    self.lexema += caracterActual
                    self.estado = 7
                    self.columa = col
                    self.__agregarBitacora()
                elif caracterActual == '/':
                    self.lexema += caracterActual
                    self.estado = 9
                    self.__agregarBitacora()
                elif caracterActual == '(':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.PARENTESIS_IZQ)
                elif caracterActual == ')':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.PARENTESIS_DER)
                elif caracterActual == ',':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.COMA)
                elif caracterActual == '%':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.PORCENTAJE)
                elif caracterActual == '{':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.LLAVE_IZQ)       
                elif caracterActual == '}':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.LLAVE_DER)  
                elif caracterActual == ':':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.DOS_PUNTOS)     
                elif caracterActual == ';':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.PUNTO_Y_COMA)
                elif caracterActual == '*':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.ASTERISCO)
                elif caracterActual == '=':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.IGUAL)
                elif caracterActual == '.':
                    self.lexema += caracterActual
                    self.columa = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.PUNTO)
                elif caracterActual == '+':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.SUMA)
                elif caracterActual == '-':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.RESTA)
                elif caracterActual == '>':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.MAYOR)
                elif caracterActual == '<':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarBitacora(self.lexema)
                    self.__agregarToken(TipoToken.MENOR)
                else:
                    if caracterActual in ('\n',' ','\t'):
                        self.estado = 0
                        self.lexema = ""
                        self.entradaLimpia += caracterActual
                    else:
                        self.bitacora.append("| Error lexico | El caracter {} no es reconocido".format(caracterActual))
                        self.__agregarErrorLexico("El caracter {} no es reconocido dentro del lenguaje".format(caracterActual))                    
            elif self.estado == 1:
                if caracterActual.isalpha() or caracterActual.isdigit() or caracterActual in ["_", "-"]:
                    self.estado = 1
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    if self.lexema in self.palabrasReservadasPropiedades:
                        self.__agregarBitacora("Propiedades")
                        self.__agregarToken(TipoToken.PROPIEDADES)
                    elif self.lexema in self.palabrasReservadasUnidades:
                        self.__agregarBitacora("Unidades")
                        self.__agregarToken(TipoToken.UNIDADES)
                    else:
                        self.__agregarBitacora("Identificador")
                        self.__agregarToken(TipoToken.IDENTIFICADOR)
                    i -= 1 
            elif self.estado == 2:
                if caracterActual.isdigit():
                    self.estado = 2
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                elif caracterActual == '.':
                    self.estado = 3
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    self.__agregarBitacora("Numero")
                    self.numeros.append(self.lexema)
                    self.__agregarToken(TipoToken.NUMERO)
                    i -= 1
            elif self.estado == 3:
                if caracterActual.isdigit():
                    self.estado = 4
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    self.bitacora.append("| Error Lexico | En el token {} se esperaba un digito y venia {}".format(self.lexema, caracterActual))
                    self.__agregarErrorLexico("Error Lexico: En el token {} se esperaba un digito y venia {}".format(self.lexema, caracterActual))
                    i -= 1
            elif self.estado == 4:
                if caracterActual.isdigit():
                    self.estado = 4
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    self.__agregarBitacora("Numero")
                    self.numeros.append(self.lexema)
                    self.__agregarToken(TipoToken.NUMERO)
                    i -= 1
            elif self.estado == 5:
                if caracterActual.isdigit():
                    self.estado = 2
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    self.estado = 0
                    self.lexema
                    self.__agregarBitacora() 
                    i -= 1
            elif self.estado == 6:
                if caracterActual.lower() in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
                    self.estado = 6
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    if len(self.lexema) == 1:
                        self.__agregarBitacora(self.lexema)
                        self.__agregarToken(TipoToken.NUMERAL)
                    else:
                        if re.search(r'#[0-9a-fA-F]{3,6}', self.lexema):
                            self.__agregarBitacora("Numero Hexadecimal")
                            self.numeros.append(self.lexema)
                            self.__agregarToken(TipoToken.NUMERO_HEXADECIMAL)
                        else:
                            splt = self.lexema.replace("#","")
                            self.lexema = "#"
                            self.__agregarBitacora(self.lexema)
                            self.__agregarToken(TipoToken.NUMERAL)
                            i -= len(splt)


                    i -= 1
            elif self.estado == 7:
                if caracterActual == '"':
                    self.lexema += caracterActual
                    self.cadenas.append(self.lexema)
                    self.__agregarBitacora("Cadena")
                    self.__agregarToken(TipoToken.CADENA)
                else:
                    self.estado = 7
                    self.lexema += caracterActual
                    self.__agregarBitacora()
            elif self.estado == 9:
                if caracterActual == '*':
                    self.estado = 10
                    self.lexema += caracterActual
                    self.__agregarBitacora()
                else:
                    self.__agregarToken(TipoToken.DIVISION)
                    i -= 1
            elif self.estado == 10:
                if caracterActual == '*':
                    self.lexema += caracterActual
                    self.estado = 11
                    self.__agregarBitacora()
                else:
                    self.lexema += caracterActual
                    self.estado = 10
                    self.__agregarBitacora()
            elif self.estado == 11:
                if caracterActual == '/':
                    self.lexema += caracterActual
                    print("COMENTARIO => \n{}".format(self.lexema))
                    self.comentarios.append(self.lexema)
                    self.entradaLimpia += self.lexema
                    self.__agregarBitacora("Comentario")
                    self.lexema = ""
                    self.estado = 0
                else:
                    self.lexema += caracterActual
                    self.estado = 10
                    self.__agregarBitacora()


            i += 1
            col += 1
    #END -------

    def analizarArchivo(self, ruta):
        if os.path.isfile(ruta):
            archivo = open(ruta,"r")
            self.analizarCadena(archivo.read())
            archivo.close()
    #END -------
    
    def imprimirTokens(self):
        for token in self.listaTokens:
            print("=====================================================")
            print('TOKEN => {}     LEXEMA => {}'.format(token.getTipo(), token.lexema))
            print("=====================================================")
    #END -------

    def imprimirErrores(self):
        for error in self.listaErrores:
            print("\n\n;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
            print(error)
            print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
    #END -------

    def crearArchivoLimpio(self, nombre_archivo):
        patron = r'([a-zA-Z]:\\)*(\w+\\)+'
        ruta = re.search(patron, self.entradaLimpia)
        ruta = ruta.group()

        ruta = re.sub(r'[a-zA-Z]:\\','',ruta)
        ruta = ruta.replace("user\\","")
        pathlib.Path(ruta).mkdir(parents=True, exist_ok=True)

        file = open(".\\" + ruta + nombre_archivo, "w")
        file.write(self.entradaLimpia)
        file.close()
    #END -------

    def __verificarDirectorioReportes(self):
        if not os.path.isdir("reportes/"):
            os.mkdir("reportes/")
    #END -------

    def generarReporteErrores(self):
        self.__verificarDirectorioReportes()

        file = open("reportes/errorescss.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Errores CSS</title>\n")
        file.write("    <style>")
        file.write("        *{margin:0; padding:0; box-sizing: border-box;}\n")
        file.write("        menu{background: rgb(27,38,68);text-align:center;padding:20px 0;}\n")
        file.write("        a{margin: 0 30px; text-decoration:none; font-size:20px; color:white;}\n")
        file.write("        a:hover{text-decoration: underline;}\n")
        file.write("        h1{text-align: center; margin: 30px 0;}\n")
        file.write("        table{border-collapse: collapse; margin: 0 auto; width: 40%;}\n")
        file.write("        td, th{border: 1px solid black; padding: 10px;}\n")
        file.write("       th{background: black; color: white}\n")
        file.write("    </style>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("    <menu>\n")
        file.write("        <a href=\"tokenscss.html\">Reporte Tokens</a>\n")
        file.write("        <a href=\"errorescss.html\">Reporte Errores</a>\n")
        file.write("    </menu>\n")
        file.write("    <h1>Reporte de Errores Lexicos CSS</h1>\n")
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

        self.__generarReporteTokens()

        os.system("start ./reportes/errorescss.html")
    #END -------

    def __generarReporteTokens(self):
        self.__verificarDirectorioReportes()

        file = open("reportes/tokenscss.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Tokens CSS</title>\n")
        file.write("    <style>")
        file.write("        *{margin:0; padding:0; box-sizing: border-box;}\n")
        file.write("        menu{background: rgb(27,38,68);text-align:center;padding:20px 0;}\n")
        file.write("        a{margin: 0 30px; text-decoration:none; font-size:20px; color:white;}\n")
        file.write("        a:hover{text-decoration: underline;}\n")
        file.write("        h1{text-align: center; margin: 30px 0;}\n")
        file.write("        table{border-collapse: collapse; margin: 0 auto; width: 40%;}\n")
        file.write("        td, th{border: 1px solid black; padding: 10px;}\n")
        file.write("       th{background: black; color: white}\n")
        file.write("    </style>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("    <menu>\n")
        file.write("        <a href=\"tokenscss.html\">Reporte Tokens</a>\n")
        file.write("        <a href=\"errorescss.html\">Reporte Errores</a>\n")
        file.write("    </menu>\n")
        file.write("    <h1>Reporte de Tokens CSS</h1>\n")
        file.write("    <table>\n")
        file.write("        <thead>\n")
        file.write("            <tr>\n")
        file.write("                <th>#</th>\n")
        file.write("                <th>Token</th>\n")
        file.write("                <th>Lexema</th>\n")
        file.write("                <th>Fila</th>\n")
        file.write("                <th>Columna</th>\n")
        file.write("            </tr>\n")
        file.write("        </thead>\n")
        file.write("        <tbody>")

        if len(self.listaTokens) != 0:
            i = 1
            for token in self.listaTokens:
                file.write("            <tr>")
                file.write("                <td>{}</td>".format(i))
                file.write("                <td>{}</td>".format(token.getTipo()))
                file.write("                <td>{}</td>".format(token.lexema))
                file.write("                <td>{}</td>".format(token.linea))
                file.write("                <td>{}</td>".format(token.columna))
                file.write("            </tr>")
                i += 1
        else:
            file.write("            <tr>")
            file.write("                <td>0</td>")
            file.write("                <td>El archivo no tiene tokens :D</td>")
            file.write("            </tr>")

        file.write("        </tbody>")
        file.write("    </table>\n")
        file.write("</body>\n")
        file.write("</html>")
        file.close()
    #END -------