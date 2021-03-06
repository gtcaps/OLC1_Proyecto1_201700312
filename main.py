import os
from tkinter import *
from tkinter import filedialog, messagebox
from AnalizadorLexicoJS.AnalizadorLexico import AnalizadorLexicoJS
from AnalizadorLexicoCSS.AnalizadorLexico import AnalizadorLexicoCSS
from AnalizadorLexicoHTML.AnalizadorLexico import AnalizadorLexicoHTML
from AnalizadorRMT.AnalizadorLexico import AnalizadorLexicoRMT
from AnalizadorRMT.AnalizadorSintactico import AnalizadorSintactico

archivo = None



####################################################
# DEFINIENDO LA VENTANA
####################################################
ventana = Tk()
ventana.title("ML Web")
ventana.resizable(False, False)

ancho_ventana = 1300
alto_ventana  = 750

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla  = ventana.winfo_screenheight()

cordenada_x = int((ancho_pantalla/2) - (ancho_ventana/2))
cordenada_y = int((alto_pantalla/2)  - (alto_ventana/2))

ventana.geometry("{}x{}+{}+{}".format(ancho_ventana, alto_ventana, cordenada_x, cordenada_y))

####################################################
# Titulo
####################################################
label_titulo = Label(ventana, text="Archivo de Entrada:")
label_nombre_archivo = Label(ventana, text="")

label_titulo.place(x=((ancho_ventana/4) - 100), y=15)
label_nombre_archivo.place(x=((ancho_ventana/4) + 20), y=15)

###################################################
# EDITOR
##################################################
editor_texto = Text(ventana)
editor_scroll = Scrollbar(editor_texto)
editor_scroll.pack(side=RIGHT, fill="y")

editor_texto.place(x=10, y=45, width= (ancho_ventana/2) - 20, height=500)
editor_texto.config(yscrollcommand=editor_scroll.set)
editor_scroll.config(command=editor_texto.yview)

###################################################
# VISOR ARCHIVO LIMPIO
##################################################
visor_texto = Text(ventana)
visor_scroll = Scrollbar(visor_texto)
visor_scroll.pack(side=RIGHT, fill="y")

visor_texto.place(x=(ancho_ventana/2), y=45, width= (ancho_ventana/2) - 10, height=500)
visor_texto.config(yscrollcommand=visor_scroll.set)
visor_scroll.config(command=visor_texto.yview)


# ####################################################
# # CONSOLA
# ###################################################
label_consola = Label(ventana,text="Consola")
label_consola.place(x=10, y=555)

consola = Text(ventana)
consola_scroll = Scrollbar(consola)
consola_scroll.pack(side=RIGHT, fill="y")

consola.place(x=10, y=580, width= ancho_ventana - 20, height=150)
consola.config(yscrollcommand=consola_scroll.set)
consola_scroll.config(command=consola.yview)


####################################################
# MENU PRINCIPAL
####################################################
def limpiarConsola():
    consola.delete("1.0",END)
    visor_texto.delete("1.0", END)

def limpiarEditor():
    editor_texto.delete("1.0", END)
    visor_texto.delete("1.0", END)

def salirVentana():
    ventana.destroy()

def abrirArchivo():
    global archivo
    archivo = filedialog.askopenfile(mode="r", filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css"),("RMT Files","*.rmt")])
    if archivo is not None:
        limpiarEditor()
        contenido = archivo.read()
        editor_texto.insert(END, contenido)
        label_nombre_archivo["text"] = os.path.basename(archivo.name)
#END

def nuevoArchivo():
    global archivo
    archivo = filedialog.asksaveasfile(filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css"),("RMT Files","*.rmt")])
    if archivo is not None:
        limpiarEditor()
        label_nombre_archivo["text"] = os.path.basename(archivo.name)

def guardarArchivo():
    global archivo
    texto = editor_texto.get("1.0", END)

    if archivo is None:
        archivo = filedialog.asksaveasfile(filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css"),("RMT Files","*.rmt")])
        label_nombre_archivo["text"] = os.path.basename(archivo.name)
        archivo.write(texto)
        archivo.close()
    else:
        f = open(archivo.name, "w")
        f.write(texto)
        f.close()

def guardarArchivoComo():
    global archivo
    texto = editor_texto.get("1.0", END)
    archivo = filedialog.asksaveasfile(filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css"),("RMT Files","*.rmt")])
    label_nombre_archivo["text"] = os.path.basename(archivo.name)
    archivo.write(texto)
    archivo.close()
#END

def resaltarPalabra(id, palabras, color):
    for palabra in palabras:
        ini = 1.0
        pos = visor_texto.search(palabra, ini, stopindex=END)
        while pos:
            longitud = len(palabra)
            fil, col = pos.split('.')
            fin = int(col) + longitud
            fin = fil + '.' + str(fin)
            visor_texto.tag_add("resaltar{}".format(id),pos, fin)
            ini = fin
            pos = visor_texto.search(palabra, ini, stopindex=END)
        visor_texto.tag_config("resaltar{}".format(id), background="white", foreground="{}".format(color))
#END

def analizador(tipo):
    analizadorLexico = None
    if tipo == "js":
        analizadorLexico = AnalizadorLexicoJS()
        messagebox.showinfo(message="Analizar Archivo JS", title="Analizar Archivo")
    elif tipo == "css":
        analizadorLexico = AnalizadorLexicoCSS()
        messagebox.showinfo(message="Analizar Archivo CSS", title="Analizar Archivo")
    elif tipo == "html":
        analizadorLexico = AnalizadorLexicoHTML()
        messagebox.showinfo(message="Analizar Archivo HTML", title="Analizar Archivo")
    elif tipo == "rmt":
        analizadorLexico = AnalizadorLexicoRMT()
        messagebox.showinfo(message="Analizar Archivo RMT", title="Analizar Archivo")


    if analizadorLexico is not None:
        analizadorLexico.analizarCadena(editor_texto.get("1.0", END))
        analizadorLexico.generarReporteErrores()
        try:
            if not tipo == "rmt":
                analizadorLexico.crearArchivoLimpio(label_nombre_archivo.cget("text"))
        except:
            messagebox.showinfo(message="No se puede crear el archivo limpio, agrege una ruta", title="Analizar Archivo")


        for token in analizadorLexico.listaTokens:
            consola.insert(END, "=====================================================\n")
            consola.insert(END, "Token: {}  Lexema: {}  Linea: {}  Columna: {}\n".format(token.getTipo(), token.lexema, token.linea, token.columna))
            consola.insert(END, "=====================================================\n")

        consola.insert(END, "\n"*3)

        for error in analizadorLexico.listaErrores:
            consola.insert(END, error + "\n")
        
        visor_texto.insert(END, analizadorLexico.entradaLimpia)

        return analizadorLexico
#END -----

def jsAnalizador():
    analizadorJS = analizador("js")
    analizadorJS.generarReporteArbol()

    resaltarPalabra(1,analizadorJS.palabrasReservadas, "red")
    resaltarPalabra(2,["+","-","*","/"], "#FA9000")      
    resaltarPalabra(3,analizadorJS.numeros,"blue")
    resaltarPalabra(4,analizadorJS.cadenas, "#E3CC10")
    resaltarPalabra(5,analizadorJS.comentarios, "gray")
    resaltarPalabra(6,analizadorJS.variables, "green")
#END -----

def cssAnalizador():
    analizadorCSS = analizador("css")
    consola.delete("1.0", END)
    for msg in analizadorCSS.bitacora:
         consola.insert(END, "{}\n".format(msg))

    resaltarPalabra(1,analizadorCSS.numeros,"blue")
    resaltarPalabra(2,analizadorCSS.comentarios, "gray")
    resaltarPalabra(3,analizadorCSS.cadenas, "#E3CC10")
    resaltarPalabra(4,analizadorCSS.palabrasReservadasPropiedades, "red")
    resaltarPalabra(5,analizadorCSS.palabrasReservadasUnidades, "red")
#END -----

def htmlAnalizador():
    analizadorHTML = analizador("html")

    resaltarPalabra(1, analizadorHTML.palabrasReservadas, "red")
    resaltarPalabra(2, analizadorHTML.comentarios, "gray")
    resaltarPalabra(3, analizadorHTML.cadenas, "#E3CC10")
    resaltarPalabra(4, re.findall(r'>.*<', visor_texto.get("1.0", END)), "black")
#END -----

def rmtAnalizador():
    analizadorRMT = analizador("rmt")
    # analizadorSintacticoRMT = AnalizadorSintactico()
    # analizadorSintacticoRMT.analizar(analizadorRMT.listaTokens)

    lineas = visor_texto.get("1.0", END).strip().split("\n")
    cad = ""
    
    for linea in lineas:
        rmt_lex = AnalizadorLexicoRMT()
        rmt_lex.analizarCadena(linea)

        rmt_sin = AnalizadorSintactico()
        rmt_sin.analizar(rmt_lex.listaTokens)

        if rmt_sin.error:
            cad += "            <tr>"
            cad += ("                <td>{}</td>".format(linea))                
            cad += ("                <td>{}</td>".format("INCORRECTO"))
            cad += ("            </tr>") 
        else:
            cad += "            <tr>"
            cad += ("                <td>{}</td>".format(linea))                
            cad += ("                <td>{}</td>".format("CORRECTO"))
            cad += ("            </tr>") 

    if not os.path.isdir("reportes/"):
        os.mkdir("reportes/")
    

    file = open("reportes/sintacticormt.html", "w")
    file.write("<!DOCTYPE html>\n<html>\n")
    file.write("<head>\n")
    file.write("    <meta charset=\"UTF-8\">\n")
    file.write("    <title>Reporte Sintactico</title>\n")
    file.write("    <style>")
    file.write("        *{margin:0; padding:0; box-sizing: border-box;}\n")
    file.write("        h1{text-align: center; margin: 30px 0;}\n")
    file.write("        table{border-collapse: collapse; margin: 0 auto; width: 40%;}\n")
    file.write("        td, th{border: 1px solid black; padding: 10px;}\n")
    file.write("       th{background: black; color: white}\n")
    file.write("    </style>\n")
    file.write("</head>\n")
    file.write("<body>\n")
    file.write("    <h1>Reporte de Analisis Sintactico</h1>\n")
    file.write("    <table>\n")
    file.write("        <thead>\n")
    file.write("            <tr>\n")
    file.write("                <th>Operacion</th>\n")
    file.write("                <th>Resultado</th>\n")
    file.write("            </tr>\n")
    file.write("        </thead>\n")
    file.write("        <tbody>")

    file.write("        {}".format(cad))

    file.write("        </tbody>")
    file.write("    </table>\n")        
    file.write("</body>\n")
    file.write("</html>")
    file.close()

    os.system("start ./reportes/sintacticormt.html")
    
#END -----
    



def analizarArchivo():
    if archivo is not None:
        if ".js" in archivo.name:
            limpiarConsola()
            jsAnalizador()
        elif ".css" in archivo.name:
            limpiarConsola()
            cssAnalizador()
        elif ".html" in archivo.name:
            limpiarConsola()
            htmlAnalizador()
        elif ".rmt" in archivo.name:
            limpiarConsola()
            rmtAnalizador()
    else:
        messagebox.showwarning(message="Elija un archivo para poder analizar", title="Analizar Archivo")

    
            
            
menu_principal = Menu(ventana)
menu_principal.add_command(label="Nuevo", command=nuevoArchivo)
menu_principal.add_command(label="Abrir", command=abrirArchivo)
menu_principal.add_command(label="Guardar", command=guardarArchivo)
menu_principal.add_command(label="Guardar Como")
menu_principal.add_command(label="Analizar", command=analizarArchivo)
menu_principal.add_command(label="Salir", command=salirVentana)
ventana.config(menu=menu_principal)


ventana.mainloop()