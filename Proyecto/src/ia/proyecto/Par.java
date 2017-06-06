package ia.proyecto;

import java.util.Objects;

/**
 * Representa un par ordenado de tipo A x B.
 */
public class Par <A, B> {

	// Primera entrada.
	private A a;
	// Segunda entrada.
	private B b;

	/**
	 * Construye un nuevo para (a,b).
	 * @param a La primera entrada.
	 * @param b La segunda entrada.
	 */
	public Par (A a, B b) {
		this.a = a;
		this.b = b;
	}

	/**
	 * Proyección sobre la primera entrada.
	 * @return La primera entrada.
	 */
	public A p1 () {
		return this.a;
	}

	/**
	 * Proyección sobre la segunda entrada.
	 * @return La segunda entrada.
	 */
	public B p2 () {
		return this.b;
	}

	/**
	 * Actualiza la primera entrada.
	 * @param a La primera entrada.
	 */
	public void setP1 (A a) {
		this.a = a;
	}

	/**
	 * Actualiza la segunda entrada.
	 * @param b La segunda entrada.
	 */
	public void setPb (B b) {
		this.b = b;
	}

	/**
	 * Determina si dos pares son iguales. Dos pares son iguales si son iguales
	 * entrada a entrada.
	 * @param o El par a comparar.
	 * @return true si los pares coinciden entrada a entrada, false e.o.c.
	 */
	@Override
	public boolean equals (Object o) {
		if (!(o instanceof Par))
			return false;
		Par<?, ?> p = (Par<?, ?>) o;
		return Objects.equals (this.a, p.a) && Objects.equals (this.b, p.b);
	}

	/** Representación de un par: '(a,b)'. */
	@Override
	public String toString () {
		return "(" + this.a.toString () + ", " + this.b.toString () + ")";
	}

}
