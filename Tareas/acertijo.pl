%%  Inteligencia Artificial.  %%
%%  Tarea 5.                  %%

%% Nombres.
nombre(elisa).
nombre(felipe).
nombre(isidro).
nombre(luis).
nombre(nuria).
%% Tipos de helado.
helado(bombon).
helado(cono).
helado(copa).
helado(corte).
helado(tarrina).
%% Precios de los helados.
precio(2.0).
precio(2.5).
precio(3.0).
precio(4.0).
precio(5.0).
%% Tipos de relación.
relacion(hermana). %% hermana de la protagonista.
relacion(hermano). %% hermano de la protagonista.
relacion(madre). %% madre de la protagonista.
relacion(novio). %% novio de la protagonista.
relacion(padre). %% padre de la protagonista.

%% Isidro no es novio de la protagonista por 1.
%% Felipe tampoco por 4.
%% Entonces es Luis.
parentesco(luis,novio).
%% Por 1 tenemos que Isidro no es el padre.
%% Entonces es el hermano.
parentesco(isidro,hermano).
%% Y Felipe el padre.
parentesco(felipe,padre).

%% Otra opción.
%%
%% El padre es hombre. No puede ser el novio.
%% Eso sería weird af.
%% parentesco(Padre,padre) :- member(Padre,[felipe,isidro]).
%% El hermano es hombre. No puede ser el novio ni el padre.
%% Eso sería weird af.
%% parentesco(Hermano,hermano) :- member(Hermano,[felipe,isidro]),
%%                                parentesco(Padre,padre),
%%                                Padre \== Hermano.
%%

%% Por 2 tenemos que Nuria no es la madre.
%% Entonces es la hermana.
parentesco(nuria,hermana).
%% Y Elisa la madre.
parentesco(elisa,madre).

%% Otra opción.
%%
%% La madre es mujer (y no es la protagonista).
%% parentesco(Madre,madre) :- member(Madre,[elisa,nuria]).
%% La hermana es mujer. No puede ser la madre.
%% Ni la protagonista.
%% parentesco(Hermana,hermana) :- member(Hermana,[elisa,nuria]),
%%                                parentesco(Madre,madre),
%%                                Madre \== Hermana.
%%

%% Helado al corte costó 2 euros más que el cono.
costo(corte,N) :- member(N,[4.0,5.0]).
costo(cono,N) :- costo(corte,M), N is (M-2).
%% Bombón costo 0.5 más que el del padre.
costo(bombon,N) :- member(N,[2.5,3.0]).
costo(Helado,Precio) :- member(Precio,[2.0,2.5]),
                        parentesco(Padre,padre),
                        pidio(Padre,Helado),
                        costo(bombon,N),
                        Precio is (N-0.5).
%% Posibles opciones de costos.
costo(Helado,Precio) :- member(Helado,[copa,tarrina]), precio(Precio).

%% Isidrio pidió bombón.
pidio(isidro,bombon).
%% El novio y Felipe no pidieron tarrina.
pidio(Nombre,tarrina) :- nombre(Nombre),
                         parentesco(Novio,novio),
                         Nombre \== Novio,
                         Nombre \== felipe.
%% Nuria pidio el más caro.
pidio(nuria,Helado) :- helado(Helado),
                       costo(Helado,N),
                       forall(pidio(_,Helado), forall(costo(Helado,M), N @>= M)).
%% La madre pidio el helado más barato.
pidio(Madre,Helado) :- helado(Helado),
                       parentesco(Madre,madre),
                       costo(Helado,N),
                       forall(pidio(_,Helado), forall(costo(Helado,M), N @=< M)).
%% Posibles opciones de helados.
pidio(Nombre,Helado) :- nombre(Nombre),
                        helado(Helado).

%% Solucion.
%% Nombre y relación están fijos por lo observado anteriormente.
solucion(Nombre1,Nombre2,Nombre3,Nombre4,Nombre5,
         Relacion1,Relacion2,Relacion3,Relacion4,Relacion5,
         Helado1,Helado2,Helado3,Helado4,Helado5,
         Costo1,Costo2,Costo3,Costo4,Costo5) :-
    nombre(Nombre1),
    nombre(Nombre2),
    nombre(Nombre3),
    nombre(Nombre4),
    nombre(Nombre5),
    parentesco(Nombre1,Relacion1),
    parentesco(Nombre2,Relacion2),
    parentesco(Nombre3,Relacion3),
    parentesco(Nombre4,Relacion4),
    parentesco(Nombre5,Relacion5),
    pidio(Nombre1,Helado1),
    pidio(Nombre2,Helado2),
    pidio(Nombre3,Helado3),
    pidio(Nombre4,Helado4),
    pidio(Nombre5,Helado5),
    costo(Helado1,Costo1),
    costo(Helado2,Costo2),
    costo(Helado3,Costo3),
    costo(Helado4,Costo4),
    costo(Helado5,Costo5).

%% Prueba
%% solucion(elisa,felipe,isidro,luis,nuria,madre,padre,hermano,novio,hermana,H1,H2,H3,H4,H5,C1,C2,C3,C4,C5).

