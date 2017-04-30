import java.util.Random;

public class Poblacion {

	private class Individuo {

		// Random para números aleatorios
		private static final Random RAND = new Random ();
		// Representación del individuo
		private int[] representacion;

		/*
		 * Crea un individuo con una representación de tamaño TAM.
		 * TAM corresponde al tamaño del tablero de TAM x TAM.
		 */
		public Individuo (int tam) {
			this.representacion = new int[tam];
			for (int i = 0; i < tam; i++)
				this.representacion[i] = RAND.nextInt (tam);
		}

		/*
		 * Provoca una mutación en los genes del individuo con probabilidad P.
		 * Mueve a las reinas a posiciones aleatorias sobre su fila.
		 */
		public void mutacion (double p) {
			int m = representacion.length, i = 0;
			while (i < m)
				if (RAND.nextDouble <= p)
					representacion[i++] = RAND.nextInt (m);
		}

		/*
		 * Calcula la aptitud del individuo.
		 * Su aptitud es el número de parejas de reinas que se atacan entre sí.
		 */
		public int aptitud () {
			return 0;
		}

		/*
		 * Recombina dos individuos para generar uno nuevo.
		 */
		public static Individuo recombinacion (Individuo i1, Individuo i2) {
			int t = i1.representacion.length;
			int corte = RAND.nextInt (t);
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

	// Tamaño de población
	private static final int T_POBLACION = 50;
	// Factor de elitismo
	private static final int ELITISMO = 1;
	// Máximas iteraciones (generaciones)
	private static final int ITERACIONES = 1000;
	// Probabilidad de mutación
	private static final double MUTACION = 0.2;
	// Tamaño del tablero
	private static final int TABLERO = 8;

	// Cantidad de individuos
	private int m;
	// Mutación
	private double p;
	// Conjunto de individuos
	private ArrayList<Individuo> individuos;

	/**
	 * Crea una nueva población con la cantidad de individuos especificada.
	 * @param individuos La cantidad de individuos.
	 */
	public Poblacion (int individuos) {
		this.m = individuos;
		this.individuos = new ArrayList<>(individuos);
		for (int i = 0; i < individuos; i++) {
			this.individuos.add (new Individuo (TABLERO));
		}
	}

}
