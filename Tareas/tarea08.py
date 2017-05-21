exec(open('Variable.py').read())
exec(open('Factor.py').read())

from Variable import Variable
from Factor import Factor

# Ejercicio 1
R = Variable ('R',[0,1])
T = Variable ('T',[0,1])
A = Variable ('A',[0,1])
J = Variable ('J',[0,1])
M = Variable ('M',[0,1])

pR = Factor ([R],[0.999,0.001])
pT = Factor ([T],[0.998,0.002])
pA_RT = Factor ([R,T,A],[0.999,0.001,0.71,0.29,0.06,0.94,0.05,0.95])
pJ_A = Factor ([A,J],[0.95,0.05,0.1,0.9])
pM_A = Factor ([A,M],[0.99,0.01,0.3,0.7])

fb1 = pR.multiplicacion (pA_RT)
fb2 = fb1.multiplicacion (pT)
fb3 = pR.multiplicacion (pT)
fc1 = fb2.marginalizacion (A)
fc2 = fc1.marginalizacion (R)

# Ejercicio 2
V1 = Variable ('V1',[0,1])
V2 = Variable ('V2',[0,1])
M = Variable ('M',[0,1])

pM = Factor ([M],[0.5,0.5])
pV1_M = Factor ([M,V1],[.9,.1,.5,.5])
pV2_M = Factor ([M,V2],[.9,.1,.5,.5])
pV1 = pV1_M.multiplicacion (pM).marginalizacion (M)
pV2 = pV2_M.multiplicacion (pM).marginalizacion (M)
pV2V1 = pV2_M.multiplicacion (pV1_M).multiplicacion (pM).marginalizacion (M)
pV2_V1 = Factor (pV2V1.alcance, [0.53/0.7,0.17/0.3,0.17/0.7,0.13/0.3])
