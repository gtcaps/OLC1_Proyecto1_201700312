import re
import pathlib
from AnalizadorLexicoJS.AnalizadorLexico import AnalizadorLexicoJS
from AnalizadorLexicoCSS.AnalizadorLexico import AnalizadorLexicoCSS


# # ====ANALIZADOR PARA JAVASCRIPT
# analizadorJS = AnalizadorLexicoJS()
# analizadorJS.analizarArchivo("archivo.js")
# # analizadorJS.imprimirTokens()
# # print("\n\n\n")
# # analizadorJS.imprimirErrores()


# cadena = "c:\\hola\\mundo"
# # patron = r'([a-zA-Z]:\\)(\w+\\)+'
# # encontrar = re.search(patron, cadena.read())
# print(re.sub(r'[a-zA-Z]:\\','',cadena))
# pathlib.Path(re.sub(r'[a-zA-Z]:\\','',cadena)).mkdir(parents=True, exist_ok=True)

analizadorCSS = AnalizadorLexicoCSS()
analizadorCSS.analizarArchivo("archivos_prueba/archivo.css")
analizadorCSS.imprimirTokens()
print("\n\n\n")
analizadorCSS.imprimirErrores()
analizadorCSS.generarReporteErrores()