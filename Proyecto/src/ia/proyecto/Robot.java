package ia.proyecto;

import java.util.Random;

/**
 * Clase Robot, representa un robot con sensores láser, odométrico y de giro.
 */
public class Robot {

    // Números aleatorios.
    private static final Random RAND = new Random ();

    // Posición en el mundo.
    private Par<Double, Double> pos;
    // Posición anterior.
    private Par<Double, Double> posAnt;
    // Ángulo en el que mira el robot.
    // 0 es las 12 del reloj, + sentido de las manecillas del reloj
    // y - sentido contrario.
    private double a;
    // Ángulo en el que miraba el robot.
    private double aAnt;
    // El mundo.
    private Mundo w;
    // Unidad de movimiento especificada por el usuario.
    private double m;
    // Unidad de giro especificada por el usuario en radianes.
    private double r;
    // Sensores láser.
    private SLaser[] laser;
    // Sensor odométrico.
    private SOdometrico odometrico;
    // Sensor de giro.
    private SGiro giro;

    public Robot (Mundo mundo, double distancia, double angulo) {
        // Se coloca en una posición aleatoria del mundo.
        this.pos = new Par<> (RAND.nextDouble () * mundo.ancho (),
            RAND.nextDouble () * mundo.alto ());
        while (mundo.celda (this.pos).obstaculo)
            this.pos = new Par<> (RAND.nextDouble () * mundo.ancho (),
                RAND.nextDouble () * mundo.alto ());
        this.w = mundo;
        this.m = distancia;
        this.r = angulo;
        // Se crean los sensores.
        this.laser = new SLaser[8];
        for (int i = 0; i < 8; i++)
            this.laser[i] = new SLaser ();
        this.odometrico = new SOdometrico ();
        this.giro = new SGiro ();
    }

    /**
     * Regresa la posición actual del robot.
     * @return La posición actual del robot.
     */
    public Par<Double, Double> posicion () {
        return this.pos;
    }

    Par<Double, Double> posAnterior () {
        return this.posAnt;
    }

    double aAnterior () {
        return this.aAnt;
    }

    public double angulo () {
        return this.a;
    }

    public SLaser[] sensoresLaser () {
        return this.laser;
    }

    public SGiro sensorGiro () {
        return this.giro;
    }

    public SOdometrico sensorOdometrico () {
        return this.odometrico;
    }

    public void mover () {
        this.posAnt = this.pos;
        Double x = this.pos.p1 ();
        Double y = this.pos.p2 ();
        this.pos = new Par<> (x + this.m * Math.sin (this.a),
            y - this.m * Math.cos (this.a));
    }

    public void girar (int d) {
        this.aAnt = this.a;
        d = d/d; // 1 o -1
        this.a += d*this.r;
    }

}
