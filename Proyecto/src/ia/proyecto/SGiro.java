package ia.proyecto;

public class SGiro extends Sensor {

    public static final Double SIGMA = 0.7;

    public SGiro () {
        super (0.0, SIGMA);
    }

    @Override
    public void medicion (Double medicion) {
        this.media = medicion + Sensor.RAND.nextGaussian () * this.desviacion;
    }

}
