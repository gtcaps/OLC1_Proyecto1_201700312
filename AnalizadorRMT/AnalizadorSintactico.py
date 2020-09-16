from AnalizadorRMT.Token import *

class AnalizadorSintactico:

    def analizar(self, listaTokens):
        self.listaTokens = listaTokens
        self.error = False
        self.pos = 0
        self.tokenPreAnalisis = self.listaTokens[self.pos]
        self.E()
        
    #END -----

    def E(self):
        self.T()
        self.EP()
    #END -----

    def EP(self):
        if self.tokenPreAnalisis.getTipo() == 'Suma':
            self.match("Suma")
            self.T()
            self.EP()
        elif self.tokenPreAnalisis.getTipo() == 'Resta':
            self.match("Resta")
            self.T()
            self.EP()
    #END -----

    def T(self):
        self.F()
        self.TP()
    #END -----

    def TP(self):
        if self.tokenPreAnalisis.getTipo() == "Multiplicacion":
            self.match("Multiplicacion")
            self.F()
            self.TP()
        elif self.tokenPreAnalisis.getTipo() == "Division":
            self.match("Division")
            self.F()
            self.TP()
    #END -----

    def F(self):
        if self.tokenPreAnalisis.getTipo() == "Parentesis Izquierdo":
            self.match("Parentesis Izquierdo")
            self.E()
            self.match("Parentesis Derecho")
        elif self.tokenPreAnalisis.getTipo() == "Numero":
            self.match("Numero")
        elif self.tokenPreAnalisis.getTipo() == "Variable":
            self.match("Variable")
        # else:
        #     self.error = True
        #     print("Error en {}".format(self.tokenPreAnalisis.lexema))
    #END -----

    def match(self, tipo):
        if tipo != self.tokenPreAnalisis.getTipo():
            self.error = True
            print("Error en {}".format(self.tokenPreAnalisis.lexema))

        if self.pos < len(self.listaTokens) - 1:
            self.pos += 1
            self.tokenPreAnalisis = self.listaTokens[self.pos]
    #END -----
        
        
        
