from AnalizadorLexicoJS.AnalizadorLexico import AnalizadorLexicoJS

# ====ANALIZADOR PARA JAVASCRIPT
analizadorJS = AnalizadorLexicoJS()
analizadorJS.analizar("var edad = 18;")
analizadorJS.imprimirTokens()