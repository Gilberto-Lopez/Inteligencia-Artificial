package ia.proyecto;

import processing.core.PApplet;
import processing.core.PFont;

import java.util.LinkedList;
import java.util.Random;
import java.lang.Math;

public class Main extends PApplet {

    PFont fuente;  // Fuente para mostrar texto en pantalla
    
    int alto = 15;         // Altura (en celdas) del mundo.
    int ancho = 15;        // Anchura (en celdas) del mundo.
    int celda = 20;          // Tamaño de cada celda cuadrada (en cm/pixeles).
    int radius = 10, directionX = 1, directionY = 0;
    float x = 200.0f;
    float y = 200.0f;
    float speed = 6.0f;

    @Override
    public void setup() {
        size(alto*celda, ancho*celda);
        smooth();
    }

    /**
    * Draws over each iteration the new position of the player.
    */
    @Override
    public void draw() {

        int i = 0;
        background(200);
        float angel = atan2(mouseY - y, mouseX - x);



        if(x >= ancho*10 && x < ancho*11 && y >= alto*6 && y < alto*7){//este if hace que choque contra el obstaculo, visualmente parece que salta pero whatever.
            if(x < ancho*10.5)
                x = (ancho*10)-1;
            else
                x = (ancho*11)+1;

            if(y < alto*6.5)
                y = (alto*6)-1;
            else
                y = (alto*7)+1;

        }else if (dist(mouseX, mouseY, x, y) > speed) { //eso hace que se mueva
                x += cos(angel) * speed; // current location + the next "step"
                y += sin(angel) * speed;
        }



        pushMatrix();
        translate(x, y);
        rotate(angel + PI);
        System.out.println((angel + PI) * 180 / PI);// este es el angulo "REAL" en grados.
        //System.out.println(x);
        rect(-celda/4, 0, celda/2, celda/3);//este es el jugador
        popMatrix();
        rect(ancho*10,alto*6,celda,celda);// este es el obstaculo

    }


    class Linea{ //supongo que esto servira para el sensor.
        int x1;
        int x2;
        int y1;
        int y2;
        boolean visible = true;

        Linea(int x1,int y1,int x2,int y2){
            this.x1 = x1;
            this.x2 = x2;
            this.y1 = y1;
            this.y2 = y2;
        }

    }





    public static void main(String args[]) {
        PApplet.main(new String[] { "ia.proyecto.Main" });
    }


}
