/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ia;

import processing.core.PApplet;
import processing.core.PFont;

import java.util.LinkedList;
import java.util.Hashtable;
import java.util.PriorityQueue;

/**
 *
 * @author Verónica Arriola
 */
public class AEstrella extends PApplet {

    PFont fuente;               // Fuente para mostrar texto en pantalla
    int tamanioMosaico = 60;    // Tamanio de cada mosaico cuadrado (en pixeles).
    int columnas = 21;
    int renglones = 10;

    Mapa mapa;
    boolean expande = false;    // Bandera para solicitar la expansión del siguiente nodo.
    Algoritmo algoritmo;
    
    public void settings() {
        size(columnas * tamanioMosaico, renglones * tamanioMosaico + 70);
    }
    
    /** Configuracion inicial */
    @Override
    public void setup(){
        // size(columnas * tamanioMosaico, renglones * tamanioMosaico + 70);
        background(50);
        fuente = createFont("Arial",12,true);
        textFont(fuente, 12);
        mapa = new Mapa(columnas, renglones);
        mapa.mundo[2][5].tipo = Tipo.OBSTACULO;
        mapa.mundo[2][6].tipo = Tipo.OBSTACULO;
        mapa.mundo[3][6].tipo = Tipo.OBSTACULO;
        mapa.mundo[4][6].tipo = Tipo.OBSTACULO;
        mapa.mundo[5][6].tipo = Tipo.OBSTACULO;
        mapa.mundo[6][6].tipo = Tipo.OBSTACULO;
        mapa.mundo[6][5].tipo = Tipo.OBSTACULO;
        mapa.mundo[4][10].tipo = Tipo.OBSTACULO;

        algoritmo = new Algoritmo();
        Mosaico estadoInicial = mapa.mundo[5][3];
        Mosaico estadoFinal = mapa.mundo[4][15];

        algoritmo.inicializa(estadoInicial, estadoFinal);
    }

    /** Dibuja la imagen en cada ciclo */
    @Override
    public void draw(){
        if(expande) {
            algoritmo.expandeNodoSiguiente();
            expande = false;
        }

        Mosaico m;
        Situacion s;
        for(int i = 0; i < renglones; i++){
            for(int j = 0; j < columnas; j++){
                m = mapa.mundo[i][j];
                s = m.situacion;
                // Dibujar cuadro
                switch(s) {
                    case SIN_VISITAR:
                        stroke(0); fill(50); break;
                    case EN_LISTA_CERRADA:
                        stroke(0); fill(200,200,0); break;
                    case EN_LISTA_ABIERTA:
                        stroke(0); fill(0,200,200); break;
                    case ACTUAL:
                        stroke(0); fill(150,0,150); break;
                    case EN_SOLUCION:
                        stroke(255); fill(0,0,100); break;
                    default:
                        stroke(0); fill(0);
                }
                switch(m.tipo) {
                    case OBSTACULO:
                        stroke(0); fill(200); break;
                    case ESTADO_INICIAL:
                        stroke(0,200,0); fill(0,200,0); break;
                    case ESTADO_FINAL:
                        stroke(200,0,0); fill(200,0,0); break;
                }
                rect(j*tamanioMosaico, i*tamanioMosaico, tamanioMosaico, tamanioMosaico);
                // Escribir datos
                fill(0);
                switch(m.tipo){
                    case ESTADO_INICIAL:
                        text("h(n)=" + m.hn, j*tamanioMosaico+4, (i+1)*tamanioMosaico - 4);
                    continue;
                }
                switch(s) {
                    case EN_SOLUCION:
                        fill(255);
                    case ACTUAL:
                    case EN_LISTA_ABIERTA:
                    case EN_LISTA_CERRADA:
                        text("f(n)=" + m.fn(), j*tamanioMosaico+4, i*tamanioMosaico + 15);
                        text("g(n)=" + m.gn, j*tamanioMosaico+4, (i+1)*tamanioMosaico - 20);
                        text("h(n)=" + m.hn, j*tamanioMosaico+4, (i+1)*tamanioMosaico - 4);
                        ellipse((float)((0.5 + j) * tamanioMosaico), (float)((0.5 + i) * tamanioMosaico), (float)10, (float)10);
                        line((float)((0.5 + j) * tamanioMosaico), (float)((0.5 + i) * tamanioMosaico),
                           (float)((0.5 + j) * tamanioMosaico + (m.padre.columna - m.columna) * 20),
                           (float)((0.5 + i) * tamanioMosaico + (m.padre.renglon - m.renglon) * 20));
                        break;
                }
            }
        }

        fill(0);
        rect(0, renglones * tamanioMosaico, columnas *  tamanioMosaico, 70);

        fill(0,200,0);
        rect(10, renglones * tamanioMosaico + 10, 20, 20);
        fill(255);
        text("Estado inicial", 40, renglones * tamanioMosaico + 30);

        fill(200,0,0);
        rect(10, renglones * tamanioMosaico + 30, 20, 20);
        fill(255);
        text("Estado final", 40, renglones * tamanioMosaico + 50);

        fill(0,200,200);
        rect(2 * tamanioMosaico, renglones * tamanioMosaico + 10, 20, 20);
        fill(255);
        text("Lista abierta", 2 * tamanioMosaico + 30, renglones * tamanioMosaico + 30);

        fill(200,200,0);
        rect(2 * tamanioMosaico, renglones * tamanioMosaico + 30, 20, 20);
        fill(255);
        text("Lista cerrada", 2 * tamanioMosaico + 30, renglones * tamanioMosaico + 50);

        fill(150,0,150);
        rect(4 * tamanioMosaico, renglones * tamanioMosaico + 10, 20, 20);
        fill(255);
        text("Nodo actual", 4 * tamanioMosaico + 30, renglones * tamanioMosaico + 30);

        fill(0,0,100);
        rect(4 * tamanioMosaico, renglones * tamanioMosaico + 30, 20, 20);
        fill(255);
        text("Solución", 4 * tamanioMosaico + 30, renglones * tamanioMosaico + 50);
    }

    
    @Override
    public void mouseClicked() {
        expande = true;
    }


    // --- Clase Mosaico
    // Representa cada casilla del mundo, corresponde a un estado posible del agente.
    class Mosaico{
        Situacion situacion = Situacion.SIN_VISITAR;
        Tipo tipo = Tipo.VACIO;
        int renglon, columna;  // Coordenadas de este mosaico
        int gn;                // Distancia que ha tomado llegar hasta aquí.
        int hn;                // Distancia estimada a la meta.
        Mosaico padre;         // Mosaico desde el cual se ha llegado.
        Mapa mapa;             // Referencia al mapa en el que se encuentra este mosaico.

        Mosaico(int renglon, int columna, Mapa mapa){
            this.renglon = renglon;
            this.columna = columna;
            this.mapa = mapa;
        }

        /** Devuelve el valor actual de fn. */
        int fn() {
            return gn + hn;
        }

        /** Calcula la distancia Manhattan a la meta. */
        void calculaHeuristica(Mosaico meta){
            /**
            * IMPLEMENTACION
            * HINT: calculen la distancia de este mosaico hacia el mosaico meta y luego multipliquenlo por 10
            * para que el valor sea significativo. tampoco deberia haber valores negativos
            */
            hn = 1 * 10;
        }

        /**
        * Devuelve una referencia al mosaico del mapa a donde se movería el agente
        * con la acción indicada.
        */
        Mosaico aplicaAccion(Accion a){
            Mosaico vecino;
            switch(a) {
                case MOVE_UP:
                    if(renglon > 0) {
                    vecino = mapa.mundo[renglon - 1][columna];
                    } else return null;
                    break;
                case MOVE_DOWN:
                    if(renglon < mapa.renglones - 1) {
                    vecino = mapa.mundo[renglon + 1][columna];
                    } else return null;
                    break;
                case MOVE_LEFT:
                    if(columna > 0) {
                    vecino = mapa.mundo[renglon][columna - 1];
                    } else return null;
                    break;
                case MOVE_RIGHT:
                    if(columna < mapa.columnas - 1) {
                    vecino = mapa.mundo[renglon][columna + 1];
                    } else return null;
                    break;
                case MOVE_NW:
                    if(renglon > 0 && columna > 0) {
                    vecino = mapa.mundo[renglon - 1][columna - 1];
                    } else return null;
                    break;
                case MOVE_NE:
                    if(renglon < mapa.renglones - 1 && columna > 0) {
                    vecino = mapa.mundo[renglon + 1][columna - 1];
                    } else return null;
                    break;
                case MOVE_SW:
                    if(renglon > 0 && columna < mapa.columnas - 1) {
                    vecino = mapa.mundo[renglon - 1][columna + 1];
                    } else return null;
                    break;
                case MOVE_SE:
                    if(renglon < mapa.renglones - 1 && columna < mapa.columnas - 1) {
                    vecino = mapa.mundo[renglon + 1][columna + 1];
                    } else return null;
                    break;
                default:
                    throw new IllegalArgumentException("Acción inválida" + a);
            }
            if (vecino.tipo == Tipo.OBSTACULO) return null;
            else return vecino;
        }
    }

    // --- Clase Mapa
    class Mapa {
        int columnas, renglones;
        Mosaico[][] mundo;

        Mapa(int columnas, int renglones) {
            this.columnas = columnas;
            this.renglones = renglones;
            mundo = new Mosaico[renglones][columnas];
            for(int i = 0; i < renglones; i++)
                for(int j = 0; j < columnas; j++)
                  mundo[i][j] = new Mosaico(i, j, this);
        }

    }

    // --- Clase nodo de búsqueda
    class NodoBusqueda implements Comparable<NodoBusqueda> {
        NodoBusqueda padre;  // Nodo que generó a este nodo.
        Accion accionPadre;  // Acción que llevó al agente a este nodo.
        Mosaico estado;      // Refencia al estado al que se llegó.
        int gn;              // Costo de llegar hasta este nodo.

        NodoBusqueda(Mosaico estado) {
            this.estado = estado; 
        }

        /** Asume que hn ya fue calculada. */
        int getFn() {
            return gn + estado.hn;
        }

        /** Calcula los nodos de búsqueda sucesores. */
        LinkedList<NodoBusqueda> getSucesores() {
            LinkedList<NodoBusqueda> sucesores = new LinkedList();
            Mosaico sucesor;
            NodoBusqueda nodoSucesor;
            for(Accion a : Accion.values()) {
                sucesor = estado.aplicaAccion(a);
                if(sucesor != null) {
                    nodoSucesor = new NodoBusqueda(sucesor);
                    nodoSucesor.gn = this.gn + a.costo();
                    nodoSucesor.padre = this;
                    nodoSucesor.accionPadre = a;
                    sucesores.add(nodoSucesor);
                }
            }
            return sucesores;
        }

        public int compareTo(NodoBusqueda nb){
            return getFn() - nb.getFn();
        }

        /** En la lista abierta se considera que dos nodos son iguales si se refieren al mismo estado. */
        public boolean equals(Object o) {
            NodoBusqueda otro = (NodoBusqueda)o;
            return estado.equals(otro.estado);
        }
    }

    // --- A*
    class Algoritmo {
        private PriorityQueue<NodoBusqueda> listaAbierta;
        private Hashtable<Mosaico, Mosaico> listaCerrada;
        Mosaico estadoFinal;  // Referencia al mosaico meta.
        boolean resuelto;

        NodoBusqueda nodoActual;
        NodoBusqueda nodoPrevio;

        void inicializa(Mosaico estadoInicial, Mosaico estadoFinal) {
            resuelto = false;
            this.estadoFinal = estadoFinal;
            // aqui deben incializar sus listas abierta y cerrada
            // listaAbierta = new PriorityQueue();
            // listaCerrada = new Hashtable();
            estadoInicial.calculaHeuristica(estadoFinal);
            estadoInicial.tipo = Tipo.ESTADO_INICIAL;
            estadoFinal.tipo = Tipo.ESTADO_FINAL;

            nodoPrevio = new NodoBusqueda(estadoInicial);
            // listaAbierta.offer(nodoPrevio);
        }

        void expandeNodoSiguiente() {
            /**
              * IMPLEMENTACION
              * HINT: Deben verificar que el juego no este resuelto, despues tomar el primer nodo
              * de la lista abierta (el nodo que tenga menor valor de la funcion f(n)), poner al nodo previo en la lista
              * cerrada, modificando su situacion. Modificar la situacion del nodo actual, verificar si el nodo actual es
              * igual al nodo final, si lo es decir que ya esta resuelto y cambiar de situacion a toda la familia del
              * nodo final, si no lo es hay que generar sus sucesores, verificar en que lista se encuentra y tomar
              * la accion correspondiente.
              */
        }
    }


    static public void main(String args[]) {
        PApplet.main(new String[] { "ia.AEstrella" });
    }

}
