from perceptron import Perceptron
from itertools import product

class RedXOR (object):
	"""
	Clase RedXOR para modelar una red neuronal capaz de calcular la operación
	lógica XOR. Recordemos que XOR se calcula como:
	v1 XOR v2 = (v1 OR v2) AND (v1 NAND v2)
	Por lo que se necesitan 3 perceptrones, uno para calcular el OR, otro para
	calcular el NAND (éstos dos corresponden a la capa oculta) y otro para AND
	(capa de salida, pues es la última operación a realizar).
	"""

	def __init__ (self):
		"""
		Crea una red neuronal para calcular XOR.
		Los perceptrones se crean con una tasa de aprendizaje de 0.3, umbral
		de error 0 y función de activación Paso unitario. Los tres perceptrones
		se entrenan completamente para su operación lógica dada.
		"""
		self.f = lambda x : 0 if x < 0 else 1
		self.tabla = list (map (list, product (*([[0,1]]*2))))
		self.__inputs = 2
		# h1 se entrena para calcular OR.
		self.h1 = Perceptron (2, self.f, 0.3, 0)
		print ('Entrenamiento Perceptrón h1 (OR).\n')
		self.h1.entrenamiento (self.tabla, [0,1,1,1], 200)
		# h2 se entrena para calcular NAND.
		self.h2 = Perceptron (2, self.f, 0.3, 0)
		print ('\nEntrenamiento Perceptrón h2 (NAND).\n')
		self.h2.entrenamiento (self.tabla, [1,1,1,0], 200)
		# o calcula la salida de la red. Calcula un AND
		self.o = Perceptron (2, self.f, 0.3, 0)
		print ('\nEntrenamiento Perceptrón o (AND).\n')
		self.o.entrenamiento (self.tabla, [0,0,0,1], 200)
		self.__salidas = [0,0,0]
		print ('\n')

	def salida (self, entradas):
		"""
		Calcula la salida de la red sobre el conjunto de entradas dado.
		:param entradas: Las entradas de la red.
		"""
		if len (entradas) != self.__inputs:
			raise Exception ('Número de entradas incorrecto.')
		self.__salidas[0] = self.h1.salida (entradas)
		self.__salidas[1] = self.h2.salida (entradas)
		self.__salidas[2] = self.o.salida (self.__salidas[0:2])
		return self.__salidas[2]
