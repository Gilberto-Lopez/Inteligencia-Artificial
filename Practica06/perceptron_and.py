from perceptron import Perceptron
from itertools import product

class PerceptronAND(Perceptron):
	"""
	Clase PerceptronAND para modelar un perceptrón que reconozca la operación
	lógica AND de tres variables.
	"""

	def __init__(self):
		"""
		Inicializa el perceptrón usando como función de activación la función
		escalón.
		"""
		super (PerceptronAND, self).__init__ (3,lambda x: 0 if x < 0 else 1)
		self.tabla_and = map(list, product (*([[0,1]]*3)))
		self.salida = [0 for _ in range(7)] + [1]
