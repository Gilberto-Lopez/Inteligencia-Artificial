package ia;

import processing.core.PApplet;
import processing.core.PFont;
import java.util.*; //Stack,  Random
import java.lang.Math;

/**
 * Clase Laberintos.
 * Práctica 3. Backtracking.
 * @author Gilberto López.
 */
public class Laberintos extends PApplet {

    PFont fuente;  // Fuente para mostrar texto en pantalla
    
    // Propiedades del modelo de laberinto.
    int alto = 15;         // Altura  (en celdas) de la cuadricula.
    int ancho = 15;        // Anchura  (en celdas) de la cuadricula.
    int celda = 40;          // Tamanio de cada celda cuadrada  (en pixeles).
    ModeloLaberinto modelo;  // El objeto que representa el modelo de termitas.

    @Override
    public void setup () {
        frameRate (20);
        size (ancho*celda,  alto*celda);
        background (50);
        fuente = createFont ("Arial", 12, true);
        modelo = new ModeloLaberinto (ancho, alto, celda);
    }
    
    /**
     * Pintar el mundo del modelo  (la cuadricula).
     */
    @Override
    public void draw () {
        background (50);
	fill (255,  0,  0);
	rect (modelo.t.posX*modelo.tam,  modelo.t.posY*modelo.tam,  modelo.tam,  modelo.tam); 
        for (int i = 0; i < alto; i++)
	    for (int j = 0; j < ancho; j++){
		if (modelo.mundo[i][j].pa)
		    line (j*modelo.tam, i*modelo.tam,  (j+1)*modelo.tam, i*modelo.tam);
		if (modelo.mundo[i][j].pd)
		    line ( (j+1)*modelo.tam, i*modelo.tam,  (j+1)*modelo.tam,  (i+1)*modelo.tam);
		if (modelo.mundo[i][j].pab)
		    line (j*modelo.tam,  (i+1)*modelo.tam,  (j+1)*modelo.tam,  (i+1)*modelo.tam);
		if (modelo.mundo[i][j].pi)
		    line (j*modelo.tam, i*modelo.tam, j*modelo.tam,  (i+1)*modelo.tam);              
	    }
        modelo.backTrack ();
    }

    /**
     * Clase Celda.
     * Representación de cada celda de la cuadrícula.
     * Las celdas saben su posición en el grid del mundo.
     * Tienen flags para saber cuáles de sus paredes se
     * deben dibujar y si están disponibles (no visitadas).
     */
    class Celda{
	int celdaX,  celdaY;
	boolean estado;
	//Paredes de la celda:
	//pa arriba,  pab abajo,  pi izquierda,  pd derecha
	boolean pa, pab, pi, pd;

	/**
	 * Constructor de una celda. Por default
	 * todas sus paredes se dibujan.
	 * @param celdaX Coordenada en x
	 * @param celdaY Coordenada en y
	 * @param estado True para casilla disponible, i.e., no ha sido visitada.
	*/
	Celda (int celdaX,  int celdaY,  boolean estado){
	    this.celdaX = celdaX;
	    this.celdaY = celdaY;
	    this.estado = estado;
	    this.pa = true;
	    this.pab = true;
	    this.pi = true;
	    this.pd = true;
	}
    }

    /**
     * Clase Laberinto.
     * Representa un laberinto.
     * Los laberintos tienen coordenadas (X,Y)
     * que nos dicen la posición actual durante la 
     * simulación.
     */
    class Laberinto{
	int posX,  posY;  // Coordenadas de la posicion del cuadrito actual en el laberinto.

	Laberinto (int posX,  int posY){
	    this.posX = posX;
	    this.posY = posY;
	}
    }
    
    /**
     * Entre las celdas del laberinto sólo nos podemos mover en cuatro
     * posiciones,  hacia arriba  (0),  hacia abajo  (1), 
     * hacia la izquierda  (2) y hacia la derecha  (3).
     */
    class ModeloLaberinto{
	int ancho,  alto;  // Tamaño de celdas a lo largo y ancho de la cuadrícula.
	int tam;  // Tamaño en pixeles de cada celda.
	Celda[][] mundo;  // Mundo de celdas donde habitan las astillas.
	Stack<Celda> p; //Stack de celdas para el back tracking.
	Laberinto t;
	Random rnd = new Random ();  // Auxiliar para decisiones aleatorias.

	/**
	 * Constructor del modelo
	 * @param ancho Cantidad de celdas a lo ancho en la cuadricula.
	 * @param ancho Cantidad de celdas a lo largo en la cuadricula.
	 * @param tam Tamaño de cada celda que compone la cuadricula.
	 */ 
	ModeloLaberinto (int ancho,  int alto,  int tam){
	    //Inicializamos las dimensiones.
	    this.ancho = ancho;
	    this.alto = alto;
	    this.tam = tam;
	    //Creamos el grid
	    mundo = new Celda[alto][ancho];
	    //Agregamos las celdas
	    for (int i = 0; i < alto; i++)
		for (int j = 0; j < ancho; j++)
		    mundo[i][j] = new Celda (j, i, true);
	    //Posición inicial aleatoria.
	    int rx = rnd.nextInt (ancho);
	    int ry = rnd.nextInt (alto);
	    t = new Laberinto (ry, rx);
	    mundo[ry][rx].estado = false;
	    p = new Stack<Celda> ();
            p.push (mundo[ry][rx]);
	}

	/**
	 * Mueve a la celda señalada la direccion dada.
	 * No se considera el tablero como un toro.
	 * Se asume que es posible moverse a la casilla en la dirección dada.
	 * @param t El laberinto sobre el cual nos desplazamos.
	 * @param direccion La direccion en la que se desea en el laberinto.
	 */
	void moverLaberinto (Laberinto t,  int direccion){
	    //Guardamos la celda actual
            p.push (mundo[t.posY][t.posX]);
	    switch (direccion) {
		//movimiento hacia arriba
	    case 0:  t.posY--;
		break;
		//movimiento hacia abajo
	    case 1:  t.posY++;
		break;
		//movimiento hacia la izquierda
	    case 2:  t.posX--;
		break;
		//movimiento hacia la derecha
	    case 3:  t.posX++;
	    }
	    //La nueva celda ya es visitada (no disponible)
	    mundo[t.posY][t.posX].estado = false;
	}
      
	/**
	 * Nos dice si la celda vecina a la posición actual
	 * indicada por la dirección dada está disponible.
	 * @param t El laberinto.
	 * @param dir La dirección en la que queremos ver si nos podemos mover.
	 */
        boolean vecinoDisponible (Laberinto t,  int dir){
	    //Cuidamos los límites del grid.
	    switch (dir){
	    case 0: if (t.posY-1 < 0) return false;
		return mundo[t.posY-1][t.posX].estado;
	    case 1: if (t.posY+1 >= alto) return false;
		return mundo[t.posY+1][t.posX].estado;
	    case 2: if (t.posX-1 < 0) return false;
		return mundo[t.posY][t.posX-1].estado;
	    case 3: if (t.posX+1 >= ancho) return false;
		return mundo[t.posY][t.posX+1].estado;
	    }
	    //Este punto no debe ser alcanzable.
	    //De llegar,  dir es un argumento inválido
	    //y no nos podemos mover en la dirección dada.
	    //Se coloca por completud.
	    return false;
        }
      
	/**
	 * "Tumba" el muro de la celda de la que nos movimos en el
	 * laberinto dependiendo la dirección.
	 * @param t La celda de la que nos movimos.
	 * @param direccion La dirección en la que nos movimos.
	 */
        public void tumbaMuro (Celda t,  int direccion){
            switch (direccion){
	    case 0: t.pa = false;
		break;
	    case 1: t.pab = false;
		break;
	    case 2: t.pi = false;
		break;
	    case 3: t.pd = false;
            }            
        }

	/**
	 * "Tumba" los muros de celdas adyacentes
	 * pues tumbaMuro () solo elimina los muros de una
	 * celda. Se asume que es posible el movimiento
	 * de la celda.
	 * @param t El laberinto.
	 * @param direccion La dirección en la que nos movimos.
	 */
        public void tumbaMuros (Laberinto t,  int direccion){
	    //Celda actual
	    tumbaMuro (mundo[t.posY][t.posX], direccion);
	    //Celda vecina
            switch (direccion){
	    case 0: tumbaMuro (mundo[t.posY-1][t.posX], 1);
		break;
	    case 1: tumbaMuro (mundo[t.posY+1][t.posX], 0);
		break;
	    case 2: tumbaMuro (mundo[t.posY][t.posX-1], 3);
		break;
	    case 3: tumbaMuro (mundo[t.posY][t.posX+1], 2);
            }
        }
        
	/**
	 * Realiza el recorrido con backtrack en el laberinto.
	 */
        public void backTrack (){
            LinkedList<Integer> v = new LinkedList<> ();
            boolean mover = false;
            int r = 0;
            while (!mover && v.size () < 4){
                r = rnd.nextInt (4);
		//Hay un vecino disponible.
		//Nos podemos mover.
                if (vecinoDisponible (t, r))
		    mover = true;
                if (!v.contains (r))
                    v.add (r);
	    }
	    if (mover){
		//Nos movemos a la siguiente dirección.
		tumbaMuros (t, r);
		moverLaberinto (t, r);
	    }else if (!p.empty ()){
		//Nos movemos a la celda previa
		//pues no hay vecnos a los que movernos
		Celda a = p.pop ();
		t.posY = a.celdaY;
		t.posX = a.celdaX;                
	    }
	}
        
    }

    /**
     * Punto de entrada del proyecto.
     * @param args the command line arguments
     */
    public static void main (String[] args) {
	PApplet.main (new String[] { "ia.Laberintos" });
    }
    
}
