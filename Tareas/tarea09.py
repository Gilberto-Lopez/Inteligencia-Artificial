exec(open('Variable.py').read())
exec(open('Factor.py').read())

MA = Variable('MA',[0,1])
MP = Variable('MP',[0,1])
AA = Variable('AA',[0,1])
AP = Variable('AP',[0,1])
JA = Variable('JA',[0,1])
JP = Variable('JP',[0,1])
BA = Variable('BA',[0,1])
BP = Variable('BP',[0,1])
LI = Variable('LI',[0,1])
LF = Variable('LF',[0,1])
FIN = Variable('FIN',[0,1])
E = Variable('E',[0,1])
IT = Variable('IT',[0,1])
VP = Variable('VP',[0,1])

pLF = Factor([LF],[0.78,0.22])
pLI = Factor([LI],[0.78,0.22])
pFIN = Factor([FIN],[0.72,0.28])
pIT = Factor([IT],[0.7,0.3])
pE = Factor([E],[0.35,0.65])

pJA_LI = Factor([JA,LI],[0.1,0.6,0.9,0.4])
pAA_FIN = Factor([AA,FIN],[0.6,0.2,0.4,0.8])
pBA_IT = Factor([BA,IT],[0.05,0.7,0.95,0.3])
pMP_MA = Factor([MP,MA],[0.97,0.03,0.03,0.97])
pAP_AA = Factor([AP,AA],[0.5,0.2,0.5,0.8])

pMA_JAAA = Factor([MA,JA,AA],[0.5,0.15,0.05,0.95,0.5,0.85,0.95,0.05])
pVP_AABA = Factor([VP,AA,BA],[0.3,0.6,0.1,0,0.7,0.4,0.9,1])
pJP_JALF = Factor([JP,JA,LF],[0.6,1,0.1,0.3,0.4,0,0.9,0.7])
pBP_BAE = Factor([BP,BA,E],[0.8,1,0.05,1,0.2,0,0.95,0])

# Ejercicio 1a
tmp1 = pMP_MA.multiplicacion(pMA_JAAA).marginalizacion(MA)
tmp2 = tmp1.multiplicacion(pJP_JALF).multiplicacion(pJA_LI).marginalizacion(JA)
tmp3 = tmp2.multiplicacion(pAP_AA).multiplicacion(pAA_FIN).marginalizacion(AA)
tmp4 = tmp3.multiplicacion(pFIN).marginalizacion(FIN)
tmp5 = tmp4.multiplicacion(pLI).marginalizacion(LI)
tmp6 = tmp5.multiplicacion(pLF).marginalizacion(LF)
# tmp6._Factor__direccionamiento({MP:1,JP:1,AP:1})

# Ejercicio 2a
tmp1 = pMP_MA.multiplicacion(pMA_JAAA).marginalizacion(MA)
tmp2 = tmp1.multiplicacion(pJA_LI).marginalizacion(JA)
tmp3 = tmp2.multiplicacion(pAA_FIN).marginalizacion(AA)
tmp4 = tmp3.multiplicacion(pFIN).multiplicacion(pLI)

tmp5 = tmp4.marginalizacion(FIN)

# tmp4._Factor__direccionamiento({FIN:1,MP:1,LI:1})/tmp5._Factor__direccionamiento({MP:1,LI:1})

# Ejercicio 3a
tmp1 = pMP_MA.multiplicacion(pMA_JAAA).marginalizacion(MA)
tmp2 = tmp1.multiplicacion(pJA_LI).multiplicacion(pJP_JALF).marginalizacion(JA)
tmp3 = tmp2.multiplicacion(pLF).marginalizacion(LF)
tmp4 = tmp3.multiplicacion(pLI).marginalizacion(LI)
tmp5 = tmp4.multiplicacion(pAA_FIN).multiplicacion(pVP_AABA).multiplicacion(pAP_AA).marginalizacion(AA)
tmp6 = tmp5.multiplicacion(pBA_IT).multiplicacion(pBP_BAE).marginalizacion(BA)
tmp7 = tmp6.multiplicacion(pE).marginalizacion(E)
tmp8 = tmp7.multiplicacion(pIT).marginalizacion(IT)
# tmp8._Factor__direccionamiento({MP:1,AP:1,JP:1,BP:1,FIN:0,VP:1})

# Ejercicio 2
tmp1 = pBP_BAE.multiplicacion(pBA_IT).marginalizacion(BA)
tmp2 = tmp1.multiplicacion(pIT).marginalizacion(IT)
tmp3 = tmp2.multiplicacion(pE).marginalizacion(E)
tmp4 = pJP_JALF.multiplicacion(pLF).marginalizacion(LF)
tmp5 = tmp4.multiplicacion(pJA_LI).marginalizacion(JA)
tmp6 = tmp5.multiplicacion(pLI).marginalizacion(LI)
tmp7 = tmp3.multiplicacion(tmp6)
# tmp7._Factor__direccionamiento ({JP:1,BP:1})
#