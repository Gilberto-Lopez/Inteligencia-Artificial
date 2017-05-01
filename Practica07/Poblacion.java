import java.util.Random;
import java.util.ArrayList;

public class Poblacion {

	private static class Individuo {

		// Representación del individuo
		private int[] representacion;
		// Aptitud del individuo;
		private int apt;

		// Constructor vacío privado
		private Individuo () {}

		/*
		 * Crea un individuo con una representación de tamaño TAM.
		 * TAM corresponde al tamaño del tablero de TAM x TAM.
		 */
		public Individuo (int tam) {
			this.representacion = new int[tam];
			for (int i = 0; i < tam; i++)
				this.representacion[i] = Poblacion.RAND.nextInt (tam);
		}

		/*
		 * Provoca una mutación en los genes del individuo con probabilidad P.
		 * Mueve a las reinas a posiciones aleatorias sobre su fila.
		 */
		public void mutacion (double p) {
			int m = representacion.length, i = 0;
			while (i < m)
				if (Poblacion.RAND.nextDouble () <= p)
					representacion[i++] = Poblacion.RAND.nextInt (m);
		}

		/*
		 * Regresa la aptitud del individuo.
		 * Su aptitud es el número de parejas de reinas que se atacan entre sí.
		 */
		public int aptitud () {
			return apt;
		}

		/*
		 * Calcula la aptitud del individuo.
		 */
		public void asignaAptitud () {
			int m = representacion.length;
			int c = 0;
			for (int i = 0; i < m-1; i++)
				for (int j = i+1; j < m; j++) {
					if (representacion[i] == representacion[j])
						c++;
					else {
						int offset = (representacion[i] > representacion[j]) ? j-i : i-j;
						if (representacion[i] - offset == representacion[j])
							c++;
					}
				}
			apt = (m*(m-1))/2 - c;
		}

		/*
		 * Regresa la representación en String del individuo.
		 */
		@Override
		public String toString () {
			String repr = "[";
			int i = 0;
			while (i < representacion.length -1)
				repr += (representacion[i++]+1) + " ";
			repr += (representacion[i]+1) + "]";
			return repr;
		}

		/*
		 * Recombina dos individuos para generar uno nuevo.
		 */
		public static Individuo recombinacion (Individuo i1, Individuo i2) {
			int t = i1.representacion.length;
			int corte = Poblacion.RAND.nextInt (t);
			Individuo nuevo = new Individuo ();
			nuevo.representacion = new int[t];
			int i = 0;
			while (i < corte)
				nuevo.representacion[i] = i1.representacion[i++];
			while (i < t)
				nuevo.representacion[i] = i2.representacion[i++];
			return nuevo;
		}

	}

	// Para números aleatorios
	private static final Random RAND = new Random ();
	// Tamaño de población
	private static final int T_POBLACION = 50;
	// Factor de elitismo
	//private static final int ELITISMO = 1;
	// Máximas iteraciones (generaciones)
	private static final int ITERACIONES = 10000;
	// Probabilidad de mutación
	private static final double MUTACION = 0.2;
	// Tamaño del tablero
	private static final int TABLERO = 8;

	// Cantidad de individuos para la población
	private int m;
	// Mutación
	private double p;
	// Conjunto de individuos
	private ArrayList<Individuo> individuos;
	// Suma de las aptitudes
	private int sumaApt;

	/**
	 * Crea una nueva población vacía con un tamaño máximo dado por la cantidad
	 * de individuos dada.
	 * @param individuos La cantidad de individuos.
	 */
	public Poblacion (int individuos) {
		this.m = individuos;
		this.individuos = new ArrayList<> (individuos);
	}

	/**
	 * Crea una nueva población con la cantidad de individuos especificada.
	 * @param individuos La cantidad de individuos.
	 * @param representación El tamaño de la representación de los individuos.
	 */
	public Poblacion (int individuos, int representacion) {
		this (individuos);
		while (individuos-- > 0)
			this.individuos.add (new Individuo (representacion));
	}

	/**
	 * Regresa la cantidad de individuos en la población.
	 */
	public int getIndividuos () {
		return this.individuos.size ();
	}

	/**
	 * Agrega un nuevo individuo a la población de ser posible.
	 * @param i El individuo.
	 */
	public void agrega (Individuo i) {
		if (individuos.size () < m)
			individuos.add (i);
	}

	/* //JavaDoc
	 * Regresa los n mejores ejemplares de la población. n debe ser menor o
	 * o igual al tamaño de la población. Las aptitudes deben ser asignadas
	 * previamente.
	 * @return Los n mejores ejemplares. NULL si n es mayor al tamaño de la
	 *         población o menor a 1.
	 */
	/*
	public ArrayList<Individuo> elitismo (int n) {
		if (n > m || n < 1)
			return null;
		ArrayList<Individuo> l = new ArrayList<> (n);
		int max = Integer.MAX_VALUE;
		while (n-- > 0) {
			int mayor = 0;
			int j = 0;
			for (int i = 0; i < m; i++) {
				Individuo t = individuos.get (i);
				int apt = t.aptitud ();
				if (apt <= max && apt >= mayor && !l.contains (t)) {
					mayor = apt;
					j = i;
				}
			}
			max = mayor;
			l.add (individuos.get (j));
		}
		return l;
	}
	*/

	/**
	 * Calcula la aptitud de cada individuo.
	 */
	public void asignarAptitud () {
		for (Individuo i : individuos) {
			i.asignaAptitud ();
			sumaApt += i.aptitud ();
		}
	}

	/**
	 * Selecciona aleatoriamente un individuo de la población mediante la
	 * selección de ruleta. Se asume que las aptitudes de los individuos ya
	 * fueron asignadas.
	 * @param El individuo.
	 */
	public Individuo seleccion () {
		while (true) {
			int i = RAND.nextInt (m);
			Individuo t = individuos.get (i);
			double pi = ((double) t.aptitud ()) / sumaApt;
			if (RAND.nextDouble () <= pi)
				return t;
		}
	}

	/**
	 * Regresa el mejor individuo de la población.
	 * @return El mejor individuo.
	 */
	public Individuo mejorIndividuo () {
		int mayor = 0, j = 0;
		for (int i = 0; i < m; i++) {
			Individuo t = individuos.get (i);
			int apt = t.aptitud ();
			if (apt > mayor) {
				mayor = apt;
				j = i;
			}
		}
		return individuos.get (j);
	}

	/**
	 * Punto de entrada de la aplicación.
	 */
	public static void main(String[] args) {
		Poblacion p = new Poblacion (T_POBLACION, TABLERO);
		p.asignarAptitud ();
		for (int i = 1; i <= ITERACIONES; i++) {
			if (i % 50 == 0)
				System.out.printf ("Generación %d: %s\n", i, p.mejorIndividuo ());
			Poblacion nuevaP = new Poblacion (T_POBLACION);
			//for (Individuo s : p.elitismo (ELITISMO))
			//	nuevaP.agrega (s);
			nuevaP.agrega (p.mejorIndividuo ());
			while (nuevaP.getIndividuos () < T_POBLACION) {
				Individuo i1 = p.seleccion ();
				Individuo i2 = p.seleccion ();
				Individuo hijo = Individuo.recombinacion (i1, i2);
				hijo.mutacion (MUTACION);
				nuevaP.agrega (hijo);	
			}
			p = nuevaP;
			p.asignarAptitud ();
		}
		System.out.println ("Mejor individuo:\n\t" + p.mejorIndividuo ());
	}

}
