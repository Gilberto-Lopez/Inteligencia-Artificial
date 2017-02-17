#!/usr/bin/env python
# -*- coding: utf-8 -*-

# El espacio de estados es pequeño y
# la cantidad de acciones también, por
# lo que no hay optimizaciones.

def estado_v (s):
	"""
	True si s pertenece al conjunto S.
	False en otro caso.
	"""
	return (0 <= s[0] <= 3 and
		0 <= s[1] <= 3 and
		(s[0] >= s[1] or s[0] == 0) and
		(s[0] <= s[1] or s[0] == 3))

def accion_v (a):
	"""
	True si a pertenece al conjunto A.
	Flase en otro caso.
	"""
	return (0 <= a[0] <= 2 and
		0 <= a[1] <= 2 and
		1 <= a[0] + a[1] <= 2)

def gamma (s,a):
	"""
	Función de transición gamma.
	"""
	if estado_v(s) and accion_v(a):
		if a[0] <= s[0] and a[1] <= s[1] and a[2] != s[2] and a[2] == 'd':
			return [(s[0]-a[0],s[1]-a[1],a[2])]
		elif a[0] + s[0] <= 3 and a[1] + s[1] <= 3 and a[2] != s[2] and a[2] == 'i':
			return [(s[0]+a[0],s[1]+a[1],a[2])]
		else:
			return []
	else:
		return []

Acciones = []
#[(0,1,'i'),(0,2,'i'),(1,0,'i'),(1,1,'i'),(2,0,'i'),(0,1,'d'),(0,2,'d'),(1,0,'d'),(1,1,'d'),(2,0,'d')]
for i in range(4):
	for j in range(4):
		Acciones.append((i,j,'i'))
		Acciones.append((i,j,'d'))

def Gamma (s):
	"""
	Función sucesor Gamma.
	"""
	c = []
	for a in Acciones:
		c = c + gamma(s,a)
	return c

def explora():
	"""
	Calcula la cerradura transitiva desde el estado inicial (3,3,'i').
	"""
	gs = [[(3,3,'i')]]
	cjto = [(3,3,'i')]
	i = 0

	while True:
		l = []
		for s in gs[i]:
			l = l+Gamma(s)
		cambio = False
		for t in l:
			if not t in cjto:
				cjto.append(t)
				cambio = True
		if cambio:
			i+=1
			gs.append(l)
		else:
			break
	return cjto
