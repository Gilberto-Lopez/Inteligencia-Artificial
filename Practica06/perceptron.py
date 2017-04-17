from random import uniform

class Perceptron (object):
	"""
	Clase Perceptron para modelar un perceptón.
	"""

	def __init__ (self, pesos = 4, activacion):
		"""
		Inicializa un perceptrón con una cantidad fija de pesos
		para las entradas (por defecto 4), establecidos como
		números aleatorios en el intervalo [-0.5,0.5], y un
		umbral para comparar la salida del perceptrón en ese
		mismo intervalo. También recibe la función de activación
		para el preceptrón
		:param pesos: La cantidad de pesos/entradas del perceptrón.
		:param activacion: La función de activación.
		"""
		self.entradas = pesos
		self.pesos = [uniform (-0.5,0.5) for _ in range (pesos)]
		self.umbral = uniform (-0.5,0.5)
		self.activacion = activacion

	def salida (self, entradas):
		"""
		Calcula la salida del perceptrón para un ejemplar dado.
		La salida del perceptrón está dada por:
			Y = f(Sum_i (w_i.x_i) - umbral)
		donde x_i es el i-ésimo valor de entrada, w_i el i-ésimo peso para x_i
		y f es la función de activación del perceptrón.
		:param entradas: Los valores de entrada para el perceptrón (ejemplar).
		"""
		if len (entradas) != self.entradas:
			return 0
		suma_ponderada = sum (w_i * x_i for (w_i, x_i) in zip (self.pesos, entradas))
		return self.activacion (suma_ponderada - self.umbral)

	def entrenamiento (self):
		pass