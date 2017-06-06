/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ia.proyecto;

import processing.core.PApplet;
import processing.core.PFont;

import java.lang.Math;
import java.util.LinkedList;
import java.util.Hashtable;
import java.util.PriorityQueue;

public class Main extends PApplet {

    PFont fuente;               // Fuente para mostrar texto en pantalla
    int tamanioMosaico = 60;    // Tamanio de cada mosaico cuadrado (en pixeles).
    int columnas = 15;
    int renglones = 10;

    Mundo mundo;
    boolean seMueve = true;    // Bandera para solicitar la expansión del siguiente nodo.
    Robot robot;
    
    public void settings() {
        size(columnas * tamanioMosaico, renglones * tamanioMosaico);
    }
    
    /** Configuracion inicial */
    @Override
    public void setup(){
        // size(columnas * tamanioMosaico, renglones * tamanioMosaico + 70);
        background(50);
        mundo = new Mundo (columnas, renglones, tamanioMosaico);
        robot = new Robot (mundo, 15, Math.PI/16);

    }

    /** Dibuja la imagen en cada ciclo */
    @Override
    public void draw(){
        Mundo.Celda[][] celdas = mundo.celdas();
        Mundo.Celda c;
        for(int i = 0; i < renglones; i++){
            for(int j = 0; j < columnas; j++){
                c = celdas[i][j];
                // Dibujar celda
                if (c.obstaculo) {
                    stroke(0);
                    fill(200);
                } else {
                    stroke(0);
                    fill(50);
                }
                rect(j*tamanioMosaico, i*tamanioMosaico, tamanioMosaico, tamanioMosaico);
                // Escribir datos
                fill(0);
            }
        }
    }

    
    @Override
    public void mouseClicked() {
        //expande = true;
    }

    static public void main(String args[]) {
        PApplet.main(new String[] { "ia.proyecto.Main" });
    }

}
