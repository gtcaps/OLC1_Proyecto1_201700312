import os
from tkinter import *
from tkinter import filedialog, messagebox
from AnalizadorLexicoJS.AnalizadorLexico import AnalizadorLexicoJS

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

def limpiarEditor():
    editor_texto.delete("1.0", END)
    visor_texto.delete("1.0", END)

def salirVentana():
    ventana.destroy()

def abrirArchivo():
    global archivo
    archivo = filedialog.askopenfile(mode="r", filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css")])
    if archivo is not None:
        limpiarEditor()
        contenido = archivo.read()
        editor_texto.insert(END, contenido)
        label_nombre_archivo["text"] = os.path.basename(archivo.name)

def nuevoArchivo():
    global archivo
    archivo = filedialog.asksaveasfile(filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css")])
    if archivo is not None:
        limpiarEditor()
        label_nombre_archivo["text"] = os.path.basename(archivo.name)

def guardarArchivo():
    global archivo
    texto = editor_texto.get("1.0", END)

    if archivo is None:
        archivo = filedialog.asksaveasfile(filetypes=[("JS Files","*.js"),("HTML Files","*.html"),("CSS Files","*.css")])
        label_nombre_archivo["text"] = os.path.basename(archivo.name)
        archivo.write(texto)
        archivo.close()
    else:
        f = open(archivo.name, "w")
        f.write(texto)
        f.close()

def guardarArchivoComo():
    pass

def jsAnalizador():
    messagebox.showinfo(message="Analizar Archivo JS", title="Analizar Archivo")
    analizadorJS = AnalizadorLexicoJS()
    analizadorJS.analizarCadena(editor_texto.get("1.0",END))
    analizadorJS.generarReporteErrores()
    analizadorJS.generarReporteArbol()
    analizadorJS.crearArchivoLimpio(label_nombre_archivo.cget("text"))

    for token in analizadorJS.listaTokens:
        consola.insert(END, "=====================================================\n")
        consola.insert(END, "Token: {}  Lexema: {}  Linea: {}  Columna: {}\n".format(token.getTipo(), token.lexema, token.linea, token.columna))
        consola.insert(END, "=====================================================\n")

    consola.insert(END, "\n"*3)

    for error in analizadorJS.listaErrores:
        consola.insert(END, error + "\n")

    visor_texto.insert(END, analizadorJS.entradaLimpia)
    

    


def analizarArchivo():
    if archivo is not None:
        if ".js" in archivo.name:
            limpiarConsola()
            jsAnalizador()
    else:
        messagebox.showwarning(message="Elija un archivo para poder analizar", title="Analizar Archivo")

    
            
            
menu_principal = Menu(ventana)
menu_principal.add_command(label="Nuevo", command=nuevoArchivo)
menu_principal.add_command(label="Abrir", command=abrirArchivo)
menu_principal.add_command(label="Guardar", command=guardarArchivo)
menu_principal.add_command(label="Guardar Como")
menu_principal.add_command(label="Analizar", command=analizarArchivo)
menu_principal.add_command(label="Reportes")
menu_principal.add_command(label="Salir", command=salirVentana)
ventana.config(menu=menu_principal)


ventana.mainloop()


# #POSIBLE SOLUCION PARA PINTAR
# # palabra = "es"
# # editor_texto.tag_config("start", background="black", foreground="red")
# # pos = editor_texto.search(palabra, "1.0", stopindex=END)
# # print(pos)

# # if pos:
# #     end_pos = "{}+{}c".format(pos, len(palabra))
# #     print("{}".format(end_pos))
# #     editor_texto.tag_add("resaltar", pos, end_pos)
# #     editor_texto.tag_config("resaltar", foreground="red")