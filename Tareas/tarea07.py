import numpy as np
import math

xi = [-0.6861007046,0.1845728382,-2.3158346172,-1.0254515503,0.4311453719,0.8427785188,-0.9005654622,0.1421184987,2.0068530366,3.5943855252]
yi = [-1.7317977268,0.451296404,-0.6509207096,-0.0809364635,0.8026880194,-1.0716033783,1.2787579969,-1.213108765,-1.4894149248,-0.8032932784]
Y = [0,1,0,1,0,1,0,1,1,0]
xi2 = [r**2 for r in xi]
yi2 = [r**2 for r in yi]

xi = np.transpose(np.matrix(xi))
yi = np.transpose(np.matrix(yi))
xi2 = np.transpose(np.matrix(xi2))
yi2 = np.transpose(np.matrix(yi2))
Y = np.transpose(np.matrix(Y))
X = np.hstack ((np.matrix ([[1] for _ in range (len (xi))]), xi, xi2, yi, yi2))

alpha = 0.3

def sigmoid (z):
	return 1.0 / (1 + np.exp (-z))

def J (Theta, X, Y):
	m = len (X)
	l = [0 for _ in range (m)]
	H = sigmoid (np.dot (X, Theta))
	# Costo
	for i in range (m):
		if Y[0,i] == 0:
			l[i] = -np.log (1 - H[0,i])
		else:
			l[i] = -np.log (H[0,i])
	return sum (l) / float (m)

def desc_grad (Theta, X, Y, e = 0.03):
	n = len (Theta)
	Rt = [0 for _ in range (n)]
	while J (Theta, X, Y) >= e:
		H = sigmoid (np.dot (X, Theta)) - Y
		for i in range (n):
			Rt[i] = Theta[0,i] - alpha * np.dot (np.transpose (X[:,i]), H)[0,0]
		Theta = np.transpose (np.matrix (Rt))
