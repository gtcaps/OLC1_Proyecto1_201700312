from AnalizadorLexicoHTML.Token import *
import os, re, pathlib

class AnalizadorLexicoHTML:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.entradaLimpia = ""
        self.estado = 0
        self.lexema = ""
        self.linea = 1
        self.columna = 1
        self.comentarios = []
        self.cadenas = []
        self.palabrasReservadas = ["html","head","title","bode","h1","h2","h3","h4","h5","h6","p","br","img","src","id","class","a","href","ul","ol","li","style","table","thead","tbody","th","tr","td","caption","colgroup","col","tfoot","border","body","div","footer"]
    #END -----

    def __agregarToken(self, tipoToken):
        token = Token(tipoToken, self.lexema, self.linea, self.columna)
        self.entradaLimpia += self.lexema
        self.listaTokens.append(token)
        self.estado = 0
        self.lexema = ""
    #END -----

    def  __agregarErrorLexico(self, mensaje):
        self.listaErrores.append(mensaje)
        self.estado = 0
        self.lexema = ""
    #END -----

    def analizarCadena(self, cadena):
        cadenaEntrada = cadena.strip() + "#"
        col = 0
        i = 0

        while i < len(cadenaEntrada):
            caracterActual = cadenaEntrada[i]

            if caracterActual == '\n':
                self.linea += 1
                col = 0

            if self.estado == 0:
                if caracterActual == '"':
                    self.lexema += caracterActual
                    self.estado = 1
                    self.columna = col
                elif caracterActual == '<':
                    self.lexema += caracterActual
                    self.estado = 2
                elif caracterActual == '/':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.DIAGONAL)
                elif caracterActual == '=':
                    self.lexema += caracterActual
                    self.columna = col
                    self.__agregarToken(TipoToken.IGUAL)
                elif caracterActual.isalpha():
                    self.lexema += caracterActual
                    self.estado = 6
                elif caracterActual == '>':
                    self.lexema += caracterActual
                    self.columna = col
                    self.estado = 7
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
                if caracterActual == '"':
                    self.lexema += caracterActual
                    self.cadenas.append(self.lexema)
                    self.__agregarToken(TipoToken.CADENA)
                else:
                    self.estado = 1
                    self.lexema += caracterActual  
            elif self.estado == 2:
                if caracterActual == '!':
                    self.lexema += caracterActual
                    self.estado = 3
                else:
                    self.__agregarToken(TipoToken.MENOR)
                    i -= 1
            elif self.estado == 3:
                if caracterActual == '-':
                    self.lexema += caracterActual
                    self.estado = 4
                else:
                    self.lexema += caracterActual
                    self.estado = 3
            elif self.estado == 4:
                if caracterActual == '-':
                    self.lexema += caracterActual
                    self.estado = 5
                else:
                    self.lexema += caracterActual
                    self.estado = 3
            elif self.estado == 5:
                if caracterActual == '>':
                    self.lexema += caracterActual
                    print("COMENTARIO =>\n{}".format(self.lexema))
                    self.comentarios.append(self.lexema)
                    self.entradaLimpia += self.lexema
                    self.lexema = ""
                    self.estado = 0
                else:
                    self.lexema += caracterActual
                    self.estado = 3
            elif self.estado == 6:
                if caracterActual.isalpha() or caracterActual.isdigit():
                    self.lexema += caracterActual
                    self.estado = 6
                else:
                    if self.lexema in self.palabrasReservadas:
                        self.__agregarToken(TipoToken.PALABRA_RESERVADA)
                    else:
                        self.__agregarToken(TipoToken.IDENTIFICADOR)
                    i -= 1    
            elif self.estado == 7:
                if caracterActual == '<':
                    if len(self.lexema) == 1:
                        self.__agregarToken(TipoToken.MAYOR)
                        self.lexema += caracterActual
                        self.__agregarToken(TipoToken.MENOR)
                    else:
                        cadena_html = self.lexema.replace(">","")
                        self.lexema = self.lexema.replace(cadena_html,"")
                        self.__agregarToken(TipoToken.MAYOR)
                        self.lexema = cadena_html
                        self.__agregarToken(TipoToken.CADENA_HTML)
                        self.lexema = caracterActual
                        self.__agregarToken(TipoToken.MENOR)
                elif caracterActual == '#' and i == (len(cadenaEntrada) - 1):
                    self.__agregarToken(TipoToken.MAYOR)
                    i -= 1
                else:
                    self.lexema += caracterActual
                    self.estado = 7


            i+= 1
            col += 1

        auxTkn = []
        for tkn in self.listaTokens:
            if re.search(r'([\t\n ][\t\ ])+', tkn.lexema):
                continue
            else:
                auxTkn.append(tkn)
        self.listaTokens = auxTkn
    #END -----

    def analizarArchivo(self, ruta):
        if os.path.isfile(ruta):
            archivo = open(ruta, "r")
            self.analizarCadena(archivo.read())
            archivo.close()
    #END -----

    def imprimirTokens(self):
        for token in self.listaTokens:
            print("=====================================================")
            print('TOKEN => {}     LEXEMA => {}'.format(token.getTipo(), token.lexema))
            print("=====================================================")
    #END -----

    def imprimirErrores(self):
        for error in self.listaErrores:
            print("\n\n;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
            print(error)
            print(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;")
    #END -----

    def crearArchivoLimpio(self, nombre_archivo):
        # patron = r'([a-zA-Z]:\\)*(\w+\\)+'
        patron = r'(PATHW)[: ]+([a-zA-Z]:\\)*(\w+\\)+'
        ruta = re.search(patron, self.entradaLimpia)
        ruta = ruta.group()

        ruta = re.sub(r'(PATHW)[: ]+',"",ruta)
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

        file = open("reportes/erroreshtml.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Errores HTML</title>\n")
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
        file.write("        <a href=\"tokenshtml.html\">Reporte Tokens</a>\n")
        file.write("        <a href=\"erroreshtml.html\">Reporte Errores</a>\n")
        file.write("    </menu>\n")
        file.write("    <h1>Reporte de Errores Lexicos HTML</h1>\n")
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

        os.system("start ./reportes/erroreshtml.html")
    #END -------

    def __generarReporteTokens(self):
        self.__verificarDirectorioReportes()

        file = open("reportes/tokenshtml.html", "w")
        file.write("<!DOCTYPE html>\n<html>\n")
        file.write("<head>\n")
        file.write("    <meta charset=\"UTF-8\">\n")
        file.write("    <title>Reporte de Tokens HTML</title>\n")
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
        file.write("        <a href=\"tokenshtml.html\">Reporte Tokens</a>\n")
        file.write("        <a href=\"erroreshtml.html\">Reporte Errores</a>\n")
        file.write("    </menu>\n")
        file.write("    <h1>Reporte de Tokens HTML</h1>\n")
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