package ia.proyecto;

import java.lang.Math;
import java.util.Random;

/**
 * Clase Mundo, representa el mundo sobre el cual se desplaza el robot.
 */
public class Mundo {

    /** Proporción de obstáculos presentes en el mundo. */
    public static final double OBSTACULOS = 0.15;
    // Números aleatorios.
    private static final Random RAND = new Random ();

    /* Clase Celda, representa las celdas del mundo. */
    class Celda {
        
        // Posición del centro en el mundo.
        final Par<Double, Double> centro;
        // Tamaño en cm de la celda.
        final int cm;
        // true si es un obstáculo, false en otro caso.
        final boolean obstaculo;
        // La creencia de que el robot esté en esta celda.
        double creencia;
        // Creencias para el cálculo de probabilidades con las observaciones de
        // los sensores láser.
        double[] creencias;
        // Distancias en línea recta al obstáculo más cercano para cada ángulo
        // discretizado.
        double[] distancias;

        // Constructor de la celda.
        public Celda (int x, int y, int cm, boolean obstaculo) {
            this.centro = new Par<> (x*cm + cm/2.0, y*cm + cm/2.0);
            this.cm = cm;
            this.obstaculo = obstaculo;
            this.creencias = new double[8];
        }

    }

    // Representación del mundo.
    private final Celda[][] matriz;
    // Ancho del mundo en celdas.
    private int ancho;
    // Alto del mundo en celdas.
    private int alto;
    // Tamaño de las celdas.
    private final int cm;

    /**
     * Construye un nuevo mundo de tamaño alto x ancho celdas, cada una
     * cuadrada de tamaño cm dado en centímetros.
     * @param ancho El ancho del mundo en celdas.
     * @param alto El alto del mundo en celdas.
     * @param cm El tamaño del lado de una celda en centímetros.
     */
    public Mundo (int ancho, int alto, int cm) {
        this.cm = cm;
        this.alto = alto;
        this.ancho = ancho;
        this.matriz = new Celda[alto][ancho];
        // Creamos las celdas y les asignamos su creencia inicial.
        int n = 0;
        for (int i = 0; i < alto; i++)
            for (int j = 0; i < ancho; j++) {
                boolean obst = RAND.nextDouble () < OBSTACULOS;
                if (!obst)
                    n++;
                this.matriz[i][j] = new Celda (j, i, cm, obst);
            }
        // La creencia para cada celda disponible es la misma al principio.
        for (int i = 0; i < alto; i++)
            for (int j = 0; i < ancho; j++)
                if (!this.matriz[i][j].obstaculo)
                    this.matriz[i][j].creencia = 1.0 / n;
        calculaDistanciasCeldas ();
    }

    /* Calculamos la distancia de cada celda no obstáculo al obstáculo más
     * cercano en línea recta. */
    private void calculaDistanciasCeldas () {
        double c1 = cm/2.0;
        double c2 = Math.sqrt(2.0)*c1;
        Celda actual;
        for (int i = 0; i < alto; i++) {
            for (int j = 0; i < ancho; j++) {
                actual = this.matriz[i][j];
                if (!actual.obstaculo) {
                    double[] d = {0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0};
                    // Dir 0.
                    int k = 1;
                    while (i - k >= 0 && !this.matriz[i-k][j].obstaculo)
                        k++;
                    d[0] = k*cm - c1;
                    // Dir 1.
                    k = 1;
                    while (i - k >= 0 && j + k < ancho
                        && !this.matriz[i-k][j+k].obstaculo)
                        k++;
                    d[1] = k*cm - c2;
                    // Dir 2.
                    k = 1;
                    while (j + k < ancho && !this.matriz[i][j+k].obstaculo)
                        k++;
                    d[2] = k*cm - c1;
                    // Dir 3.
                    k = 1;
                    while (i + k < alto && j + k < ancho
                        && !this.matriz[i+k][j+k].obstaculo)
                        k++;
                    d[3] = k*cm - c2;
                    // Dir 4.
                    k = 1;
                    while (i + k < alto && !this.matriz[i+k][j].obstaculo)
                        k++;
                    d[4] = k*cm - c1;
                    // Dir 5.
                    k = 1;
                    while (i + k < alto && j - k >= 0
                        && !this.matriz[i+k][j-k].obstaculo)
                        k++;
                    d[5] = k*cm - c2;
                    // Dir 6.
                    k = 1;
                    while (j - k >= 0 && !this.matriz[i][j-k].obstaculo)
                        k++;
                    d[6] = k*cm - c1;
                    // Dir 7.
                    k = 1;
                    while (i - k >= 0 && j - k >= 0
                        && !this.matriz[i-k][j-k].obstaculo)
                        k++;
                    d[7] = k*cm - c2;
                    actual.distancias = d;
                }
            }
        }
    }

    /**
     * Dado un par de números, regresa la celda correspondiente en el mundo.
     * @param posicion Un par de números.
     * @return La celda que corresponde al par de números dado.
     */
    public Celda celda (Par<Double, Double> posicion) {
        if (posicion.p2() >= this.alto*this.cm ||
            posicion.p1() >= this.ancho*this.cm ||
            posicion.p2() < 0.0 || posicion.p1() < 0.0)
            return null;
        int x = posicion.p1 ().intValue ();
        int y = posicion.p2 ().intValue ();
        return this.matriz[y/cm][x/cm];
    }

    /**
     * Dado un ángulo en radianes, regresa el ángulo discretizado.
     * @param t El ángulo.
     * @return El ángulo discretizado.
     */
    public int anguloDiscretizado (double t) {
        t += 22.5;
        while (t <= 0)
            t += 2*Math.PI;
        t = t % (2*Math.PI);
        int i = 0;
        while(t > 45.0) {
            t -= 45.0;
            i++;
        }
        return i;
    }

    /**
     * Regresa el alto del mundo en centímetros.
     * @return El alto del mundo en centímetros.
     */
    public int alto () {
        return this.alto * this.cm;
    }

    /**
     * Regresa el ancho del mundo en centímetros.
     * @return El ancho del mundo en centímetros.
     */
    public int ancho () {
        return this.ancho * this.cm;
    }

    public void p_st_l (Robot r) {
        int t = anguloDiscretizado (r.angulo ());
        double d = Math.sqrt (2*Math.PI)*SLaser.SIGMA;
        double ed = 2*SLaser.SIGMA*SLaser.SIGMA;
        for (Celda[] a : this.matriz) {
            for (Celda c : a) {
                SLaser[] sensores = r.sensoresLaser ();
                for (int i = 0; i < 8; i++) {
                    double m = sensores[i].lectura () - c.distancias[(i + t) % 8];
                    c.creencias[i] = Math.exp(-m*m/ed)/d;
                }
            }
        }
    }

    public double p_th_thptht (Robot r) {
        int th = anguloDiscretizado (r.angulo ());
        int thp = anguloDiscretizado (r.aAnterior ());
        double ed = SGiro.SIGMA*SGiro.SIGMA;
        double d = Math.sqrt (2*Math.PI)*SGiro.SIGMA;
        double m = r.sensorGiro ().lectura () - (th - thp);
        return Math.exp(m*m/ed)/d;
    }

    // Si consideramos la posición del robot es el centro de lp
    // y mira en el ángulo theta', al desplazarse su posición sería
    // virtualmente
    // (ant.p1 () + at*Math.sin (r.angulo ()), ant.p2 () - at*Math.cos (r.angulo ()))
    // entonces tomamos la distancia desde este punto al centro de l
    // m1^2+m2^2 y le sumamos un factor de error m3^2, que es la diferencia
    // entre el ángulo en que mira el robot y el ángulo de la recta que pasa
    // por los centros, mientras más diverjan estos ángulos menos probable es
    // que el robot se acerque a l desde lp, al sumar m3^2 al exponente nos
    // alejamos del centro de la densidad en 0 y caemos en un punto donde se
    // acumula menos probabilidad y se ve reflejado este hecho.
    public double p_l_lpat (Robot r, Celda l, Celda lp) {
        double ed = 2*SOdometrico.SIGMA*SOdometrico.SIGMA;
        double d = Math.sqrt (2*Math.PI)*SOdometrico.SIGMA;
        double at = r.sensorOdometrico ().lectura ();
        Par<Double, Double> ant = lp.centro;// r.aAnterior ();
        Par<Double, Double> pos = l.centro;// r.posicion ();
        // double m1 = ant.p1 () + at*Math.cos (r.aAnterior ()) - pos.p1 ();
        double m1 = ant.p1 () + at*Math.sin (r.angulo ()) - pos.p1 ();
        // double m2 = ant.p2 () + at*Math.sin (r.aAnterior ()) - pos.p2 ();
        double m2 = ant.p2 () - at*Math.cos (r.angulo ()) - pos.p2 ();
        // double m3 = r.aAnterior () - r.angulo ();
        double m3 = r.angulo () - Math.atan((pos.p1()-ant.p1())/(pos.p2()-pos.p1()));
        return Math.exp(-(m1*m1+m2*m2+m3*m3)/ed)/d;
    }

}
