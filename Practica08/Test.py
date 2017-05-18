from Variable import Variable
from Factor import Factor

if __name__ == '__main__':
	vA = Variable ('A',[0,1])
	vB = Variable ('B',[0,1])

	fA = Factor ([vA],[.3,.7])
	print (fA)
	fB = Factor ([vB],[.6,.4])
	print (fB)

	print ('Multiplicación de los factores A y B')
	fAB = fA.multiplicacion (fB)
	print (fAB)

	vC = Variable ('C',[0,1])

	fAC = Factor ([vA,vC],[.27*.54,.1*.4,.66*.9,.32*.15])
	print (fAC)

	print ('\nMultiplicación de los factores AB y AC')
	fABC = fAB.multiplicacion (fAC)
	print (fABC)

	print ('\nReducción de AB con A = 0')
	fB_rA0 = fAB.reduccion (vA, 0)
	print (fB_rA0)

	print ('\nNormalización de B con A = 0')
	fBN = fB_rA0.normalizacion ()
	print (fBN)

	print ('\nMarginalización de AB con B')
	fA_mB = fAB.marginalizacion (vB)
	print (fA_mB)

#