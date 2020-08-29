from AnalizadorLexicoJS.AnalizadorLexico import AnalizadorLexicoJS


# ====ANALIZADOR PARA JAVASCRIPT
analizadorJS = AnalizadorLexicoJS()
analizadorJS.analizarArchivo("archivo.js")
analizadorJS.imprimirTokens()
print("\n\n\n")
analizadorJS.imprimirErrores()

