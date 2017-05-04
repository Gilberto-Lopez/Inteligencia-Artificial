import java.util.Random;
import java.util.ArrayList;

/**
 * Clase Poblacion representa una población de individuos
 * para encontrar la solución al problema.
 */
public class Poblacion {

	/* Representa un individuo de la población. */
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
			int m = representacion.length;
			for (int i = 0; i < m; i++)
				if (Poblacion.RAND.nextDouble () <= p)
					representacion[i] = Poblacion.RAND.nextInt (m);
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
		 * El más apto es aquél en el que hay menor cantidad de reinas
		 * atacándose simultáneamente.
		 * Consideración: La última reina no puede atacar otras reinas a su
		 * derecha, la penúltima puede atacar a lo más una, la antepenúltima
		 * puede atacar a lo más dos, todas las demás pueden atacar a lo más
		 * tres reinas a su derecha. Hay virtualmente a lo más (N-2)*3 reinas
		 * atacándose simultáneamente en un tablero de N x N.
		 */
		public void asignaAptitud () {
			int m = representacion.length;
			int c = 0;
			for (int i = 0; i < m-1; i++) {
				int pos = representacion[i];
				boolean r = false;
				boolean du = false;
				boolean dd = false;
				for (int j = i+1; j < m; j++) {
					if (representacion[j] == pos && !r) {
						c++;
						r = true;
						continue;
					}
					int offset = (representacion[i] > representacion[j]) ? j-i : i-j;
					if (pos > 0 && !dd && representacion[j] == pos - offset) {
						c++;
						dd = true;
						continue;
					}
					if (pos < m && !du && representacion[j] == pos - offset) {
						c++;
						du = true;
						continue;
					}
				}
			}
			apt = (m-2)*3 - c;
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
			while (i <= corte)
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
	private static final int ITERACIONES = 1000;
	// Probabilidad de mutación
	private static final double MUTACION = 0.2;
	// Tamaño del tablero
	private static final int TABLERO = 8;

	// Cantidad de individuos para la población
	private int m;
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
		Individuo s = null;
		while (s == null) {
			for (Individuo i : individuos) {
				double pi = ((double) i.aptitud ()) / sumaApt;
				if (RAND.nextDouble () <= pi)
					s = i;
			}
		}
		return s;
	}

	/**
	 * Regresa el mejor individuo de la población.
	 * Las aptitudes deben haber sido calculadas previamente.
	 * @return El mejor individuo.
	 */
	public Individuo mejorIndividuo () {
		int mejor = 0, j = 0;
		for (int i = 0; i < m; i++) {
			Individuo t = individuos.get (i);
			int apt = t.aptitud ();
			if (apt > mejor) {
				mejor = apt;
				j = i;
			}
		}
		return individuos.get (j);
	}

	/**
	 * Decide si la población contiene un ejemplar cuya aptitud alcanza el
	 * valor óptimo proporcionado. Las aptitudes deben calcularse antes.
	 * @param valorOptimo El valor que se considera óptimo.
	 * @return true si la población contiene un ejemplar óptimo, false e.o.c.
	 */
	public boolean esOptimo (int valorOptimo) {
		for (Individuo i : individuos)
			if (i.aptitud () == valorOptimo)
				return true;
		return false;
	}

	/**
	 * Punto de entrada de la aplicación.
	 */
	public static void main(String[] args) {
		int fitOptimo = (TABLERO-2)*3; // Fitness óptimo.
		int i; // Iteración
		System.out.printf ("Aptitud óptima: %d\n", fitOptimo);

		Poblacion p = new Poblacion (T_POBLACION, TABLERO);
		p.asignarAptitud ();
		boolean optimo = p.esOptimo (fitOptimo);
		for (i = 1; i <= ITERACIONES && !optimo; i++) {
			Individuo M = p.mejorIndividuo ();
			if (i % 50 == 0)
				System.out.printf ("Generación %d:\tIndividuo: %s, Aptitud: %d\n", i, M, M.aptitud ());
			Poblacion nuevaP = new Poblacion (T_POBLACION);
			//for (Individuo s : p.elitismo (ELITISMO))
			//	nuevaP.agrega (s);
			nuevaP.agrega (M);
			while (nuevaP.getIndividuos () < T_POBLACION) {
				Individuo i1 = p.seleccion ();
				Individuo i2 = p.seleccion ();
				Individuo hijo = Individuo.recombinacion (i1, i2);
				hijo.mutacion (MUTACION);
				nuevaP.agrega (hijo);	
			}
			p = nuevaP;
			p.asignarAptitud ();
			optimo = p.esOptimo (fitOptimo);
		}
		System.out.printf ("\nSolución óptima : %s\n\tAptitud %d, encontrada en la generación %d\n\t\n",
			p.mejorIndividuo (), p.mejorIndividuo ().aptitud (), i-1);
	}

}
