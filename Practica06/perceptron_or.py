from perceptron import Perceptron
from itertools import product

class PerceptronOR(Perceptron):
	"""
	Clase PerceptronOR para modelar un perceptrón que reconozca la operación
	lógica OR de tres variables.
	"""

	def __init__(self):
		"""
		Inicializa el perceptrón usando como función de activación la función
		escalón.
		"""
		super (PerceptronOR, self).__init__ (3,lambda x: 0 if x < 0 else 1)
		self.tabla_or = list (map (list, product (*([[0,1]]*3))))
		self.salida_or = [0] + [1 for _ in range(7)]
