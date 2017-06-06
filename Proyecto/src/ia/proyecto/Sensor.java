package ia.proyecto;

import java.util.Random;

public abstract class Sensor {

    protected Double media;
    protected final Double desviacion;
    protected final Random RAND = new Random ();

    protected Sensor (Double media, Double desviacion) {
        this.media = media;
        this.desviacion = desviacion;
    }

    public Double lectura () {
        return this.media;
    }

    public abstract void medicion (Double meidicion);
    
}
