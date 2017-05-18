from Variable import Variable

class Factor (object):
    """
    Clase Factor para distribuciones de probabilidad conjuntas que implementa
    las operaciones Multiplicación, Reducción, Normalización y Marginalización.
    """

    def __init__ (self, alcance, valores):
        """
        Construye un factor con un alcance (lista de objetos Variable), una
        lista de valores asociados a cada renglón y la tabla de valores de las
        variables de su alcance.
        :param alcance: El alcance del factor.
        :param valores: Los valores de cada renglón.
        """
        self.alcance = alcance
        self.valores = valores
        self.tabla_valores = Variable.tabla_de_valores (alcance)

    def __direccionamiento (self, variables):
        # Método auxiliar que recibe un diccionario de variables y su valor
        # asignado y regresa el índice de la tabla de valores correspondiente.
        r = 0
        for var in self.alcance:
            r = r * len (var.valores_posibles) + variables[var]
        return r

    def __mult_disjunta (self, factor):
        # Multitplicación de factores con alcance disjuntos.
        alcance = self.alcance + factor.alcance
        valores = []
        for t_i in self.valores:
            for t_j in factor.valores:
                valores.append (t_i * t_j)
        return Factor (alcance, valores)

    def multiplicacion (self, factor):
        """
        Multiplica el factor self con el factor dado y regresa el resultado.
        El orden en que aparecen las variables en el factor resultado puede
        cambiar al orden del que aparecen en la unión de sus alcances (como
        listas).
        :param factor: El factor con el que se va a multiplicar.
        """
        interseccion = list (filter (lambda x: x in factor.alcance, self.alcance))
        if interseccion == []:
            return self.__mult_disjunta (factor)
        else:
            valores = []
            V = interseccion[0]
            for s in V.valores_posibles:
                f1 = self.reduccion (V, s)
                f2 = factor.reduccion (V, s)
                f3 = f1.multiplicacion (f2)
                valores += f3.valores
            return Factor ([V] + f3.alcance, valores)

    def reduccion (self, variable, valor):
        """
        Reduce un factor dada una variable y el valor que debe tener dicha
        variable.
        :param variable: La variable con la que se va a reducir.
        :param valor: El valor de la variable que se debe cumplir.
        """
        indice = self.alcance.index (variable)
        c = len (variable.valores_posibles)
        variables = self.alcance.copy ()
        variables.remove (variable)
        gaps = 1
        m = len (self.alcance)
        for i in range (m):
            gaps *= len (self.alcance[m-(i+1)].valores_posibles)
            if m-(i+1) == indice:
                break
        valores = []
        # disgusting, fix!
        try:
            j = 0
            while True:
                m = gaps // c
                for i in range (m):
                    valores.append (self.valores[gaps*j + m*valor + i])
                j += 1
        except Exception:
            pass
        return Factor (variables, valores)

    def normalizacion (self):
        """
        Regresa la normalización del factor self.
        """
        t = sum (self.valores)
        return Factor (self.alcance.copy (), [x / t for x in self.valores])

    def marginalizacion (self, variable):
        """
        Marginaliza una variable del factor.
        :param variable: La variable a marginalizar.
        """
        variables = self.alcance.copy ()
        variables.remove (variable)
        factores = []
        for s in variable.valores_posibles:
            factores.append (self.reduccion (variable, s))
        valores = zip (*[f.valores for f in factores])
        return Factor (variables, list (map (sum, valores)))

    def __str__ (self):
        """
        Representación en string de un factor.
        """
        return self.__repr__ ()

    def __repr__ (self):
        """
        Representación en string de un factor.
        """
        string = '%s\n' % self.alcance
        for t in zip (self.tabla_valores, self.valores):
            string += '{} {:f}\n'.format (*t)
        return string

#