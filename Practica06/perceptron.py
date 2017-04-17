from random import uniform
import math

class Perceptron (object):
	"""
	Clase Perceptron para modelar un perceptón.
	"""

	def __init__ (self, n, activacion, tasa_aprendizaje = 0.1, error = 0.1):
		"""
		Inicializa un perceptrón con una cantidad fija de pesos para las
		entradas, establecidos como números aleatorios en el intervalo
		[-0.5,0.5], y un umbral para comparar la salida del perceptrón en ese
		mismo intervalo. También recibe la función de activación para el
		preceptrón, la tasa de aprendizaje (en el intervalo (0,1)) y el umbral
		de error para el entrenamiento (no negativo).
		:param n: El número de entradas del perceptrón.
		:param activacion: La función de activación.
		:param tasa_aprendizaje: La tasa de aprendizaje.
		:param error: Umbral de error para el entrenamiento.
		"""
		self.n = n
		# n+1 pesos por el sesgo.
		self.pesos = [uniform (-0.5, 0.5) for _ in range (n+1)]
		self.theta = uniform (-0.5, 0.5)
		self.f = activacion
		self.alpha = tasa_aprendizaje if 0 < tasa_aprendizaje < 1 else 0.1
		self.error = error

	def salida (self, entradas):
		"""
		Calcula la salida del perceptrón para un ejemplar dado.
		La salida del perceptrón está dada por:
			Y = f(Sum i (w_i.x_i) - theta)
		donde x_i es el i-ésimo valor de entrada, w_i el i-ésimo peso para x_i,
		theta el umbral y f es la función de activación del perceptrón.
		:param entradas: Los valores de entrada para el perceptrón (ejemplar).
		"""
		if len (entradas) != self.n:
			return float('nan')
		# El sesgo
		entradas = [1] + entradas
		suma_ponderada = sum ([w_i * x_i for (w_i, x_i) in zip (self.pesos, entradas)])
		return self.f (suma_ponderada - self.theta)

	def _entrenamiento (self, ejemplar, salida):
		# Método auxiliar para entrenamiento(), calcula el error del perceptrón
		# con un ejemplar dado y actualiza los pesos del perceptrón.
		salida_perceptron = self.salida (ejemplar)
		if math.isnan (salida_perceptron):
			return salida_perceptron
		error = salida - salida_perceptron
		if error != 0:
			self.pesos = [w_i + self.alpha * x_i * error for (w_i, x_i) in zip (self.pesos, ejemplar)]
		return error

	def entrenamiento (self, conjunto, salida):
		"""
		Proceso de entrenamiento de perceptrón. Itera sobre el conjunto de
		ejemplares de entrada las veces necesarias hasta minimizar el error
		de la salida del perceptrón por debajo del umbral de error permitido.
		:param conjunto: El conjunto de ejemplares para el entrenamiento.
		:param salida: El conjunto de salidas esperadas para cada ejemplar.
		"""
		while True:
			for (ejemplar_j, salida_j) in zip (conjunto, salida):
				error_t = self._entrenamiento (ejemplar_j, salida_j)
				if math.isnan (error_t):
					return
				if abs (error_t) <= self.error:
					return