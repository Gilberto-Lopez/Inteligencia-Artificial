from random import uniform
import math

class Perceptron (object):
	"""
	Clase Perceptron para modelar un perceptón.
	"""

	def __init__ (self, pesos = 4, activacion, tasa_aprendizaje = 0.1):
		"""
		Inicializa un perceptrón con una cantidad fija de pesos
		para las entradas (por defecto 4), establecidos como
		números aleatorios en el intervalo [-0.5,0.5], y un
		umbral para comparar la salida del perceptrón en ese
		mismo intervalo. También recibe la función de activación
		para el preceptrón y la tasa de aprendizaje, en el intervalo (0,1)
		:param pesos: La cantidad de pesos/entradas del perceptrón.
		:param activacion: La función de activación.
		:param tasa_aprendizaje: La tasa de aprendizaje.
		"""
		self.entradas = pesos
		self.pesos = [uniform (-0.5,0.5) for _ in range (pesos)]
		self.theta = uniform (-0.5,0.5)
		self.f = activacion
		self.alpha = tasa_aprendizaje if 0 < tasa_aprendizaje < 1 else 0.1

	def salida (self, entradas):
		"""
		Calcula la salida del perceptrón para un ejemplar dado.
		La salida del perceptrón está dada por:
			Y = f(Sum i (w_i.x_i) - theta)
		donde x_i es el i-ésimo valor de entrada, w_i el i-ésimo peso para x_i,
		theta el umbral y f es la función de activación del perceptrón.
		:param entradas: Los valores de entrada para el perceptrón (ejemplar).
		"""
		if len (entradas) != self.entradas:
			return float('nan')
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
		pass
