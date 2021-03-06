from itertools import product

# ------ Dominio -----

class Dominio:
    """ Clase para definir el dominio, o espacio de estados en el cual se plantearán problemas de planeación. """
    def __init__(self, nombre, tipos, predicados, acciones):
        """
        Inicializa un dominio
        :param nombre:
        :param tipos:
        :param predicados:
        :param acciones:
        """
        self.nombre = nombre
        self.tipos = tipos
        self.predicados = predicados
        self.acciones = acciones

    def __str__(self):
        dic = {'name':          self.nombre,
               'types':         "  \n".join(self.tipos),
               'predicates':    "  \n".join(str(p) for p in self.predicados),
               'actions':       "\n".join(str(a) for a in self.acciones)
               }
        return """(define (domain {name})
          (:requirements :strips :typing)
          (:types
            {types})
          (:predicates
            {predicates})
          )
          {actions})
        """.format(**dic)

    def __repr__(self):
        return self.__str__()

class Variable:
    """ Variable tipada. """
    def __init__(self, nombre, tipo, valor=None):
        """
        :param nombre: símbolo nombre de esta variable.  Los nombres de variables inician con ?
        :param tipo: tipo de la variable, debe estar registrado en la descripción del dominio
        :param valor: objeto vinculado a esta variable, si es None la variable está libre
        """
        self. nombre = nombre
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        if self.valor:
            return self.valor.nombre
        return "{} - {}".format(self.nombre, self.tipo)

    def __repr__(self):
        return self.__str__()

    def copia (self):
        """
        Crea una copia de la variable self.
        """
        # nombre, tipo y valor están fijos.
        return Variable(self.nombre, self.tipo, self.valor)

class Predicado:
    """ Representa un hecho. """
    def __init__(self, nombre, variables, negativo = False):
        """
        Predicados para representar hechos.
        :param nombre:
        :param variables: lista de variables tipadas
        :param negativo: indica un predicado del tipo "no P", utilizable para especificar efectos o metas.
        """
        self.nombre = nombre
        self.variables = variables
        self.negativo = negativo

    def __str__(self):
        pred = "({0} {1})".format(self.nombre, " ".join(str(v) for v in self.variables))
        if self.negativo:
            return "(not {0})".format(pred)
        return pred

    def __repr__(self):
        return self.__str__()

    def copia (self):
        """
        Crea una copia del predicado self.
        """
        # nombre y negativo están fijos
        # Las variables se deben copiar.
        return Predicado (self.nombre,
            [x.copia () for x in self.variables],
            self.negativo)

class Acción:
    """ Función de transición con su acción correspondiente. """
    def __init__(self, nombre, parámetros, precondiciones, efectos, vars=None):
        """
        Inicializa definición de la función de transición para esta acción.
        :param nombre: nombre de la acción
        :param parámetros: lista de variables tipadas
        :param precondiciones: lista de predicados con variables libres
        :param efectos: lista de predicados con variables libres
        :param vars: lista de variables libres que pueden tomar su valor de cualquier objeto del domino simpre que
               sus valores satisfagan las restriciones de las precondiciones.
        """
        self.nombre = nombre
        self.parámetros = parámetros
        self.precondiciones = precondiciones
        self.efectos = efectos
        self.vars = vars

    def __str__(self):
        dic = {'name':      self.nombre,
               'params':    " ".join(str(p) for p in self.parámetros),   # Podrían reunirse 1o los de tipos iguales
               'prec':      " ".join(str(p) for p in self.precondiciones),
               'efec':      " ".join(str(p) for p in self.efectos)
               }
        if self.vars:
            dic['vars'] = "\n    :vars {}".format(" ".join(str(v) for v in self.vars))
        else:
            dic['vars'] = ""
        return """(:action {name}
            :parameters   ({params}) {vars}
            :precondition (and {prec})
            :effect       (and {efec})
        )
        """.format(**dic)

    def __repr__(self):
        return self.__str__()

# ------ Problema -----

class Objeto:
    """ Valor concreto para variables en el dominio. """
    def __init__(self, nombre, tipo):
        """
        Crea un objeto existente en el dominio para este problema.
        :param nombre: Símbolo del objeto
        :param tipo: tipo del objeto
        """
        self.nombre = nombre
        self.tipo = tipo

    def __str__(self):
        return "{} - {}".format(self.nombre, self.tipo)

    def __repr__(self):
        return self.__str__()

class Problema:
    """ Definicion de un problema en un dominio particular. """
    def __init__(self, nombre, dominio, objetos, predicados, predicados_meta):
        """
        Problema de planeación en una instancia del dominio.
        :param nombre: nombre del problema
        :param dominio: referencia al objeto con la descripción genérica del dominio
        :param objetos: lista de objetos existentes en el dominio, con sus tipos
        :param predicados: lista de predicados con sus variables aterrizadas, indicando qué cosas son verdaderas en el
               estado inicial.  Todo aquello que no esté listado es falso.
        :param predicados_meta: lista de predicados con sus variables aterrizadas, indicando aquellas cosas que deben
               ser verdaderas al final.  Para indicar que algo debe ser falso, el predicado debe ser negativo.
        """
        self.nombre = nombre
        self.dominio = dominio # ref a objeto Dominio
        self.objetos = objetos
        self.estado = predicados
        self.meta = predicados_meta

    def __str__(self):
        dic = {'name':          self.nombre,
               'domain_name':   self.dominio.nombre,
               'objects':       "\n".join(str(o) for o in self.objetos),
               'init':          "\n".join(str(p) for p in self.estado),
               'goal':          "\n".join(str(p) for p in self.meta)}
        return """(define (problem {name}
          (:domain {domain_name})
          (:objects
            {objects})
          (:init
            {init})
          (:goal
            (and {goal}))
        )
        """.format(**dic)

    def __repr__(self):
        return self.__str__()

    def es_aplicable (self, accion):
        """
        Determina si la acción dada, que debe estar en el dominio, es aplicable
        en el estado actual del problema, y de ser posible, con qué sustitución.
        Regresa una tupla (B,L) donde B es un booleano (si la acción es
        aplicable B es True, False en otro caso) y L es la lista de variables
        con sus valores resultantes de la sustitución o [].
        :param accion: la acción que se desea aplicar.
        """
        vars = []
        vars.extend (accion.parámetros + (accion.vars if accion.vars != None else [])) 
        asignaciones = self._asignaciones (vars)
        if asignaciones == []:
            # Alguna variable no se pudo unificar
            return (False, asignaciones)
        flag = False;
        sust = []
        for sigma in asignaciones:
            for (x, o) in sigma:
                x.valor = o
            # Las precondiciones de la acción están aterrizadas
            if self._estado_satisface (accion.precondiciones):
                flag = True
                sust = sigma
                break
        for x in vars: x.valor = None
        return (flag, sust)

    def _aplicable (self, accion):
        vars = []
        vars.extend (accion.parámetros + (accion.vars if accion.vars != None else [])) 
        asignaciones = self._asignaciones (vars)
        if asignaciones == []:
            # Alguna variable no se pudo unificar
            return (False, asignaciones)
        flag = False;
        sust = []
        for sigma in asignaciones:
            for (x, o) in sigma:
                x.valor = o
            # Las precondiciones de la acción están aterrizadas
            if self._estado_satisface (accion.precondiciones):
                flag = True
                sust.append (sigma)
        for x in vars: x.valor = None
        return (flag, sust)        

    def aplica_accion (self, accion, sustitucion):
        """
        Aplica la acción con la sustitución dada sobr el problema actual.
        La acción debe ser aplicable con la sustitución dada. Regresa un
        nuevo problema con la sustitución aplicada.
        :param accion: la acción que se desea aplicar.
        :param sustitucion: la sustitución que permite aplicar la acción.
        """
        sucesor = self.copia ()
        for p in map (lambda x: x.copia (), accion.efectos):
            for v in p.variables:
                for (x, o) in sustitucion:
                    if v.tipo == x.tipo and v.nombre == x.nombre:
                        v.valor = o
                        break
            # Eliminamos la literal contraria del estado si
            # esta existe.
            sucesor._elimina_contrario (p)
            sucesor.estado.append (p)
        return sucesor

    def es_meta (self):
        """
        Determina si el estado actual del problema satisface las condiciones del
        campo meta.
        """
        return self._estado_satisface (self.meta)

    def _asignaciones (self, variables):
        # Regresa todas las posibles asignaciones de las variables en la lista
        # de entrada en el estado actual.
        asignaciones = []
        for var in variables:
            a_var = [(var, x) for x in self.objetos if x.tipo == var.tipo]
            if a_var == []:
                # No se pudo unificar var
                return []
            asignaciones.append(a_var)
        return map (list, product (*asignaciones))

    def _estado_satisface (self, condiciones):
        # Determina si el estado actual del problema satisface las condiciones
        # dadas (lista de predicados aterrizados).
        for pred in condiciones:
            r = False
            for s in self.estado:
                if (pred.nombre == s.nombre and
                    pred.negativo == s.negativo and
                    self._variables_iguales (pred.variables, s.variables)):
                    # pred está en el estado.
                    r = True
                    break
            if not r:
                # pred no está en el estado.
                return r
        return True

    def _elimina_contrario (self, predicado):
        # Elimina la negación del predicado del estado si esta. No hace nada
        # si la negación no está en el estado.
        for p in self.estado:
            if (p.nombre == predicado.nombre and
                p.negativo != predicado.negativo and
                self._variables_iguales (p.variables, predicado.variables)):
                self.estado.remove (p)

    def _variables_iguales (self, l1, l2):
        # Determina si dos listas de variables son iguales, las variables
        # aparecen en el mismo orden, tienen el mismo tipo, nombre y valor.
        if len (l1) != len (l2):
            return False
        for i in range(len(l1)):
            if (l1[i].tipo != l2[i].tipo or
                l1[i].valor != l2[i].valor):
                return False
        return True

    def copia (self):
        """
        Crea una copia del problema self.
        """
        # nombre, objetos, dominio y meta están fijos.
        # El estado se copia.
        return Problema (self.nombre,
            self.dominio,
            self.objetos,
            [x.copia () for x in self.estado],
            self.meta)

class Solucion:
    """
    Clase para realizar una búsqueda en amplitud de la
    solución del problema.
    """

    class _Nodo:
        # Clase para nodos de búsqueda.

        def __init__ (self, problema, padre = None, accion = None, sustitucion = None):
            # Inicializa un nodo de búsqueda con el problema dado.
            # Dada la acción y sustitución, si se aplica a padre.problema
            # se llega al problema del nodo actual.
            self.problema = problema
            self.padre = padre
            self.accion = accion
            self.sustitucion = sustitucion

        def sucesores (self):
            # Obtiene los sucesores del problema
            if self.problema.es_meta (): return []
            dank = []
            for a in self.problema.dominio.acciones:
                (b, sust) = self.problema._aplicable (a)
                if b:
                    for s in sust:
                        dank.append (
                            Solucion._Nodo (self.problema.aplica_accion (a, s),
                            self,
                            a,
                            s))
            return dank

    def __init__ (self, problema):
        """
        Crea un objeto solución con una pila de tuplas (Pr,Pa,A,S)
        donde Pr es el problema (con un cierto estado) y Pa es el
        padre, A la acción y S la sustitución tal que al aplicarla
        a Pa se llega a Pr.
        :param problema: el problema.
        """
        self.listaAbierta = [Solucion._Nodo (problema)]

    def expande (self, imprime = False):
        """
        Expande el espacio de estados y regresa una lista de nodos
        de búsqueda tal que el estado del problema que guardan
        satisface las metas.
        """
        metas = []
        while self.listaAbierta != []:
            n_actual = self.listaAbierta.pop (0)
            sucesores = n_actual.sucesores ()
            self.listaAbierta.extend (sucesores)
            for s in sucesores:
                print(s.accion.nombre)
                if s.problema.es_meta ():
                    metas.append (s)
            if imprime:
                print (self.listaAbierta)
                print (metas, "\n")
        return metas

if __name__ == '__main__':
    print("Crea aquí los objetos del problema y pide a la computadora que lo resuelva")

    # 1. Objetos y problema

    # Objetos
    r1 = Objeto ('r1', 'robot')
    l1 = Objeto ('l1', 'location')
    l2 = Objeto ('l2', 'location')
    k1 = Objeto ('k1', 'crane')
    k2 = Objeto ('k2', 'crane')
    p1 = Objeto ('p1', 'pile')
    p2 = Objeto ('p2', 'pile')
    q1 = Objeto ('q1', 'pile')
    q2 = Objeto ('q2', 'pile')
    ca = Objeto ('ca', 'container')
    cb = Objeto ('cb', 'container')
    cc = Objeto ('cc', 'container')
    cd = Objeto ('cd', 'container')
    ce = Objeto ('ce', 'container')
    cf = Objeto ('cf', 'container')
    pallet = Objeto ('pallet', 'container')

    # Predicados
    adjacent = Predicado ('adjacent',
        [Variable ('?l1', 'location'), Variable ('?l2', 'location')])
    attached = Predicado ('attached',
        [Variable ('?p', 'pile'), Variable ('?l', 'location')])
    belong = Predicado ('belong',
        [Variable ('?k', 'crane'), Variable ('?l', 'location')])
    at = Predicado ('at',
        [Variable ('?r', 'robot'), Variable ('?l', 'location')])
    occupied = Predicado ('occupied',
        [Variable ('?l', 'location')])
    loaded = Predicado ('loaded',
        [Variable ('?r', 'robot'), Variable ('?c', 'container')])
    unloaded = Predicado ('unloaded',
        [Variable ('?r', 'robot')])
    holding = Predicado ('holding',
        [Variable ('?k', 'crane'), Variable ('?l', 'location')])
    empty = Predicado ('empty',
        [Variable ('?k', 'crane')])
    in_ = Predicado ('in',
        [Variable ('?c', 'container'), Variable ('?p', 'pile')])
    top = Predicado ('top',
        [Variable ('?c', 'container'), Variable ('?p', 'pile')])
    on = Predicado ('on',
        [Variable ('?k1', 'container'), Variable ('?k2', 'container')])
    # Negaciones
    noccupied = Predicado ('occupied',
        [Variable ('?l', 'location')], True)
    nat = Predicado ('at',
        [Variable ('?r', 'robot'), Variable ('?l', 'location')], True)
    nunloaded = Predicado ('unloaded',
        [Variable ('?r', 'robot')], True)
    nholding = Predicado ('holding',
        [Variable ('?k', 'crane'), Variable ('?l', 'location')], True)
    nloaded = Predicado ('loaded',
        [Variable ('?r', 'robot'), Variable ('?c', 'container')], True)
    nempty = Predicado ('empty',
        [Variable ('?k', 'crane')], True)
    nin = Predicado ('in',
        [Variable ('?c', 'container'), Variable ('?p', 'pile')], True)
    ntop = Predicado ('top',
        [Variable ('?c', 'container'), Variable ('?p', 'pile')], True)
    non = Predicado ('on',
        [Variable ('?k1', 'container'), Variable ('?k2', 'container')], True)

    # Acciones
    r_m = Variable ('?r', 'robot')
    from_m = Variable ('?from', 'location')
    to_m = Variable ('?to', 'location')
    move = Acción ('move',
        [r_m, from_m, to_m],
        [
        Predicado ('adjacent', [from_m, to_m]),
        Predicado ('at', [r_m, from_m]),
        Predicado ('occupied', [to_m], True)
        ],
        [
        Predicado ('at', [r_m, to_m]),
        Predicado ('occupied', [from_m], True),
        Predicado ('occupied', [to_m]),
        Predicado ('at', [r_m, from_m], True)
        ])
    k_l = Variable ('?k', 'crane')
    c_l = Variable ('?c', 'container')
    r_l = Variable ('?r', 'robot')
    l_l = Variable ('?l', 'location')
    load = Acción ('load',
        [k_l, c_l, r_l],
        [
        Predicado ('at', [r_l, l_l]),
        Predicado ('belong', [k_l, l_l]),
        Predicado ('holding', [k_l, c_l]),
        Predicado ('unloaded', [r_l])
        ],
        [
        Predicado ('loaded', [r_l,c_l]),
        Predicado ('unloaded', [r_l], True),
        Predicado ('empty', [k_l]),
        Predicado ('holding', [k_l, c_l], True)
        ],
        [l_l])
    k_u = Variable ('?k', 'crane')
    c_u = Variable ('?c', 'container')
    r_u = Variable ('?r', 'robot')
    l_u = Variable ('?l', 'location')
    unload = Acción ('unload',
        [k_u, c_u, r_u],
        [
        Predicado ('belong', [k_u, l_u]),
        Predicado ('at', [r_u, l_u]),
        Predicado ('loaded', [r_u, c_u]),
        Predicado ('empty', [k_u])
        ],
        [
        Predicado ('unloaded', [r_u]),
        Predicado ('holding', [k_u, c_u]),
        Predicado ('loaded', [r_u, c_u], True),
        Predicado ('empty', [k_u], True)
        ],
        [l_u])
    k_t = Variable ('?k', 'crane')
    c_t = Variable ('?c', 'container')
    p_t = Variable ('?p', 'pile')
    l_t = Variable ('?l', 'location')
    else_t = Variable ('?else', 'container')
    take = Acción ('take',
        [k_t, c_t, p_t],
        [
        Predicado ('belong', [k_t, l_t]),
        Predicado ('attached', [p_t, l_t]),
        Predicado ('empty', [k_t]),
        Predicado ('in', [c_t, p_t]),
        Predicado ('top', [c_t, p_t]),
        Predicado ('on', [c_t, else_t])
        ],
        [
        Predicado ('holding', [k_t, c_t]),
        Predicado ('top', [else_t, p_t]),
        Predicado ('in', [c_t, p_t], True),
        Predicado ('top', [c_t, p_t], True),
        Predicado ('on', [c_t, else_t], True),
        Predicado ('empty', [k_t], True)
        ],
        [l_t, else_t])
    k_p = Variable ('?k', 'crane')
    c_p = Variable ('?c', 'container')
    p_p = Variable ('?p', 'pile')
    else_p = Variable ('?else', 'container')
    l_p = Variable ('?l', 'location')
    put = Acción ('put',
        [k_p, c_p, p_p],
        [
        Predicado ('belong', [k_p, l_p]),
        Predicado ('attached', [p_p, l_p]),
        Predicado ('holding', [k_p, c_p]),
        Predicado ('top', [else_p, p_p])
        ],
        [
        Predicado ('in', [c_p, p_p]),
        Predicado ('top', [c_p, p_p]),
        Predicado ('on', [c_p, else_p]),
        Predicado ('top', [else_p, p_p], True),
        Predicado ('holding', [k_p, c_p], True),
        Predicado ('empty', [k_p]),
        ],
        [else_p, l_p])

    # Dominio
    dwr = Dominio ('dock-worker-robot',
        ['robot', 'location', 'crane', 'pile', 'container'],
        [adjacent, attached, belong, at, occupied, loaded, unloaded, holding, empty, in_, top, on],
        [move, load, unload, take, put])

    print (dwr)

    # Problema
    dwrpb1 = Problema ('dwrpb1', dwr,
        [r1, l1, l2, k1, k2, p1, p2, q1, q2, ca, cb, cc, cd, ce, cf, pallet],
        [ # Predicados del problema
        Predicado ('adjacent', [Variable ('?l1', 'location', l1), Variable ('?l2', 'location', l2)]),
        Predicado ('adjacent', [Variable ('?l1', 'location', l2), Variable ('?l2', 'location', l1)]),
        Predicado ('attached', [Variable ('?p', 'pile', p1), Variable ('?l', 'location', l1)]),
        Predicado ('attached', [Variable ('?p', 'pile', q1), Variable ('?l', 'location', l1)]),
        Predicado ('attached', [Variable ('?p', 'pile', p2), Variable ('?l', 'location', l2)]),
        Predicado ('attached', [Variable ('?p', 'pile', q2), Variable ('?l', 'location', l2)]),
        Predicado ('belong', [Variable ('?k', 'crane', k1), Variable ('?l', 'location', l1)]),
        Predicado ('belong', [Variable ('?k', 'crane', k2), Variable ('?l', 'location', l2)]),
        Predicado ('in', [Variable ('?c', 'container', ca), Variable ('?p', 'pile', p1)]),
        Predicado ('in', [Variable ('?c', 'container', cb), Variable ('?p', 'pile', p1)]),
        Predicado ('in', [Variable ('?c', 'container', cc), Variable ('?p', 'pile', p1)]),
        Predicado ('in', [Variable ('?c', 'container', cd), Variable ('?p', 'pile', q1)]),
        Predicado ('in', [Variable ('?c', 'container', ce), Variable ('?p', 'pile', q1)]),
        Predicado ('in', [Variable ('?c', 'container', cf), Variable ('?p', 'pile', q1)]),
        Predicado ('on', [Variable ('?k1', 'container', ca), Variable ('?k2', 'container', pallet)]),
        Predicado ('on', [Variable ('?k1', 'container', cb), Variable ('?k2', 'container', ca)]),
        Predicado ('on', [Variable ('?k1', 'container', cc), Variable ('?k2', 'container', cb)]),
        Predicado ('on', [Variable ('?k1', 'container', cd), Variable ('?k2', 'container', pallet)]),
        Predicado ('on', [Variable ('?k1', 'container', ce), Variable ('?k2', 'container', cd)]),
        Predicado ('on', [Variable ('?k1', 'container', cf), Variable ('?k2', 'container', ce)]),
        Predicado ('top', [Variable ('?c', 'container', cc), Variable ('?p', 'pile', p1)]),
        Predicado ('top', [Variable ('?c', 'container', cf), Variable ('?p', 'pile', q1)]),
        Predicado ('top', [Variable ('?c', 'container', pallet), Variable ('?p', 'pile', p2)]),
        Predicado ('top', [Variable ('?c', 'container', pallet), Variable ('?p', 'pile', q2)]),
        Predicado ('at', [Variable ('?r', 'robot', r1), Variable ('?l', 'location', l1)]),
        Predicado ('unloaded', [Variable ('?r', 'robot', r1)]),
        Predicado ('occupied', [Variable ('?l', 'location', l1)]),
        Predicado ('empty', [Variable ('?k', 'crane', k1)]),
        Predicado ('empty', [Variable ('?k', 'crane', k2)])
        ],
        [ # Predicados meta del problema
        Predicado ('in', [Variable ('?c', 'container', ca), Variable ('?p', 'pile', p2)]),
        Predicado ('in', [Variable ('?c', 'container', cb), Variable ('?p', 'pile', q2)]),
        Predicado ('in', [Variable ('?c', 'container', cc), Variable ('?p', 'pile', p2)]),
        Predicado ('in', [Variable ('?c', 'container', cd), Variable ('?p', 'pile', q2)]),
        Predicado ('in', [Variable ('?c', 'container', ce), Variable ('?p', 'pile', q2)]),
        Predicado ('in', [Variable ('?c', 'container', cf), Variable ('?p', 'pile', q2)]),
        ])

    print (dwrpb1)
    
#    sol = Solucion (dwrpb1)
#    sol.expande ()
