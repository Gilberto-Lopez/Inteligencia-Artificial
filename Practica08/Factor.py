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
        return 0

    def multiplicacion (self, factor):
        pass

    def reduccion (self, variable, valor):
        pass

    def normalizacion (self):
        """
        Regresa la normalización del factor self.
        """
        t = sum (self.valores)
        return Factor (self.alcance.copy (), [x / t for x in self.valores])

    def marginallizacion (self, variable):
        pass

#