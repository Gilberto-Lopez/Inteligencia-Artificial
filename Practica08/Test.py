from Variable import Variable
from Factor import Factor

if __name__ == '__main__':
	vA = Variable ('A',[0,1])
	vB = Variable ('B',[0,1])

	fA = Factor ([vA],[.3,.7])
	fB = Factor ([vB],[.6,.4])

	print ('Multiplicación de los factores A y B')
	fAB = fA.multiplicacion (fB)
	print ("%s" % fAB.alcance)
	for (r,v) in zip (fAB.tabla_valores, fAB.valores):
		print (r, v)

	vC = Variable ('C',[0,1])

	fAC = Factor ([vA,vC],[.27*.54,.1*.4,.66*.9,.32*.15])

	print ('\nMultiplicación de los factores AB y AC')
	fABC = fAB.multiplicacion (fAC)
	print ("%s" % fABC.alcance)
	for (r,v) in zip (fABC.tabla_valores, fABC.valores):
		print (r, v)

	print ('\nReducción de AB con A = 0')
	fB_rA0 = fAB.reduccion (vA, 0)
	print ("%s" % fB_rA0.alcance)
	for (r,v) in zip (fB_rA0.tabla_valores, fB_rA0.valores):
		print (r, v)

	print ('\nNormalización de B con A = 0')
	fBN = fB_rA0.normalizacion ()
	print ("%s" % fBN.alcance)
	for (r,v) in zip (fBN.tabla_valores, fBN.valores):
		print (r, v)

	print ('\nMarginalización de AB con B')
	fA_mB = fAB.marginalizacion (vB)
	print ("%s" % fA_mB.alcance)
	for (r,v) in zip (fA_mB.tabla_valores, fA_mB.valores):
		print (r, v)
