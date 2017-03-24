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


if __name__ == '__main__':
    print("Crea aquí los objetos del problema y pide a la computadora que lo resuelva")

#    # Objetos y problema
#    r1 = Objeto ('r1', 'robot')
#    l1 = Objeto ('l1', 'location')
#    l2 = Objeto ('l2', 'location')
#    k1 = Objeto ('k1', 'crane')
#    k2 = Objeto ('k2', 'crane')
#    p1 = Objeto ('p1', 'pile')
#    p2 = Objeto ('p2', 'pile')
#    q1 = Objeto ('q1', 'pile')
#    q2 = Objeto ('q2', 'pile')
#    ca = Objeto ('ca', 'container')
#    cb = Objeto ('cb', 'container')
#    cc = Objeto ('cc', 'container')
#    cd = Objeto ('cd', 'container')
#    ce = Objeto ('ce', 'container')
#    cf = Objeto ('cf', 'container')
#    pallet = Objeto ('pallet', 'container')
#
#
#    dominio = Dominio ('dock-worker-robot',
#        ['robot', 'location', 'crane', 'pile', 'container'],
#        [],
#        [])



    # Ejemplo de cómo usar las clases
    p = Predicado('en-tripulación', [Variable('?m', 'marinero')])
    np = Predicado('en-tripulación', [Variable('?m', 'marinero')], True)
    dominio = Dominio('Barquito',
                      ['marinero'],
                      [p],
                      [Acción('desembarcar', [Variable('?m', 'marinero')], [p], [np])])
    print(dominio)

    popeye = Objeto('Popeye', 'marinero')
    pobj = Predicado('en-tripulación', [Variable('?m', 'marinero', popeye)])
    npobj = Predicado('en-tripulación', [Variable('?m', 'marinero', popeye)], True)
    problema = Problema('baja-de-barquito', dominio, [popeye], [pobj], [npobj])
    print(problema)