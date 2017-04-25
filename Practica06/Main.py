from perceptron import Perceptron
from itertools import product
from random import randint, choice

def and_list (list):
	for e in list:
		if e == 0:
			return e
	return 1

def or_list (list):
	for e in list:
		if e == 1:
			return e
	return 0

# Ejemplares de entrenamiento (eliminar repeticiones)
#	for _ in range (randint (0, len(tabla)-1)):
#		<ej_nombre>.append (choice (tabla))

# Unit step function
f = lambda x : 0 if x < 0 else 1

if __name__ == '__main__':
	# Conjunto de entradas para probar los perceptrones.
	cjto_entradas = [[0]*3,[1,0,1],[0,0,1],[1]*3]
	cjto_salidas_and = [0,0,0,1]
	cjto_salidas_or = [0,1,1,1]

	# Tabla de entradas
	tabla = list (map (list, product (*([[0,1]]*3))))
	# Salidas del AND
	salida_and = [0 for _ in range(7)] + [1]
	# Salidas del OR
	salida_or = [0] + [1 for _ in range(7)]

	# Conjuntos de entrenamiento

	# 1.
	cjto_1 = [tabla[0],tabla[-1]]
	salidas_1_and = [0,1]
	salidas_1_or = [0,1]

	# 2.
	cjto_2 = tabla
	salidas_2_and = salida_and
	salidas_2_or = salida_or

	# 3.
	cjto_3 = [[1, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 1]]
	salidas_3_and = list (map (and_list, cjto_3))
	salidas_3_or = list (map (or_list, cjto_3))

	# 4.
	cjto_4 = [[0, 1, 1], [0, 0, 0], [0, 1, 0], [1, 1, 1]]
	salidas_4_and = list (map (and_list, cjto_4))
	salidas_4_or = list (map (or_list, cjto_4))

	# 5.
	cjto_5 = [[1, 1, 0], [0, 1, 0], [1, 1, 1]]
	salidas_5_and = list (map (and_list, cjto_5))
	salidas_5_or = list (map (or_list, cjto_5))

	# Perceptrones AND

	# 1.
	print ('***** Perceptron AND 1 *****')
	p_and_1 = Perceptron (3, f, 0.01, 0)
	print ('Tasa de aprendizaje:\t', p_and_1.alpha)
	print ('Pesos:\t', [p_and_1.theta] + p_and_1.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_1, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_and_1.entrenamiento (cjto_1, salidas_1_and, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_and):
		out = p_and_1.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 2.
	print ('***** Perceptron AND 2 *****')
	p_and_2 = Perceptron (3, f, 0.1, 0)
	print ('Tasa de aprendizaje:\t', p_and_2.alpha)
	print ('Pesos:\t', [p_and_2.theta] + p_and_2.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_2, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_and_2.entrenamiento (cjto_2, salidas_2_and, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_and):
		out = p_and_2.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 3.
	print ('***** Perceptron AND 3 *****')
	p_and_3 = Perceptron (3, f, 0.01, 0)
	print ('Tasa de aprendizaje:\t', p_and_3.alpha)
	print ('Pesos:\t', [p_and_3.theta] + p_and_3.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_3, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_and_3.entrenamiento (cjto_3, salidas_3_and, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_and):
		out = p_and_3.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 4.
	print ('***** Perceptron AND 4 *****')
	p_and_4 = Perceptron (3, f, 0.01, 0)
	print ('Tasa de aprendizaje:\t', p_and_4.alpha)
	print ('Pesos:\t', [p_and_4.theta] + p_and_4.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_4, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_and_4.entrenamiento (cjto_4, salidas_4_and, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_and):
		out = p_and_4.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 5.
	print ('***** Perceptron AND 5 *****')
	p_and_5 = Perceptron (3, f, 0.1, 0)
	print ('Tasa de aprendizaje:\t', p_and_5.alpha)
	print ('Pesos:\t', [p_and_5.theta] + p_and_5.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_5, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_and_5.entrenamiento (cjto_5, salidas_5_and, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_and):
		out = p_and_5.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# Perceptrones OR

	# 1.
	print ('***** Perceptron OR 1 *****')
	p_or_1 = Perceptron (3, f, 0.3, 0)
	print ('Tasa de aprendizaje:\t', p_or_1.alpha)
	print ('Pesos:\t', [p_or_1.theta] + p_or_1.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_1, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_or_1.entrenamiento (cjto_1, salidas_1_or, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_or):
		out = p_or_1.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 2.
	print ('***** Perceptron OR 2 *****')
	p_or_2 = Perceptron (3, f, 0.3, 0)
	print ('Tasa de aprendizaje:\t', p_or_2.alpha)
	print ('Pesos:\t', [p_or_2.theta] + p_or_2.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_2, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_or_2.entrenamiento (cjto_2, salidas_2_or, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_or):
		out = p_or_2.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 3.
	print ('***** Perceptron OR 3 *****')
	p_or_3 = Perceptron (3, f, 0.1, 0)
	print ('Tasa de aprendizaje:\t', p_or_3.alpha)
	print ('Pesos:\t', [p_or_3.theta] + p_or_3.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_3, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_or_3.entrenamiento (cjto_3, salidas_3_or, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_or):
		out = p_or_3.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 4.
	print ('***** Perceptron OR 4 *****')
	p_or_4 = Perceptron (3, f, 0.1, 0)
	print ('Tasa de aprendizaje:\t', p_or_4.alpha)
	print ('Pesos:\t', [p_or_4.theta] + p_or_4.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_4, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_or_4.entrenamiento (cjto_4, salidas_4_or, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_or):
		out = p_or_4.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')

	# 5.
	print ('***** Perceptron OR 5 *****')
	p_or_5 = Perceptron (3, f, 0.03, 0)
	print ('Tasa de aprendizaje:\t', p_or_5.alpha)
	print ('Pesos:\t', [p_or_5.theta] + p_or_5.pesos)
	print ('Conjunto de entrenamiento:\t', cjto_5, '\n')
	print ('-----Proceso de entrenamiento\n')
	p_or_5.entrenamiento (cjto_5, salidas_5_or, 200)
	print ('-----Pruebas\n')
	for (ej, s) in zip (cjto_entradas, cjto_salidas_or):
		out = p_or_5.salida (ej)
		print ('Entrada:\t', ej, '\n\tSalida:\t', out, '\tSalida esperada:\t', s)
	print ('\n')
