from itertools import product

class Variable (object):
    """
    Clase Variable, representa una variable aleatoria para la clase Factor.
    """

    def __init__ (self, nombre, valores_posibles):
        """
        Constructor, crea una nueva variable con el nombre y los posibles
        valores que puede tomar.
        :param nombre: El nombre de la variable.
        :param valores_posibles: Los posibles valores que puede tomar la
                                 variable.
        """
        self.nombre = nombre
        self.valores_posibles = valores_posibles

    def __str__ (self):
        """
        Representación de una variable: Su nombre.
        """
        return self.nombre

    def __repr__ (self):
        """
        Representación de una variable: Su nombre.
        """
        return self.__str__ ()

    def __eq__ (self, other):
        """
        Comparación de variables. Dos variables son iguales si tienen el mismo
        nombre y la misma lista de valores posibles en el mismo orden.
        :param other: La variable con la que se desea comparar.
        """
        return (self.nombre == other.nombre
            and self.valores_posibles == other.valores_posibles)

    @staticmethod
    def tabla_de_valores (variables):
        """
        Regresa la tabla de valores con todas las combinaciones de los valores
        que pueden tomar las variables.
        :param variables: La lista de variables.
        """
        return list (map (list, product (*[x.valores_posibles for x in variables])))

#