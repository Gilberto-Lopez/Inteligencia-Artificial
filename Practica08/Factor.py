from itertools import product

class Factor (object):

	def __init__ (self, variables, probabilidades):
		"""
		Crea un nuevo factor con la lista de variables dadas y las
		probabilodades correspondientes a cada renglón del factor, en el orden
		en que se listan las variables y la cardinalidad de su soporte.
		:param variables: La lista de variables del factor.
		:param probabilidades: Las probabilidades del factor (una entrada por)
		                       renglón.
		"""
		# Listas de pares llave-valor:
		# Llave: Nombre de la variable, "X"
		# Valor: Carindalidad del soporte de la variable, 3 -> [0,1,2]
		self.variables = variables
		# Lista de números:
		# Renglones del factor, ordenados en el orden que aparecen las
		# variables en self.variables
		self.probabilidades = probabilidades

	def __indice (self, variable):
		# Busca el índice de una variable en la lista de variables del factor
		# Si no la encuentra regresa -1
		i = 0
		for (k, _) in self.variables:
			if k == variable:
				return i
			i += 1
		return -1

	@classmethod
	def multiplicacion (factor1, factor2):
		"""
		Multiplica los factores dados, FACTOR1 y FACTOR2, y regresa el
		resultado.
		:param factor1: El primer factor.
		:param factor2: El segundo factor.
		"""
		pass

	def reduccion (self, variable, valor):
		indice = self.__indice (variable)
		c = self.variables[indice][1]
		variables = [(k, v) for (k, v) in self.variables if k != variable]
		sop = [v for (k, v) in self.variables]
		gaps = 1
		m = len (sop)
		for i in range (m):
			if m-(i+1) == indice:
				break
			gaps *= sop[m-(i+1)]
		probabilidades = []
		# disgusting, fix!
		try:
			j = 0
			while True:
				probabilidades.append (self.probabilidades[c*gaps*j + valor])
				j += 1
		except Exception:
			pass
		return Factor (variables, probabilidades)

	def normalizar (self):
		"""
		Normaliza el factor.
		"""
		t = sum (self.probabilidades)
		self.probabilidades = [x / t for x in self.probabilidades]

	def marginalizar (self, variable):
		pass
