# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


class CongruenteLinear:
    def __init__(self, a: int, m: int, seed: int, c:int, uniformimenteDistribuido: bool):
        self.a = a
        self.m = m
        self.seed = seed
        self.c = c
        self.uniformimenteDistribuido = uniformimenteDistribuido
        self.primeiroNumero = True 

        self.cont = 0 
        #self.arrayTeste = [0.3276, 0.8851, 0.1643, 0.5542, 0.6813, 0.7221, 0.9881]

    def geraAleatorio(self):
        """ 
        r = self.arrayTeste[self.ponteiro]
        
        return r
        """
        self.cont += 1

        if self.primeiroNumero:
            self.primeiroNumero = False
            self.x0 = ((self.a*self.seed) + self.c) % self.m
            self.xn = self.x0
            if self.uniformimenteDistribuido:
                return abs(self.x0 / self.m)
            else:
                return abs(self.x0)
        else:
            self.xn = ((self.a*self.xn) + self.c )% self.m
            if self.uniformimenteDistribuido:
                return abs(self.xn / self.m)
            else:
                return abs(self.xn)
            
            
    





