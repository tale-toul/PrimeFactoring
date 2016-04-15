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

En esta versión vamos a empezar con el nivel 5, ya que los anterirores ya se resolvian muy
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
    3569874547 = [3569874547L] In 12343.9727 seconds (más de 3 horas y media).- La
    factorización de este número es mucho más lenta, esto se debe a que hemos pasado de
    usar un número de tipo "int" a uno sin límite de precisión, la pista está en el sufijo
    L:
    https://docs.python.org/2/library/stdtypes.html#numeric-types-int-float-long-complex
    El número máximo que se puede tratar como int viene determinado por sys.maxint:

        >>import sys
        >>sys.maxint
        2147483647

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



INFORMES ASINCRONOS Y RALENTIZACION

En la versión 1.1.1 he añadido la funcionalidad de mostrar el estado de la factorización
del número de forma asíncrona.  Cuando la aplicación recibe una señal SIG.USR1 mediante
una orden como:

    $ kill -USR1 <pid>

Se detiene la ejecución de forma temporal mientras se ejecuta una función que muestra los
factores que se han encontrado hasta ahora, el último candidato probado, y el tiempo que
lleva ejecutandose la factorización, después de esto la ejecución continua por donde iba.
Esta funcionalidad es muy util ya que permite ver por donde va la factorización y hacernos
una idea de cuanto va a tardar.  

Sin embargo he observado que esta funcionalidad ralentiza la ejecución del programa,
parece que se comprueba o muestrea la posible llegada de la señal de forma periodica lo
que hace que el tiempo de ejecución de una factorización se multiplique por dos, con lo
que perdemos la mejora que habíamos ganado con la eliminiación del chequeo de los números
pares.

Voy a cambiar el código para que esta funcionalidad se pueda activar a través de una
opción de línea de comandos, pero por defecto este dessactivada.



Actualizacion sobre el problema de ralentización

Después de varias pruebas he podido comprobar que la ralentización del programa no se
debe a la existencia de la comprobación de la señal extena USR1, sino a la transformación
de la variable "candidate" en global, en lugar de local como hasta ahora.  Por lo que se
ve el acceso a una variable global es más lento que el uso de una local.

Para recuperar el rendimiento de la aplicación tengo que volver a usar la variable
"candidate" como local a la función "factorize", pero sin sacrificar la funcionalidad de
mostrar de forma asincrona el estado de la factorización.

En la versión 1.1.3 las variables **pfactors** y **candidate**, esta última es la más importante,
se vuelven a dejar como locales a la función "_factorize_".  Para poder mostrar estas
variables cuando llega una señal USR1 se utiliza el _stack frame_ que se le pasa como
parametro a la función que maneja la señal; este _stack frame_ se puede consultar a traves
del módulo **inspect** en concreto el método **inspect.getargvalues(stack)** que devuelve
entre otros un diccionario con las variables locales de la función que se estaba
ejecutando cuando se recibió la señal:

   (args,varargs,keywords,local_vars)=inspect.getargvalues(stack)

Ahora ya puedo mostrar el valor accediendo a ellas:

    local_vars['pfactors']
    local_vars['candidate']



VERSION 1.2

Esta versión es una extensión de la versión 1.1.  Hemos llevado un poco más haya el
concepto de no probar números que sabemos positivamente que no son primos.  

En esta versión no vamos a probar los números que terminan en 5, excepto el propio 5.
Primero probaremos los candidatos 2, 3 y 5, y luego entramos en un bucle general que va
probando los números que terminan en 7, 9, 1 y 3, a parte de los números pares que ya no
probabamos, también nos saltamos los números que son divisibles por 5. 

Si el número a factorizar esta compuesto exclusivamente por factores 2, 3 y 5 no se
comprueba la condición de final del programa (candidate <= compnum) hasta llegar al bucle
principal, sin embargo esto no supondra apenas perdida de tiempo.

Ya en el bucle principal probamos cada candidato terminado en 7, 9, 1 y 3 sin añadir
ninguna condición adicional, solo estamos expandiendo las comprobacione que antes teníamos
en un solo bucle while; tras comprobar el candidato terminado en 3 en lugar de añadir 2 al
candidato, añadimos 4 y saltamos el 5, llegando al 7.  

La clave para mejorar la velocidad de factorización está en no añadir nuevas
comprobaciones y eliminar un candidato de cada 5 posibles lo que supone una reducción del
20% en el número de candidatos a probar, lo cual debe traducirse en una reducción de ese
mismo 20% en el tiempo de factorización de los un números.




Pruebas de la versión 1.2

-Nivel 7
 1-Número compuesto múltiple
    5577944 = [2, 2, 2, 19, 36697] In 0.025 seconds
 2-Número compuesto por dos primos
    2713147 = [557, 4871] In 0.0036 seconds
    4789649 = [2053, 2333] In 0.002 seconds
 3-Número primo
    5587943 = [5587943] In 4.4989 seconds
    4789637 = [4789637] In 3.8675 seconds

Nivel batido.

-Nivel 8
 1-Número compuesto múltiple
    12773543 = [29, 151, 2917] In 0.0021 seconds
 2-Número compuesto por dos primos
    26503111 = [4871, 5441] In 0.0038 seconds
 3-Número primo
    12763547 = [12763547] In 8.4344 seconds
    32763557 = [32763557] In 22.211 seconds
    52763197 = [52763197] In 36.5111 seconds

Nivel batido.

-Nivel 9
 1-Número compuesto múltiple
    455133121 = [139, 1237, 2647] In 0.002 seconds
    370918413 = [3, 3, 3, 71, 181, 1069] In 0.001 seconds

 2-Número compuesto por dos primos
    370918411 = [5441, 68171] In 0.0471 seconds

 3-Número primo
    370918423 = [370918423] In 247.586 seconds
    469241039 = [469241039] In 376.4097 seconds
    540918487 = [540918487] In 441.5368 seconds

Nivel batido.

-Nivel 10
 1-Número compuesto múltiple
    
    1569874542 = [2, 3, 47, 1063, 5237] In 0.0044 seconds
    6569874545 = [5, 13, 83, 1217771] In 3.427 seconds
    6569374545 = [3, 3, 5, 19, 7683479] In 22.5648 seconds.  Aunque se ha acelerado la
    factorización sigue pasando lo mismo con este número, si factorizamos el último primo
    (7683479) solo necesita unos 7 segundos, pero el número completo tarda 4 veces más, no
    se a qué se debe esto ya que los primeros factores se encuentran rápido y entonces nos
    queda el último factor, que ahora tarda mucho más. 
    
 2-Número compuesto por dos primos
    2803249819 = [36523, 76753] In 0.2087 seconds

 3-Número primo

    1569874541 = [1569874541] In 1271.9291 seconds
    3569874547 = [3569874547L] In 8839.9594 seconds.  Más de 2 horas y media, parte de la
        mejora en la velocidad puede deberse a que he cerrado otras aplicaciones (vim) y
        he dejado la sesión (screen) desconectada de la consola ssh.  El tiempo ha
        mejorado mucho pero aun es demasiado.

Nivel no batido.


VERSION 1.3

Las versiones 1.1 y 1.2 han mejorado el rendimiento sensiblemente, eliminando el 60% de
los candidatos a probar en el proceso de factorización: de cada decena eliminamos los
números pares y los terminados en 5.  Sin embargo esta importate mejora se queda en poca
cosa cuando la comparamos con el incremento de dificultad al pasar al nivel 10, no solo se
multiplica por 10 el numero de posibles números, sino que además los números que superan
el límite de aquellos que se pueden representar internamente con un entero (int), son
representados con un tipo de número sin límite que es más lento en el tratamiento, de ahí
que el incremento a la hora de calcular un número primo en el nivel 10 se haya
multiplicado, no por 10, sino por 40.

En resumen nuestras mejoras no nos han permitido superar ni un solo nivel.  Intentaremos
corregir este defecto en la versión 1.3 del programa.



Descarte de candidatos insensatos

Vamos a fijarnos bien en el procedimiento de factorización y ver como podemos mejorarlo,
nos interesa eliminar más candidatos del proceso de busqueda de factores.

Cuando empezamos a buscar candidatos siempre empezamos desde los más pequeños, el primero
que probamos es el 2.  Si nuestro número es divisible entre 2, lo dividimos, guardamos el
2 en la lista de factores y continuamos con la facorización del número resultante de la
división, y ahora el problema se ha reducido a la mitad.  ¿Pero qué pasa si el número no es
divisible entre 2? cogemos el siguiente candidato, el 3 y repetimos el proceso anterior, y
así continuamos hasta que el candidato sea igual al número a factorizar, se dividen ambos,
el resultado es 1 y entonces el siguiente candidato es más grande que el número a
factorizar (1) y se termina la factorización.

Todo esto ya lo sabemos, pero pensemos un momento en la situación en que los candidatos
que estamos probando son grandes y están ya cerca del número a factorizar.  Es evidente
que estos candidatos no pueden ser factores del número a factorizar, si uno de ellos lo
fuera, esto quiere decir que al dividir nuestro número entre el candidato, debo obtener
otro número entero, que además debe ser muy pequeño porque nuestro candidato es grande (se
acerca al número a factorizar).  El candidato más pequeño posible es el 2, así que
cualquier candidato "grande" que al dividir al número a factorizar de como resultado menos
que dos, es un candidato "insensato" que nunca puede ser factor del número a factorizar y
lo podemos descartar.

Veamoslo desde otro punto de vista: supongamos que dividimos el número a factorizar entre
el primero de los factores posibles, que es el 2; si el número no es divisible entre 2,
cualquier candidato que sea mayor que la el número partido por 2 no puede ser un factor de
este, ya que cualquier número mayor que la mitad del número a factorizar, al multiplicarlo
por el menor de los números primos posibles (2) simpre nos dará un número mayor que el
número original, y si lo multiplicamos por otro factor más grande (3,5,7,etc) el resultado
será aun mas grande que el número original.  En conclusión cualquier candidato que sea
mayor que la mitad del número a factorizar no puede ser un factor válido, es pues un
candidato "insensato" y lo podemos descartar desde el principio, reduciendo a la mitad, de
un plumazo el número de candidatos a probar.

Esta idea la podemos extender, supongamos que ahora dividimos el número a factorizar entre
el siguiente candidato (3), si es divisible calculamos el resultado, guardamos el factor
y continuamos factorizando el número resultante.  Pero si no es divisible, cualquier
candidato mayor que el número a factorizar dividido entre 3 no puede ser un factor válido,
ya que cualquiera de estos candidatos al multiplicarlos por otro candidato mayor que 3 nos
da como resultado un número mayor que el número a factorizar, y ya sabemos que no los
podemos multiplicar por 2 ó por 3, que ya hemos determinado que no son factores válidos
del número a factorizar.  Por lo tanto si el número a factorizar no es divisible entre 3
lo candidatos mayores que 1 tercio del número a factorizar son candidatos "insensatos" y
los descartamos.

Este patrón se repite para cada candidato que probamos y no es un factor del número a
factorizar.  Si el número no es divisible entre el candidato, todo posible candidato mayor
que el número a factorizar dividido entre el actual candidato se puede descartar.

Cambiaremos nuestro algoritmo de calculo y por cada candidato que probemos ajustaremos el
valor del candidato máximo por encima del cual no probaremos ninguno más.

Esta mejora reducirá enormemente el número de candidatos que tenemos que probar para
factorizar un número.  Hagamos unas pruebas con la nueva versión y luego 
cuantificaremos esta reducción.


Pruebas de la version 1.3 

-Nivel 9
 1-Número compuesto múltiple
    455133121 = [139, 1237, 2647] In 0.0021 seconds
    370918413 = [3, 3, 3, 71, 181, 1069] In 0.0006 seconds

 2-Número compuesto por dos primos
    370918411 = [5441, 68171] In 0.0079 seconds

 3-Número primo
    370918423 = [370918423] In 0.0265 seconds
    469241039 = [469241039] In 0.0392 seconds
    540918487 = [540918487] In 0.0282 seconds

Nivel batido.  Estos resultados sí que suponen una reducción impresionante

-Nivel 10
 1-Número compuesto múltiple
    1569874542 = [2, 3, 47, 1063, 5237] In 0.0016 seconds
    6569874545 = [5, 13, 83, 1217771L] In 0.0051 seconds
    6569374545 = [3, 3, 5, 19, 7683479L] In 0.0115 seconds

 2-Número compuesto por dos primos
    2803249819 = [36523, 76753L] In 0.1846 seconds

 3-Número primo

    1569874541 = [1569874541] In 1271.9291 seconds
    3569874547 = [3569874547L] In 8839.9594 seconds.
    1569874541 = [1569874541] In 0.0774 seconds
    3569874547 = [3569874547L] In 0.2893 seconds

Nivel batido.  La mejora en tiempo es increible, por los tiempos obtenidos se observa
               una reducción en 100 mil veces con respecto a los tiempos obtenidos antes.

-Nivel 11
 1-Número compuesto múltiple
    25488769875 = [3, 5, 5, 5, 613, 110881L] In 0.0029 seconds 
 2-Número compuesto por dos primos
    25763162207 = [74699, 344893L] In 0.4127 seconds 
 3-Número primo
    24488769871 = [24488769871L] In 0.9026 seconds
    34488769921 = [34488769921L] In 0.8911 seconds

Nivel batido.

-Nivel 12
 1-Número compuesto múltiple
    569887462577 = [29, 181, 2591, 41903L] In 0.0133 seconds
 2-Número compuesto por dos primos
    537898651883 = [568783, 945701L] In 3.0829 seconds
 3-Número primo
    545687416927 = [545687416927L] In 4.0713 seconds

Nivel batido

-Nivel 13
 1-Número compuesto múltiple
    5456874516927 = [3, 107, 9133, 1861339L] In 0.0398 seconds
 2-Número compuesto por dos primos
    5160575927179 = [945701, 5456879L] In 6.1602 seconds
 3-Número primo
    5425687106863 = [5425687106863L] In 12.4455 seconds

Nivel batido.  Interesante, que el tiempo de factorización del número primo ha aumentado,
pero no se ha multiplicado por 10 como se esperaba sino solo por tres.

-Nivel 14
 1-Número compuesto múltiple
    45932156884361 = [11, 17, 5557, 44201279L] In 0.0321 seconds 
 2-Número compuesto por dos primos
    42619824616849 = [4328921, 9845369L] In 23.7017 seconds
 3-Número primo
    56083345812829 = [56083345812829L] In 41.4079 seconds

Nivel batido.

-Nivel 15
 1-Número compuesto múltiple
    560833458128296 = [2, 2, 2, 1300967, 53886211L] In 7.3137 seconds
 2-Número compuesto por dos primos
    460746856969877 = [9845369, 46798333L] In 56.3123 seconds
 3-Número primo
    536944873216931 = [536944873216931L] In 136.4375 seconds

Nivel batido.

-Nivel 16
 1-Número compuesto múltiple
    3644792236778694 = [2, 3, 101, 42473, 141607813L] In 0.2011 seconds
 2-Número compuesto por dos primos
    3849788417036503 = [59423701, 64785403L] In 368.5947 seconds
 3-Número primo
    5332147896211517 = [5332147896211517L] In 462.7662 seconds

Nivel batido.




CALCULO DEL CANDIDATO MÁXIMO

De la explicación anterior (ver Descarte de candidatos insensatos) se deduce la existencia
de un candidato máximo, más haya del cual nunca vamos a probar nuevos factores,
idependientemente de que el número que estemos factorizando sea primo o compuesto, en todo
caso si el número es compuesto el candidato máximo se reduce.  

Nos interesa conocer el valor de este candidato máximo, para calcularlo al principio del
programa y no tener que estar actualizando su valor por cada posible candidato que
probamos durante el proceso de factorización, con ello nos ahorraremos operaciones y
aumentaremos aun más la velocidad del programa.

Veamos la evolución de los primeros candidatos:

Cuando el candidato C=2 => el candidato máximo M_C=(número)/2
Cuando el candidato C=3 => el candidato máximo M_C=(número)/3
Cuando el candidato C=5 => el candidato máximo M_C=(número)/5

La condición que se comprueba en la aplicación es:

...
while candidate <= max_candidate:
...

De aquí se puede deducir la siguiente formula:
     C <= (número)/C
     C^2 <= número
     C <= sqrt(número)

Entonces nuestro candidato máximo es la raiz cuadrada del número a factorizar. La raiz
cuadrada de un número será en general un número con decimales, por lo tanto redondeamos la
formula por arriba, que finalmente queda:

    C <= sqrt(número) + 1

La raiz cuadrada de un número, en general, estará formada por otro número que tendrá la
mitad de cifras que el número original.  Por ejemplo la raiz cuadrada de un número de 8
cifras será un número de 4 cifras.  De aquí se deduce, si comparamos el metodo de la
versión 1.3 con el de versiones anteriores; que en el peor de los casos, cuando estemos
intentando factorizar un número primo, el problema se reduce al nivel del que hasta ahora
teníamos con un número con la mitad de cifras.  Por ejemplo la factorización de un número
primo de 10 cifras debe ser equivalente en la versión 1.3 a la factorización de un número
de 5 cifras en versiones anteriores.  



Comprobaciones innecesarias, mejora de rendimiento

En la versión 1.3.1 la lógica del programa no comprueba que el candidato ha superado el
límite por cada nuevo candidato que se prueba, sino una vez por cada decena; esto hace que
hagamos unas cuantas comprobaciones de candidatos innecesarias, como máximo 3, una vez que
ya hemos superado el límite; pero esto probablemente mejora el rendimiento del programa
para números grandes ya que la mayoría de las comprobaciones son negativas, es decir el
candidato no es mayor que el máximo; a menos comprobaciones más rápido es el programa.


Pruebas de la version 1.3.1

-Nivel 15
 1-Número compuesto múltiple
    560833458128296 = [2, 2, 2, 1300967, 53886211L] In 3.3503 seconds
 2-Número compuesto por dos primos
    460746856969877 = [9845369, 46798333L] In 23.171 seconds
 3-Número primo
    536944873216931 = [536944873216931L] In 57.6638 seconds

Nivel batido.  Me ha sorprendido que la mejora en el rendimiento sea tan grande,
reduciendose los tiempos a menos de la mitad.

-Nivel 16
 1-Número compuesto múltiple
    3644792236778694 = [2, 3, 101, 42473, 141607813L] In 0.1109 seconds
 2-Número compuesto por dos primos
    3849788417036503 = [59423701, 64785403L] In 149.1083 seconds
 3-Número primo
    5332147896211517 = [5332147896211517L] In 203.8097 seconds

Nivel batido.

-Nivel 17
 1-Número compuesto múltiple
    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.0144 seconds

 2-Número compuesto por dos primos
    32563672784171761 = [67894373, 479622557L] In 147.9295 seconds

 3-Número primo
    55641397544639089 = [55641397544639089L] In 612.2571 seconds

Nivel batido.

-Nivel 18

 1-Número compuesto múltiple
    954788612384655179 = [53077, 118429, 151894763L] In 0.2716 seconds
 2-Número compuesto por dos primos
    498542964342543929 = [652231511, 764365039L] In 1679.6016 seconds
 3-Número primo
    546698741123646019 = [546698741123646019L] In 1904.126 seconds

Nivel batido.  Es interesante ver como el tiempo necesario para factorizar un número primo
(3) o un número compuesto por dos primos del mismo nivel (2) es similar



¿Por qué es similar el tiempo de factorización de números (2) y (3)?

Vemos que los tiempos necesarios para factorizar números de los tipos (2) y (3) son del
mismo orden, salvo en el nivel 17, después veremos por qué la diferencia en este nivel.

La razón de que los tiempos sean similares es que el problema de factorización se ha
reducido en buscar un candidato dentro que como máximo puede tener el valor raiz cuadrada
del número a factorizar.  La raiz cuadrada, en general, será un número que tendrá la
mita de de las cifras que el número a factorizar.  

Por otra parte en el caso de los números (2) tenemos un número compuesto por dos primos de
similar cantidad de cifras, es decir es del orden de la raíz cuadrada del número a
factorizar.  Vemos pues que encontrar el menor factor en este caso es un problema similar
a llegar a máximo factor en el caso (3).  Cuando encontramos el menor de los factores, se
divide el número original entre este factor, y el nuevo número que tenemos que factorizar
tiene un nuevo máximo factor, que es del orden de su raiz cuadrada, y que es menor que el
último candidato probado, que además es el primer factor encontrado, con lo que tan pronto
como encontramos el primer factor se termina el proceso de factorización del número
compuesto.

El caso del nivel 17 es un tanto extremo: el número (2) está compuesto por dos factores,
uno de ellos de 8 cifras y el otro de nueve.  El proceso de factorización se termina al
encontrar el factor de 8 cifras.  Sin embargo en el caso de número (3) la raiz cuadrada
del número es del orden de 9 cifras, por lo tanto es normal que al tener una cifra más el
tiempo de factorización sea aproximadamente 5 veces más grande.



-Nivel 19
 1-Número compuesto múltiple
    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 0.3112 seconds
 2-Número compuesto por dos primos
    2537675226119470571 = [548997653, 4622379007L] In 1450.0095 seconds
 3-Número primo
    5977455832169755667 = [5977455832169755667L] In 6907.1926 seconds. (casi dos horas)

Nivel no superado.  En este nivel el tiempo se ha disparado a casi dos horas, y por lo
tanto se considera no superado.


