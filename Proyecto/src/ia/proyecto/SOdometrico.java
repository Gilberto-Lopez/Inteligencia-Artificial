package ia.proyecto;

public class SOdometrico extends Sensor {

    public static final Double SIGMA = 0.7;

    public SOdometrico () {
        super (0.0, SIGMA);
    }

    @Override
    public void medicion (Double medicion) {
        this.media += medicion + RAND.nextGaussian ()*desviacion;
    }

}
