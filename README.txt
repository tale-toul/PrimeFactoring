FACTORIZACION DE NUMEROS PRIMOS

Author: tale.toul@gmail.com

INTRODUCCION

Vamos a desarrollar un proyecto software para solucionar un problema simple: descomponer
un número en sus factores primos.  La idea es simple, tenemos un número que debe ser
entero, ya que la factorización solo tiene sentido en los enteros, que además será
positivo, aunque es posible factorizar números negativos no los vamos a tener en cuenta;
y lo vamos a descomponer en una serie números primos que al ser multiplicados entre sí
nos darán el número original.  

A = b * c * d * .... Siendo b,c,d números primos

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


VERSION 1.0

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


Validación de resultados

Vamos a añadir algunos métodos para validar los resultados obtenidos por nuestro
programa.
En primer lugar usaremos una función para comprobar que los resultados obtenidos son
correctos.  Esta función es facil de implementar, se le pasa el número que hemos
factorizado y los factores que hemos encontrados; multiplicamos los factores entre sí y
debemos obtener el número a factorizar.  No vamos a comprobar si los factores son números
primos.

Un segundo método de validación consiste en tener una batería de pruebas conocida, un
conjunto de números primos con sus factores ya calculados, ejecutar el programa de tal
manera que lea la lista de números de la batería de pruebas y compare los resultados
obtenidos con los resultados de la batería.  Este método está pendiente de programar.


Pruebas

Vamos a ver hasta donde podemos llegar con esta versión del programa, probaremos a
factorizar números cada vez más grandes y veremos cuanto tarda el programa en obtener sus
factores.  
Nos interesan dos aspectos principales en el proceso: Obtener un resultado correcto al
factorizar el número; que el tiempo de resolución del problema (factorizar) sea razonable.

Definiremos varios parametros importantes:
-El tamaño del número a factorizar.- Para cuantificar el número a factorizar
consideraremos solo el número de cifras que lo componen y no el número concreto. El
número de cifras determinará el nivel que hemos batido con nuestro programa.

-El tiempo que tarde en ser factorizado.- La calidad de nuestro programa se mide por dos
factores principales: que sea capaz de factorizar el número correctamente y que lo haga
dentro de un tiempo razonable, definiremos un tiempo máximo para factorizar un número de
una hora, y veremos hasta que nivel llegamos con este tiempo. 
Al definir un tiempo máximo necesitamos un mecanismo que nos permita medir el tiempo que
tarda el programa y otro que nos permita detener el programa y que este muestre por donde
iba cuando se detuvo: los factores encontrados y hasta qué candidato ha
probado.  Para poder comparar el tiempo que tarda nuestro programa en resolver
cada factorización definiremos un hardware standard, este será un Raspberry Pi.

-El tipo de número a factorizar.- Intentaremos factorizar varios tipos de números: al
menos un número compuesto de más de dos factores; al menos un número compuesto por dos
factores de tamaño similar (en cifras); al menos un número primo.  Cada uno de estos
números tardará un tiempo distinto en ser factorizado, siendo el número primo el que más
tarde con diferencia.



Generacion automática de casos de prueba

Para generar casos de prueba sin necesidad de introducirlos uno a uno voy a usar la
siguiente orden en una consola:

 # for x in {1..500}; do ./PrimeFactor.py --addtest testcases.dat -v $(python -c "import random;print random.randint(1000000,9999999)"); done

Esta orden esta compuesta por un bucle que se ejecutará 500 veces, dentro del bucle se
ejecuta el programa de factorización, y el número a factorizar es generado por un trozo de
código python, que genera un número aleatorio dentro del rango que se le indica.




Pruebas de la versión 1.0
Para estas pruebas usaremos como plataforma hardware un Raspberry Pi modelo B
revisión 1, con sistema operativo raspbian jessie

-Nivel 1 
 En este nivel los números compuestos y los primos serán de una sola cifra, por no ser
 posible reducir el número de cifras en menos que uno.
 
 1-Número compuesto múltiple.- Solo existe un caso que podemos usar para un número
 compuesto por más de dos números primos, este es el 8=[2,2,2]
    8 = [2, 2, 2] In 0.000190019607544 seconds
 2-Número compuesto por dos primos.- Usaremos el 9=[3,3]
    9 = [3, 3] In 0.000190019607544 seconds
 3-Número primo.- 7=[7]
    7 = [7] In 0.000192880630493 seconds
 4-Adicionalmente guardaremos como casos de prueba todos los números interesantes de una
 cifra, desde el 1 al 9

 Nivel batido. Los tiempos de factorización son del orden de microsegundos. 


-Nivel 2
 1-Número compuesto múltiple
    30 = [2, 3, 5] In 0.000200986862183 seconds
 2-Número compuesto por dos primos
    14 = [2, 7] In 0.000207901000977 seconds
 3-Número primo
    17 = [17] In 0.000205993652344 seconds
 
 Nivel batido. Los tiempos siguen siendo ridiculos

-Nivel 3
 1-Número compuesto múltiple
    172 = [2, 2, 43] In 0.000254154205322 seconds
 2-Número compuesto por dos primos
    187 = [11, 17] In 0.000391006469727 seconds
 3-Número primo
    487 = [487] In 0.00111198425293 seconds
    683 = [683] In 0.00135493278503 seconds

 Nivel batido. Los tiempos de factorización suben al orden de los milisegundos.

-Nivel 4
 1-Número compuesto múltiple
    4823 = [7, 13, 53] In 0.000292778015137 seconds
 2-Número compuesto por dos primos
    6523 = [11, 593] In 0.00151515007019 seconds
 3-Número primo
    4871 = [4871] In 0.008544921875 seconds
    5441 = [5441] In 0.00976800918579 seconds

 Nivel batido. 

-Nivel 5
 1-Número compuesto múltiple
    16523 = [13, 31, 41] In 0.000253915786743 seconds
 2-Número compuesto por dos primos
    26233 = [37, 709] In 0.00139808654785 seconds
 3-Número primo
    27253 = [27253] In 0.0481271743774 seconds
    68171 = [68171] In 0.118710041046 seconds
 
 Nivel batido. El número del apartado dos, que tomaremos como referencia está todavía en
 el orden de los milisegundos.

-Nivel 6
 1-Número compuesto múltiple
    372531 = [3, 23, 5399] In 0.00950002670288 seconds
 2-Número compuesto por dos primos
    332621 = [487, 683] In 0.00151205062866 seconds
 3-Número primo
    375643 = [375643] In 0.667051076889 seconds

Nivel batido. Seguimos en milisegundos para el número (2) pero estamos en más de medio
segundo para el número primo.

-Nivel 7
 1-Número compuesto múltiple
    5577944 = [2, 2, 2, 19, 36697] In 0.064346075058 seconds
 2-Número compuesto por dos primos
    2713147 = [557, 4871] In 0.00906491279602 seconds
 3-Número primo
    5587943 = [5587943] In 9.97602105141 seconds

Nivel batido. Para los números (1) y (2) los tiempos siguen siendo bajas (centesimas y
milesimas de segundo, pero para el número (3) el tiempo a subido a casi 10 segundos, lo
que supone multiplicar por más de 10 el tiempo del número (3) del nivel 6.

-Nivel 8
 1-Número compuesto múltiple
    12773543 = [29, 151, 2917] In 0.00515103340149 seconds
 2-Número compuesto por dos primos
    26503111 = [4871, 5441] In 0.0102159976959 seconds
 3-Número primo
    12763547 = [12763547] In 22.8130741119 seconds

Nivel batido. 

-Nivel 9

 1-Número compuesto múltiple
    455133121 = [139, 1237, 2647] In 0.00713801383972 seconds
    370918413 = [3, 3, 3, 71, 181, 1069] In 0.00222587585449 seconds
 2-Número compuesto por dos primos
    370918411 = [5441, 68171] In 0.154046058655 seconds
 3-Número primo
    370918423 = [370918423] In 662.737498045 seconds 

Nive batido. Esta vez el caso (3) ha tardado algo más de 11 minutos, lo cual es un tiempo
considerable, pararemos las pruebas en este nivel y buscaremos alguna mejora en el
programa que reduzca el tiempo de cálculo.


    
VERSION 1.1

En la versión 1.0 fuimos capaces de llegar al nivel 9, sin embargo el tiempo necesario
para determinar que un número es primo en este nivel se multiplico por más de 10 con
respecto al nivel 8. Necesitamos modificar el programa para hacer que el algoritmo de
factorización sea más eficiente.

ELIMINACION DE NUMEROS PARES

La mejora que vamos a introducir en esta versión es la eliminación de los números pares en
los chequeos de los candidatos; por definición sabemos que un número par es siempre
divisible por 2, y por lo tanto no puede ser un número primo.
El funcionamiento del algoritmo de factorización empezará probando el número 2, que es el
primer número par y por lo tanto sí puede ser primo.  El número compuesto se prueba a
dividir por 2, si es divisible se volverá a probar a dividior por 2, así tantas veces como
el numero resultante de la división siga siendo divisible por 2, por ejemplo 8 será
probado tres veces a divir por 2.
Cuando el número resultante de la división ya no sea divisible por 2, aumentamos en uno el
candidato, pasando al 3, y probamos a dividir de nuevo, cuando el número a factorizar no
sea divisible por 3, no pasamos al siguiente sino que saltamos al 5, sumando 2 al
candidato anterior, y así a partir de ese momento, se sumará dos a candidato anterior
pasando siempre al siguiente número impar.
Con esta mejora conseguimos reducir el número de comprobaciones de divisibilidad a la
mitad y por lo tanto debe suponer un aumento considerable en la velocidad del programa.


Pruebas de la versión 1.1

En esta versión vamos a empezar con el nivel 6, ya que los anterirores ya se resolvian muy
rápido en la versión 1.0

-Nivel 5
 1-Número compuesto múltiple
    66753 = [3, 3, 7417] In 0.0067 seconds
 2-Número compuesto por dos primos
    26233 = [37, 709] In 0.0008 seconds
 3-Número primo
    36523 = [36523] In 0.0328 seconds
    76753 = [76753] In 0.0673 seconds

Nivel batido.  Como se esperaba los tiempos son mejores.

-Nivel 6
 1-Número compuesto múltiple
    372531 = [3, 23, 5399] In 0.006 seconds
    658724 = [2, 2, 11, 11, 1361] In 0.0016 seconds
 2-Número compuesto por dos primos
    332621 = [487, 683] In 0.0009 seconds
 3-Número primo
    375643 = [375643] In 0.3989 seconds
    651727 = [651727] In 0.6983 seconds

Nivel batido.

-Nivel 7
 1-Número compuesto múltiple
    5577944 = [2, 2, 2, 19, 36697] In 0.0483 seconds
 2-Número compuesto por dos primos
    2713147 = [557, 4871] In 0.0068 seconds
    4789649 = [2053, 2333] In 0.0026 seconds
 3-Número primo
    5587943 = [5587943] In 5.9718 seconds
    4789637 = [4789637] In 4.1817 seconds

Nivel batido.
 
-Nivel 8
 1-Número compuesto múltiple
    12773543 = [29, 151, 2917] In 0.004 seconds
 2-Número compuesto por dos primos
    26503111 = [4871, 5441] In 0.0061 seconds
 3-Número primo
    12763547 = [12763547] In 11.1387 seconds
    32763557 = [32763557] In 34.7135 seconds
    52763197 = [52763197] In 45.9598 seconds

Nivel batido.  En la "factorización" del número primo es donde se ve claramente que el
tiempo requerido se ha reducido a la mitad, ya que ahora solo probamos la mitad de los
posibles candidatos.

-Nivel 9

 1-Número compuesto múltiple
    455133121 = [139, 1237, 2647] In 0.0025 seconds
    370918413 = [3, 3, 3, 71, 181, 1069] In 0.0013 seconds

 2-Número compuesto por dos primos
    370918411 = [5441, 68171] In 0.0606 seconds

 3-Número primo
    370918423 = [370918423] In 324.2495 seconds (más de 5 minutos)
    469241039 = [469241039] In 410.9201 seconds
    540918487 = [540918487] In 573.4807 seconds 

Nivel batido.  En el cálculo del número primo es donde vemos la gran mejora de esta
version, el timpo se ha reducido a la mitad del que se necesito en la version 1.0.  

-Nivel 10
 1-Número compuesto múltiple
    1569874542 = [2, 3, 47, 1063, 5237] In 0.005 seconds
    6569874545 = [5, 13, 83, 1217771] In 5.4298 second
    6569374545 = [3, 3, 5, 19, 7683479] In 29.44 seconds.- El caso de este número es
    intereante, si factorizamos el último primo (7683479) solo necesita unos 7 segundos,
    pero el número completo tarda 4 veces más, no se a qué se debe esto ya que los
    primeros factores se encuentran rápido y entonces nos queda el último factor, que
    ahora tarda mucho más. 
    
 2-Número compuesto por dos primos
 3-Número primo
    1569874541 = [1569874541] In 1367.8559 seconds (más de 22 minutos)
    3569874547 = [3569874547L] In 12343.9727 seconds (más de 3 horas y media)

Nivel NO batido.  Este nivel de momento nos bate a nosotros.



INCREMENTO EN LA COMPLEJIDAD DEL PROBLEMA 

En cada nivel que hemos ido abordando, el tiempo necesario para completar la factorización
de un número crece, como era de esperar.  Este crecimiento sin embargo es muy distinto
según el tipo de número que estemos factorizando, si el número es compuesto los tiempos no
han crecido mucho a lo largo de los diferentes niveles, hasta llegar la nivel 10 donde se
observa un fenómeno extraño: un número compuesto tarda mucho más en factorizarse que la
suma de las factorizaciones de sus primos.

Donde sí vemos diferencias importantes es a la hora de "factorizar" números primos, en
cada nivel se observa un incremento en el tiempo de aproximadamente de 10 veces con
respecto al tiempo que se necesito en el nivel anterior.  Esto se debe a que el conjunto
números posibles a factorizar se multiplica por 10 cada vez que añadimos una cifra a los
números (subimos un nivel).  

Por ejemplo, si estamos factorizando números de 3 cifras, el conjunto total es de 999
(1 a 999), si ahora añadimos una cifra y factorizamos números de 4 cifras, el conjunto
total es de 9999 (1 a 9999) diez veces más.  

A todos los efectos esto quiere decir que la complejidad media del problema tiene un
crecimiento exponencial, multiplicandose por 10 por cada cifra que añadimos al número a
factorizar.  

Es por este incremento exponencial que, como dijimos al principio, el problema no tiene
solución dentro de un tiempo razonable.  Es posible mejorar el rendimiento del programa,
pero por mucho que lo mejoremos no seremos capaces de mantener un ritmo de mejora
equiparable al aumento de la complejidad del problema.

Es interesante darse cuenta que, cuando subimos un nivel de dificultad aumentando una cifra
al número a factorizar, el conjunto de números del anterior nivel que hemos conseguido superar, solo
supone el 10% del conjunto total de los posibles números a factorizar en este nivela.
Visto de otro modo, si descartamos todos los números de los anteriores niveles ya
superados, aun tenemos el 90% del problema sin resolver.

Aun con esta nueva visión derrotista de nuestro problema, veremos que podemos aplicar
técnicas que mejoraran mucho el rendimiento del programa, permitiendonos llegar a niveles
superiores.




 1-Número compuesto múltiple
 2-Número compuesto por dos primos
 3-Número primo
