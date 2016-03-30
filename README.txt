FACTORIZACION DE NUMEROS PRIMOS


INTRODUCCION

Vamos a desarrollar un proyecto software para solucionar un problema simple: descomponer
un número en sus factores primos.  La idea es simple, tenemos un número que debe ser
entero, ya que la factorización solo tiene sentido en los enteros, que además será
positivo, aunque es posible factorizar números negativos no los vamos a tener en cuenta;
y lo vamos a descomponer en una serie números primos que al ser multiplicados entre sí
nos darán el número original.  

A = b * c * d * …. Siendo b,c,d números primos

Si el número a factorizar no se puede descomponer quiere decir que es primo. Por si
alguien está despistado un número primo es aquel que solo es divisible por el mismo y por
1.

Para aclarar qué tipo de números vamos a tratar, estos siempre serán enteros positivos,
tanto los números que vamos a descomponer como los primos resultantes y los posibles
valores intermedios.  Las operaciones que realicemos siempre darán como resultado un
entero positivo, si no fuera así, por ejemplo en una división, el resultado de esta
operación se redondea o se descarta.


ALCANCE

Como se ha dicho antes el problema es sencillo de acometer, buscar los factores de un
número o en su defecto determinar si este es primo es una tarea sencilla, fácil de
comprender  de programar, al menos inicialmente.  Sin embargo veremos que la dificultad
de obtener una solución correcta crece enormemente a medida que el número a factorizar se
hace más grande, hasta el punto en que veremos que es imposible acometerla y resolverla.

Por lo tanto tenemos un problema sencillo de comprender y de atacar pero imposible de
solucionar a partir de cierto nivel.  Sin embargo no debemos desfallecer, Iremos
desarrollando el problema poco a poco desde un nivel básico inicial y pasando a niveles
superiores a medida que hayamos batido el desafío del nivel actual como si se tratará
de un videojuego de aventuras; veremos hasta donde somos capaces de llegar.


DESCRIPCIÓN DEL PROCEDIMIENTO BÁSICO

El procedimiento básico para factorizar un número A es sencillo, buscaremos otros números
menores que él (b,c,d,...), que sean primos, de manera que al dividir nuestro número A
entre estos el resultado sea otro número entero, por ejemplo A/b = B siendo B un entero
positivo y el resto de la división es 0 (cero).  Para buscar los posibles factores
(b,c,d,...) empezaremos dividiendo el número (A) desde el primer primo relevante, que es
el número 2, y los números sucesivos; cuando encontremos un número que divida a  A,
guardaremos el factor y continuaremos buscando factores pero esta vez usaremos el
resultado de la división B como número a factorizar, hasta obtener todos los factores o
determinar que el número que estamos dividiendo es primo.

Veamos un ejemplo, vamos a factorizar el número 14:
1. Probamos a dividirlo entre 2:  14/2   el resultado es un entero = 7
2. Guardo el 2 en la lista de factores primos de 14 y continúo dividiendo usando ahora el
resultado de la división anterior, es decir 7 3. Puesto que el resultó de la última
división fue un entero continuamos probando el mismo factor, solo pasamos al siguiente
cuando la división no devuelva un entero =>  7/2 = 3.5  El resultado no es entero, luego
se descarta.
4. Probamos el siguiente factor: 3 => 7/3= 2.333   El resultado no es entero y se
descarta 5. Probamos el siguiente factor: 4 => 7/4=1.75  No es entero se descarta
6. Probamos el siguiente factor: 5 => 7/5=1.4   No es entero se descarta
7. Probamos el siguiente factor 6 => 7/6=1.16     No es entero se descarta
8. Probamos el siguiente factor 7 => 7/7 = 1  El resultado es entero, pero hemos llegado
al número que estábamos intentando factorizar, así que hemos terminado la busqueda y
determinado que 7 es un factor primo.
9. El resultado final es que los factores primos de 14 son 2 y 7, de hecho 7*2=14



¿CÓMO SÉ QUE EL FACTOR QUE HE OBTENIDO ES UN NÚMERO PRIMO?

Cuando busco los factores de un número este puede ser divisible entre números que son
primos y otros que no lo son, ¿cómo puedo estar seguro que el factor que he encontrado es
un número primo?, por ejemplo el número 16 es divisible entre 2 que es primo, pero
también entre 8, que no lo es.  Ciertamente 8 es un divisor del número 16 y a su vez es
un número compuesto, pero usando la técnica descrita en el apartado anterior, empezando a
probar factores desde el número 2 e ir incrementando en uno cada vez, nos asegura que
antes de llegar a probar el número compuesto (8) como divisor, habremos probado los
factores de este, que necesariamente son menores que él, y por lo tanto si llegamos a
probar el número compuesto (8), el número a factorizar ya no será divisible entre él.
16=2*2*2*2, no llegamos ni a probar el 8
Veamos otro ejemplo: 88 => 88/2 = 44 => 44/2=22 => 22/2=11 ...=> 11/8=1.375 (se descarta)
…=> 11/11=1 (fin)


VERSION 1.0.0

La factorización de un número es un buen ejemplo de tarea adecuada para realizar con un
programa (software), es repetitiva e implica operaciones matemáticas, que son realizadas
muy rápidamente por un ordenador, pero lentamente por una persona.

El procedimiento básico para factorizar un número es es facil de programar, el
funcionamiento básico del programa es:

-Le pasamos el número a factorizar al programa en la linea de comandos
-Creamos un bucle en el que al número a factorizar se le aplica la operación módulo
contra el candidato a ser un factor.  La operación módulo devuelve el resto de la
división entre dos números, si el resto es cero el número a dividir es divisible entre el
candidato, lo que implica que es un factor de este, si el resto es distinto de cero el
número no es divisible entre el candidato y por lo tanto no es un factor de este.  
-Si se encuentra un factor, se añade a la lista de factores, y el número a factorizar se
divide entre el factor, y será el que se use a partir de ahora como número a factorizar;
se vuelve a probar el mismo candidato a factor sobre el nuevo número. 
-Si no se encuentra un factor en la iteración del bucle se incrementa en uno el candidato
y se vuelve a entrar en el bucle.
-El bucle se repite hasta que el candidato a factor sea mayor que el número a factorizar.

