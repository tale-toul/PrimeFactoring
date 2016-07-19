## FACTORIZACION DE NUMEROS PRIMOS

Author: tale.toul@gmail.com

### INTRODUCCION

Vamos a desarrollar un proyecto software para solucionar el siguiente problema:
descomponer un número en sus factores primos.  La idea es simple, tenemos un número, que
debe ser entero, ya que la factorización solo tiene sentido en los enteros, que además
será positivo, aunque es posible factorizar números negativos no los vamos a tener en
cuenta; y lo vamos a descomponer en una serie números primos que al ser multiplicados
entre sí obtendremos el número original.  

`A = b * c * d * .... Siendo b,c,d números primos` 

Si el número a factorizar no se puede descomponer, esto quiere decir que es primo. Por si
alguien está despistado un número primo es aquel que solo es divisible por él mismo y por
1.

Para aclarar qué tipo de números vamos a tratar, estos siempre serán enteros positivos,
tanto los números que vamos a descomponer como los primos resultantes y los posibles
valores intermedios.  Las operaciones que realicemos siempre darán como resultado un
entero positivo, si no fuera así, por ejemplo en una división, el resultado de esta
operación se redondea o se descarta.


### ALCANCE

Como se ha dicho antes el problema es sencillo de acometer, buscar los factores de un
número o en su defecto determinar si este es primo es una tarea sencilla, fácil de
comprender y de programar, al menos inicialmente.  Sin embargo veremos que la dificultad
de obtener una solución correcta crece enormemente a medida que el número a factorizar se
hace más grande, hasta el punto en que veremos que es imposible resolverla en un tiempo
razonable.

Por lo tanto tenemos un problema sencillo de comprender y de atacar pero imposible de
solucionar a partir de cierto nivel.  Sin embargo no debemos desfallecer, Iremos
desarrollando el problema poco a poco desde un nivel básico inicial y pasando a niveles
superiores a medida que hayamos batido el desafío del nivel actual como si se tratará
de un videojuego de aventuras; veremos hasta donde somos capaces de llegar.


### DESCRIPCIÓN DEL PROCEDIMIENTO BÁSICO

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
   resultado de la división anterior, es decir 7.
3. Puesto que el resultó de la última división fue un entero continuamos probando el mismo
   factor, solo pasamos al siguiente cuando la división no devuelva un entero =>  7/2 =
   3.5  El resultado no es entero, luego se descarta.
4. Probamos el siguiente factor: 3 => 7/3= 2.333   El resultado no es entero y se
   descarta 
5. Probamos el siguiente factor: 4 => 7/4=1.75  No es entero se descarta
6. Probamos el siguiente factor: 5 => 7/5=1.4   No es entero se descarta
7. Probamos el siguiente factor 6 => 7/6=1.16     No es entero se descarta
8. Probamos el siguiente factor 7 => 7/7 = 1  El resultado es entero, pero hemos llegado
   al número que estábamos intentando factorizar, así que hemos terminado la busqueda y
   determinado que 7 es un factor primo.
9. El resultado final es que los factores primos de 14 son 2 y 7, de hecho 7 * 2=14



### ¿CÓMO SÉ QUE EL FACTOR QUE HE OBTENIDO ES UN NÚMERO PRIMO?

Cuando busco los factores de un número este puede ser divisible entre números que son
primos y otros que no lo son, ¿cómo puedo estar seguro que el factor que he encontrado es
un número primo?, por ejemplo el número 16 es divisible entre 2 que es primo, pero
también entre 8, que no lo es.  Ciertamente 8 es un divisor del número 16 y a su vez es
un número compuesto, pero usando la técnica descrita en el apartado anterior, empezando a
probar factores desde el número 2 e ir incrementando en uno cada vez, nos asegura que
antes de llegar a probar el número compuesto (8) como divisor, habremos probado los
factores de este, que necesariamente son menores que él, y por lo tanto si llegamos a
probar el número compuesto (8), el número a factorizar ya no será divisible entre él.
`16 = 2 * 2 * 2 * 2` no llegamos ni a probar el 8

Veamos otro ejemplo, en el que factorizamos el número 88 

1. 88/2 = 44 
2. 44/2=22 
3. 22/2=11 
4. ...
5. 11/8=1.375 (se descarta)
6. ...
7. 11/11=1 (fin)


### VERSION 1.0

La factorización de un número es un buen ejemplo de tarea adecuada para realizar con un
programa (software), es repetitiva e implica operaciones matemáticas, que son realizadas
muy rápidamente por un ordenador pero lentamente por una persona.

El procedimiento básico para factorizar un número es facil de programar, el funcionamiento
básico del programa es el siguiente:

1. Le pasamos el número a factorizar al programa como parametro

2. Creamos un bucle en el que al número a factorizar se le aplica la operación módulo
   contra el candidato a ser un factor `num%candidato`.  La operación módulo devuelve el
   resto de la división entre dos números, si el resto es cero el número es divisible por
   el candidato, lo que implica que es un factor de este; si el resto es distinto de cero
   el número no es divisible por el candidato y por lo tanto no es un factor de este.  

3. Si se encuentra un factor, se añade a la lista de factores, y el número a factorizar se
   divide por el factor, y el resultado será el que se use a partir de ahora como número a
   factorizar; se vuelve a probar el mismo candidato a factor sobre el nuevo número. 

4. Se incrementa en uno el candidato para probar el siguiente número y se vuelve a entrar
   en el bucle.

5. El bucle se repite hasta que el candidato a factor sea mayor que el número a
   factorizar.


#### Validación de resultados

Vamos a añadir algunos métodos para validar los resultados obtenidos por nuestro
programa.

En primer lugar usaremos una función para comprobar que los resultados obtenidos son
correctos.  Esta función es facil de implementar, se le pasa el número que hemos
factorizado y los factores que hemos encontrado; multiplicamos los factores entre sí y
debemos obtener el número a factorizar.  No vamos a comprobar si los factores son números
primos.

Un segundo método de validación consiste en tener una batería de pruebas conocida, un
conjunto de números primos con sus factores ya calculados, ejecutar el programa de tal
manera que lea la lista de números de la batería de pruebas y compare los resultados
obtenidos con los resultados de la batería.  Este método está pendiente de programar.


#### Pruebas

Vamos a ver hasta donde podemos llegar con esta versión del programa, probaremos a
factorizar números cada vez más grandes y veremos cuanto tarda el programa en obtener sus
factores.  
Nos interesan dos aspectos principales en el proceso: Obtener un resultado correcto al
factorizar el número; que el tiempo de resolución del problema (factorizar) sea razonable.

Definiremos varios parametros importantes:
+ El tamaño del número a factorizar.- Para cuantificar el número a factorizar
  consideraremos solo el número de cifras que lo componen y no el número concreto. El
  número de cifras determinará el nivel que hemos batido con nuestro programa.

+ El tiempo que tarde en ser factorizado.- La calidad de nuestro programa se mide por dos
  factores principales: que sea capaz de factorizar el número correctamente y que lo haga
  dentro de un tiempo razonable, definiremos un tiempo máximo para factorizar un número de
  una hora, y veremos hasta que nivel llegamos con este tiempo.  Al definir un tiempo
  máximo necesitamos un mecanismo que nos permita medir el tiempo que tarda el programa y
  otro que nos permita detener el programa y que este muestre por donde iba cuando se
  detuvo: los factores encontrados y hasta qué candidato ha probado.  Para poder comparar
  el tiempo que tarda nuestro programa en resolver cada factorización definiremos un
  hardware standard, este será un Raspberry Pi.

+ El tipo de número a factorizar.- Intentaremos factorizar varios tipos de números: al
  menos un número compuesto de más de dos factores; al menos un número compuesto por dos
  factores de tamaño similar (en cifras); al menos un número primo.  Cada uno de estos
  números tardará un tiempo distinto en ser factorizado, siendo el número primo el que más
  tarde con diferencia.



#### Generacion automática de casos de prueba

Para generar casos de prueba sin necesidad de introducirlos uno a uno voy a usar la
siguiente orden en una consola:

`# for x in {1..500}; do ./PrimeFactor.py --addtest testcases.dat -v $(python -c "import
random;print random.randint(1000000,9999999)"); done`

Esta orden esta compuesta por un bucle que se ejecutará 500 veces, dentro del bucle se
ejecuta el programa de factorización, y el número a factorizar es generado por un trozo de
código python, que genera un número aleatorio dentro del rango que se le indica.



#### Pruebas de la versión 1.0

Para estas pruebas usaremos como plataforma hardware un Raspberry Pi modelo B
revisión 1, con sistema operativo raspbian jessie

+ Nivel 1 
 En este nivel los números compuestos y los primos serán de una sola cifra, por no ser
 posible reducir el número de cifras en menos que uno.
 
 1. Número compuesto múltiple.- Solo existe un caso que podemos usar para un número
 compuesto por más de dos números primos, este es el 8=[2,2,2]
    8 = [2, 2, 2] In 0.000190019607544 seconds
 2. Número compuesto por dos primos.- Usaremos el 9=[3,3]
    9 = [3, 3] In 0.000190019607544 seconds
 3. Número primo.- 7=[7]
    7 = [7] In 0.000192880630493 seconds
 4. Adicionalmente guardaremos como casos de prueba todos los números interesantes de una
 cifra, desde el 1 al 9

 Nivel batido. Los tiempos de factorización son del orden de microsegundos. 


+ Nivel 2
 1. Número compuesto múltiple
    30 = [2, 3, 5] In 0.000200986862183 seconds
 2. Número compuesto por dos primos
    14 = [2, 7] In 0.000207901000977 seconds
 3. Número primo
    17 = [17] In 0.000205993652344 seconds
 
 Nivel batido. Los tiempos siguen siendo ridiculos

+ Nivel 3
 1. Número compuesto múltiple
    172 = [2, 2, 43] In 0.000254154205322 seconds
 2. Número compuesto por dos primos
    187 = [11, 17] In 0.000391006469727 seconds
 3. Número primo
    487 = [487] In 0.00111198425293 seconds
    683 = [683] In 0.00135493278503 seconds

 Nivel batido. Los tiempos de factorización suben al orden de los milisegundos.

+ Nivel 4
 1. Número compuesto múltiple
    4823 = [7, 13, 53] In 0.000292778015137 seconds
 2. Número compuesto por dos primos
    6523 = [11, 593] In 0.00151515007019 seconds
 3. Número primo
    4871 = [4871] In 0.008544921875 seconds
    5441 = [5441] In 0.00976800918579 seconds

 Nivel batido. 

+ Nivel 5
 1. Número compuesto múltiple
    16523 = [13, 31, 41] In 0.000253915786743 seconds
 2. Número compuesto por dos primos
    26233 = [37, 709] In 0.00139808654785 seconds
 3. Número primo
    27253 = [27253] In 0.0481271743774 seconds
    68171 = [68171] In 0.118710041046 seconds
 
 Nivel batido. El número del apartado dos, que tomaremos como referencia está todavía en
 el orden de los milisegundos.

+ Nivel 6
 1. Número compuesto múltiple
    372531 = [3, 23, 5399] In 0.00950002670288 seconds
 2. Número compuesto por dos primos
    332621 = [487, 683] In 0.00151205062866 seconds
 3. Número primo
    375643 = [375643] In 0.667051076889 seconds

Nivel batido. Seguimos en milisegundos para el número (2) pero estamos en más de medio
segundo para el número primo.

+ Nivel 7
 1. Número compuesto múltiple
    5577944 = [2, 2, 2, 19, 36697] In 0.064346075058 seconds
 2. Número compuesto por dos primos
    2713147 = [557, 4871] In 0.00906491279602 seconds
 3. Número primo
    5587943 = [5587943] In 9.97602105141 seconds

Nivel batido. Para los números (1) y (2) los tiempos siguen siendo bajas (centesimas y
milesimas de segundo, pero para el número (3) el tiempo a subido a casi 10 segundos, lo
que supone multiplicar por más de 10 el tiempo del número (3) del nivel 6.

+ Nivel 8
 1. Número compuesto múltiple
    12773543 = [29, 151, 2917] In 0.00515103340149 seconds
 2. Número compuesto por dos primos
    26503111 = [4871, 5441] In 0.0102159976959 seconds
 3. Número primo
    12763547 = [12763547] In 22.8130741119 seconds

Nivel batido. 

+ Nivel 9
 1. Número compuesto múltiple
    455133121 = [139, 1237, 2647] In 0.00713801383972 seconds
    370918413 = [3, 3, 3, 71, 181, 1069] In 0.00222587585449 seconds
 2. Número compuesto por dos primos
    370918411 = [5441, 68171] In 0.154046058655 seconds
 3. Número primo
    370918423 = [370918423] In 662.737498045 seconds 

Nive batido. Esta vez el caso (3) ha tardado algo más de 11 minutos, lo cual es un tiempo
considerable, pararemos las pruebas en este nivel y buscaremos alguna mejora en el
programa que reduzca el tiempo de cálculo.


    
### VERSION 1.1

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

Las versiones 1.1 y 1.2 han mejorado el rendimiento considerablemente, eliminando el 60%
de los candidatos a probar en el proceso de factorización: de cada decena eliminamos los
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



FACTORIZACION POR SECTORES


Candidato incial

La siguiente modificación que hacemos en el programa no está directamente relacionada con
una mejora en el rendimiento, por el contrario supondrá una ligerisima perdida del mismo.

Se trata de añadir un parámetro que nos permita indicar el candidato a partir del cual
queremos empezar a probar en la busqueda de factores.  Hasta ahora el programa siempre
empezaba probando candidatos a partir del 2, pero con esta opción podremos empezar a
probar en cualquier número entero arbitrario mayor o igual que 2.

La idea es simple, indico en la linea de comandos el candidato a partir del que quiero
empezar a buscar factores, por ejemplo:

 $./PrimeFactor.py -v 332621 -c 501

Implementar esta idea es, sin embargo, algo más complejo de lo que en un principio parece.
La función "factorize" esta inicialmente diseñada para empezar con el 2 como primer
candidato y a partir de ahí probar los siguientes en orden, de esta manera se prueba el
2, el 3, el 5, y a partir de ahí todos los números que acaben en 7, 9, 1 y 3, saltando
todos los números pares y terminados en 5, que no pueden ser factores primos.  Puesto que
ahora el primer candidato puede ser cualquier número hay que modificar sustancialmente la
lógica:

-Se mantiene la idea de probar solo números que pueden ser factores primos, es decir no
 probaremos números terminados en cifra par, ni terminados en 5.  Si un número es
 divisible por 2 y tambien por 8, pero el candidato inicial es 5, ni el 2 ni el 8
 aparecerán como factores, puesto que el 2 es menor que el primer candidato y el 8 queda
 excluido por ser número par.  

-Si el candidato inicial es menor o igual a 5, la lógica no cambia tanto, comprobamos
 en cada paso el valor del candidato: primero si es igual a 2, luego si es igual a 3,
 luego 4 y por último 5; de esta manera sea cual sea el valor inicial del candidato, el
 programa empezará a ejecutarse en el punto correcto.  Mención especial merece la
 condición en que el candidato inicial es 4, en este caso simplemente saltamos al
 siguiente valor (5) sin hacer nada.

-Si el valor del candidato inicial es mayor que 5, la función debe empezar a ejecutarse
 directamente en el bucle principal, y dependiendo de la cifra final del candidato los
 pasos se darán de una forma u otra. En la función original el bucle estaba pensado para
 que la primera vez que se entrara en el bucle principal, el número acabará en 7, después
 de tratar este candidato se sumaban +2 y el siguiente candidato acababa en 9, depues se
 sumanban +2 y el siguiente candidatos acababa en 1, despues se sumaban +2 y el siguiente
 candidato acababa en 3, y finalmente se sumanban +4 y el siguiente candidato acababa de
 nuevo en 7 y empezaba de nuevo el bucle.  Los incrementos seguían un patron fijo:
 +2,+2,+2,+4.  Pero con la nueva versión de la función si el primer candidato termina en
 un número distinto a 7 el patron de incremnetos cambia.  Para solucionar este problema
 se define un diccionario que tendrá como clave la última cifra del candidato que entra
 en el bucle por primera vez y como valor una lisa con los incrementos en el orden
 correcto en que se deben ejecutar.  Según la cifra en que termine el candidato inicial
 se seleccionará una lista de incrementos u otra, por ejemplo si el candidato inicial
 termina en 3, los incrementos serán: (3) +4 (7) +2 (9) +2 (1) +2 (3) ó [4,2,2,2].  Ahora
 el incremento que se aplica, en lugar de una constante, es un valor de una lista
 (candidate += increment[1]) esto es lo que hace que el programa se ralentice un poco con
 respecto al uso de una constante. He probado a usar una "tuple" en lugar de una lista
 pero esto ralentiza aun más el programa.

-También hay que tener en cuenta que el valor del candidato inicial pueda terminar en una
 cifra par o en 5, en cuyo caso debemos incrementar el valor del candidato hasta el
 siguiente número que termine en 1,3,7 ó 9, que son los únicos finales de candidatos
 válidos.  Esto se consigue con un bucle if que comprueba la cifra final del candidato, 
 si termina en alguno de las cifras "prohibidas" lo actualiza hasta el siguiente número
 válido.  Si por el contrario usa una terminación válida no hace nada.


Candidato final

Otra mejora en la aplicación es la posbilidad de indicar el candidato final hasta el que
queremos buscar factores.  Añadimos la posibilidad de usar un argumento de linea de
comandos para asignar el valor máximo que puede tener el candidato en la busqueda de
factores del número.  Esta opción del programa resulta ser sencilla de implementar.

Con esta opción los candidatos se irán probando hasta que el candidato sea mayor que el
candidato máximo posible, como hasta ahora, con la diferencia que este máximo pude ser
uno de dos valores posible:

-La raiz cuadrada del número a factorizar
-El candidato máximo indicado en linea de comandos

Usaremos el menor de los dos valores anteriores.

El candidato final debería ser mayor que el candidato inicial, sin embargo no lo
comprobamos explicitamente, la lógica del programa hace que si el candidato final es
menor que el inicial, la factorización termine inmediatamente. Salvo en el extraño caso
en que el primer y último candidato sean menor que 5, en cuyo caso si se podria probar
alguno de los candidatos menores, por ejemplo:  

    $./PrimeFactor.py -v 64795512344765945 -c 4 -l 2
    Factors of 64795512344765945 = [5, 12959102468953189] In 0.0 seconds


Factores NO primos

Al poder seleccionar un segmento arbitrario dentro del cual buscar los factores del número,
no podemos garantizar que los factores encontrados sean números primos, ya que no hemos
probado todos los candidatos desde el inicio, o sea a partir del 2.  Es completamente
posible que uno o más de los factores encontrados dentro del segmento de candidatos sean
números compuestos, que son factores del número inicial pero no son números primos.  Por
ejemplo:

    $ ./PrimeFactor.py -v 3644792236778694 -c 120 
    Factors of 3644792236778694 = [303, 42473, 283215626] In 0.0036 seconds

El número 303 es un factor pero no es primo, es divible entre 3, que es un factor primo
del número original.



MEJORA EN EL HARDWARE

En la última modificación al programa no se consiguio ninguna mejora en la velocidad, si
acaso un ligero empeoramiento.  Vamos a aplicar una mejora, que esta vez no implia tocar
el código.

Hasta ahora estabamos utilizando como plataforma hardware un Raspberry Pi modelo B, ahora
vamos a pasar a utilizar un Raspberry Pi 3 modelo B.  Esperamos que haya una mejora en el
rendimiento, veremos de qué magnitud.


Pruebas en el RPi 3

-Nivel 16
 1-Número compuesto múltiple
    3644792236778694 = [2, 3, 101, 42473, 141607813L] In 0.027 seconds
 2-Número compuesto por dos primos
    3849788417036503 = [59423701, 64785403L] In 39.324 seconds
 3-Número primo
    5332147896211517 = [5332147896211517L] In 49.0334 seconds

Nivel batido. Vemos que se ha reducido el tiempo a una cuarta parte del que teníamos con el anterior hardware

-Nivel 17
 1-Número compuesto múltiple
    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.0039 seconds
 2-Número compuesto por dos primos
    32563672784171761 = [67894373, 479622557L] In 45.8701 seconds    
 3-Número primo
    55641397544639089 = [55641397544639089L] In 158.3416 seconds    

Nivel batido.


-Nivel 18

 1-Número compuesto múltiple
    954788612384655179 = [53077, 118429, 151894763L] In 0.0768 seconds
 2-Número compuesto por dos primos
    498542964342543929 = [652231511, 764365039L] In 452.1801 seconds
 3-Número primo
    546698741123646019 = [546698741123646019L] In 507.4415 seconds    

Nivel batido.  Igual que en los anteriores el tiempo se reduce aproximadamente a un cuarto

-Nivel 19
 1-Número compuesto múltiple
    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 0.0827 seconds
 2-Número compuesto por dos primos
    2537675226119470571 = [548997653, 4622379007L] In 384.9777 seconds
 3-Número primo
    5977455832169755667 = [5977455832169755667L] In 1825.4157 seconds. (media hora aproximadamente)

Nivel batido. Hemos conseguido batir este nivel, al reducir casi 1/4 el tiempo
que se necesito con el anterior hardware. Sin embargo es evidente que no
seremos capaces de superar el siguiente nivel.

 

DIVIDIENDO EL PROBLEMA EN SEGMENTOS

Versión 2.1.x

Con el nuevo hardware la velocidad del programa ha mejorado mucho, sin embargo aun estamos
desperdiciando gran parte de la capacidad del hardware.  El programa se ejeucta en una
sola de las 4 CPUs que tiene el RPi 3, por lo tanto estamos desperdiciando la potencia de
esas 3 restantes CPUs.

Antes de llegar a ejecutar la factorización en paralelo entre las CPUs del computador voy
a definir una nueva función (factor_broker) que, en base al espacio del problema y al
número de CPUs de la máquina, genera una serie de segmentos dentro de los cuales buscaremos
los factores del número.

El espacio del problema viene delimitado por los enteros que se encuentran entre el
candidato mínimo y el máximo, estos valores pueden venir de la linea de comandos o ser
calculados.  Este espacio se divide entre el númeor de CPUs y el valor obtenido y
redondeado se utiliza para crear los segmentos donde se buscarán los factores.  Por
ejemplo si el candidato mínimo es 2 y el máximo es 1025, y el número de CPUs es 4:

    1025/4=256.25 => incremento = 257

    Segmento1=(2,259)
    Segmento2=(260,517)
    Segmento3=(518,775)
    Segmento4=(776,1033)

Vemos que el límite superior del último segmento se pasa del valor del candidato máximo,
sin embargo la diferencia no supondrá apenas perdida de rendimiento, ya que la diferencia
es muy pequeña.

Una vez que tenemos los segmentos definidos ejecutamos la función que ya teníamos
factorize_with_limits para buscar factores dentro de ese segmento.

El problema que nos encontramos con esta forma de dividir el problema de factorización es
que cuando buscamos factores en un segmento distinto del primero, no podemos estar seguros
que los factores encontrados sean números primos, por debemos filtrar los factores encontrados en
cada segmento para eliminar los factores compuestos.

Para "limpiar" las listas de factores obtenidas de los distintos segmentos creamos una
nueva función de factorización (factorize_with_factors) a la que se le pasa el número a
factorizar y una lista de candidatos, que previamente hemos construido añadiendo todos los
factores obtenidos en los distintos segmentos.  Se eliminan los duplicados de la lista y
se ordena, a continuación usamos los elemetos de esa lista como candidatos a factorizar el
número compuesto.  Puesto que empezamos por los más pequeños, que probablemente son
primos, cuando lleguemos a otro mayor que esté compuesto por el producto de primos
anteriroes, el número resultante de la factorización ya no será divisible por este
candidato compuesto.  Por ejemplo, el número 60 se divide en los siguientes segmentos:

60
segments [(2, 4), (5, 7), (8, 10), (11, 13)]

Y los factores encontrados en cada segmentos son:

[2, 2, 3, 5],   [5, 12],  [60],   [60]

Cuando volvemos a factorizar el número con los candidatos:

[2, 2, 3, 5, 12]

El 12 no llegaremos ni a probarlo por ser menor que el candidato máximo, que se actualiza
tras cada factor.

Otro ejemplo: el número 1690

Los segmentos son:

segments [(2, 12), (13, 23), (24, 34), (35, 45)]

Y los factores encontrados en cada segmentos son:

[2, 5, 13, 13],   [13, 13, 10],   [1690],   [1690]

Cuando se prueban de nuevo estos factores, y llegamos al 10, antes hemos dividido el
número entre 2 y 5, por lo tanto el número resultante cuando llegamos al factor 10, no es
divisible por éste, y no es considerado como factor válido, aunque sí lo era cuando se
factorizo en el segmento (13,23)


Rendimiento

Este cambio en el funcionamiento del programa implica una caida en el rendimiento del
programa, que varía según el número que estemos factorizando:

-En el caso de los números de tipo (1) la perdida de rendimiento es enorme, mientras que
antes por cada factor que encontrabamos el problema de factorización se reducía y
convergía rapidamente, ahora buscamos factores en todos los segmentos, es decir en todo el
espacio de candidatos independientemente de si se han encontrado factores en otros
segmentos anteriores, y esto ralentiza la finalización del programa.

Por ejemplo en el nivel 17 la diferencia entre el tiempo obtenido antes y ahora es de más
de 2 minutos:


-Nivel 17
 1-Número compuesto múltiple
    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.0039 seconds

    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 126.8963 seconds

-En el caso de los números de tipo (2) la perdida de rendimiento es menor, aunque tambien
es grande.  En este caso solo hay que encontrar un factor y dependiendo del segmento en el
que se encuentre se ralentizará más o menos la finalización del programa, de nuevo en el
nivel 17:

-Nivel 17
 2-Número compuesto por dos primos
    32563672784171761 = [67894373, 479622557L] In 45.8701 seconds

    32563672784171761 = [67894373, 479622557L] In 107.6737 seconds

-Los números de tipo (3) son los menos afectados por la pérdida de rendimiento, ya que no
hay factores y hay que recorrer todo el espacio de candidatos para finalizar el programa,
una vez más en el nivel 17:

-Nivel 17
 3-Número primo
    55641397544639089 = [55641397544639089L] In 158.3416 seconds

    55641397544639089 = [55641397544639089L] In 160.6151 seconds

En sucesivas versiones nos basaremos en el trabajo de esta versión para conseguir mejoras
en el rendimiento del programa.




EJECUCIÓN PARALELA DE LOS SEGMENTOS

En la versión 2.1.1 vamos a aprovechar la división en segmentos del problema para ejecutar
la factorización dentro de cada uno de ellos de forma paralela.  Con la ejecución paralela
aprovechamos mejor el hardware de la máquina, y veremos que en esta primera versión y
según el tipo de número a factorizar, el rendimiento del programa puede mejorar o
empeorar.

Puesto que tenemos el problema bien delimitado en segmentos independientes podemos
ejecutar la factorización en cada segmento como un proceso independiente de los demás y al
final recopilar y filtrar los resultados.

Para ejecutar varios procesos en paralelo se utiliza el modulo python "multiprocessing" y
la función que se ejecutará como proceso independiente será factorize_with_limits.
Algunas de las modificaciones importantes a esta función son:

-Cada proceso independiente debe guardar sus resultados en un almacenamiento común a todos
los procesos, para ello utilizamos un objeto de tipo multiprocessing.Queue que gestiona
los accesos concurrentes sin provocar inconsistencias.  Por lo tanto en la llamada a la
función factorize_with_limits se incluye la cola común como un nuevo parametro.  Al final
de la función, los factores encontrados se añaden a la cola.

-Al guardar los resusltados en la cola se elimina la linea "return" que devolvía los
factores encontrados en el segmento.

-Los procesos independientes no pueden recibir señales externas, por lo que se elimina el
tratamiento de las mismas de la fución. 

Los procesos independientes se lanzan desde la fucnión factor_broker, donde se define la
cola para guardar los resultados.  Aquí se crean tantos procesos como CPUs tiene la
máquina, se guardan en una lista y se lanza su ejecución.  A continuación se espera a que
terminen todos los procesos usando el metodo join(), de lo contrario el programa
continuaría adelante sin esperar a los resultados obtenidos de los procesos de
factorización.

Cuando todos los procesos han terminado se lee la cola de resultados y se mandan a la
función clean_results que devuelve solo los factores primos.



Pruebas de rendimiento
v 2.2

-Nivel 17
 1-Número compuesto múltiple
    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.0039 seconds

    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 44.0142 seconds
 2-Número compuesto por dos primos
    32563672784171761 = [67894373, 479622557L] In 45.8701 seconds    

    32563672784171761 = [67894373, 479622557L] In 32.5388 seconds
 3-Número primo
    55641397544639089 = [55641397544639089L] In 158.3416 seconds 
    
    55641397544639089 = [55641397544639089L] In 47.3305 seconds   

-Nivel batido.  En el número compuesto (1) el rendimiento ha empeorado; en el número
compuesto (2) a mejorado un poco; sin embargo en el número primo (3) ha mejorado mucho, se
ha dividido por 4 el tiempo necesario para determinar que el número es primo.

-Nivel 18

 1-Número compuesto múltiple
    954788612384655179 = [53077, 118429, 151894763L] In 0.0768 seconds

    954788612384655179 = [53077, 118429, 151894763L] In 173.0106 seconds
 2-Número compuesto por dos primos
    498542964342543929 = [652231511, 764365039L] In 452.1801 seconds

    498542964342543929 = [652231511, 764365039L] In 145.8587 seconds
 3-Número primo
    546698741123646019 = [546698741123646019L] In 507.4415 seconds  
    
    546698741123646019 = [546698741123646019L] In 181.5399 seconds  

Nivel batido.  En este caso la resolución del número de tipo (1) tarda mucho más, pero las
resoluciones de los números de tipo (2) y (3) son más rápidas.

-Nivel 19
 1-Número compuesto múltiple
    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 0.0827 seconds

    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 357.5535 seconds
 2-Número compuesto por dos primos
    2537675226119470571 = [548997653, 4622379007L] In 384.9777 seconds

    2537675226119470571 = [548997653, 4622379007L] In 335.733 seconds
 3-Número primo
    5977455832169755667 = [5977455832169755667L] In 1825.4157 seconds. (media hora aproximadamente)

    5977455832169755667 = [5977455832169755667L] In 685.0041 seconds

Nivel batido. 

A estas alturas es evidente que el rendimiento de esta versión es mejor en el caso (3),
peor en el caso (1) y similar en el caso (2).  Hay que mejorar la lógica del programa.


¿Por qué es peor el rendimiento en los números compuestos por varios factores?

La razón es que cuando un número está compuesto por varios factores, a medida que vamos
encontrando dichos factores el número a factorizar se reduce muy rapidamente y por lo
tanto el problema se resuelve en poco tiempo.  

Esto funciona muy bien cuando usamos un método secuencial para solucionar el problema,
pero cuando usamos un método paralelo la reducción del número a factorizar está delimitada
dentro del segmento de factorización.  Si por ejemplo todos los factores de un número
están dentro del primer segmento, la factorización de ese primer segmento terminará muy
rápido, pero el resto de segmentos recorreran todo el espacio de candidatos sin encontrar
ningún factor.  Por lo tanto la factorización total tardará tanto como la factorización del
segmento más lento, que será el que tenga menos (nigún) factores en él.



PARALELISMO SECUENCIAL
Branch 2.2

Para evitar el problema de la lentitud de factorización en los números compuestos por
múltiples primos vamos a definir un método que tenga en cuenta la finalización de los
segmentos de forma secuencial desde el primero.

La idea es que a medida que vayan terminando los procesos de factorización vayamos
reevaluando si la factorización ya se ha completado, y si no es así, la posibilidad de que
el candidato máximo se haya reducido, lo cual ocurre si se han encontrado factores primos
en el proceso recien terminado.

Es importante que estas comprobaciones se hagan en orden secuencial desde el primer
segmento en adelante, ya que si el proceso que gestiona el tercer segmento termina antes
que los que gestionan los segmentos 1 y 2, no puedo asegurar que los factores encontrados
en el tercer segmento sean primos, ni que los segmentos 1 y 2 no contengan otros factores.

El funcionamiento es el siguiente:

Supongamos que tenemos 4 procesos, cada uno buscando factores primos en una cuarta parte
del espacio de posibles factores.

-Cuando el primer proceso de factorización termina, si el último candidato que se ha
 probado es mas grande que el candidato máximo posible para el número a factorizar,
 entonces marcamos el proceso total de factorización como completado y se termina el
 programa.

-Si al terminar el primer proceso no se ha terminado la factorización pero sí se ha
 encontrado algún factor, sabemos que estos factores son primos y que el número
 resultante de dividir el número original entre los factores encontrados es menor que el
 original y por lo tanto es más facil y rápido de factorizar.  
 
 Entonces vamos a parar el segundo proceso y relanzarlo con nuevos valores.

 Se bloquea el segundo proceso con un "lock" que le impide actualizar el número a
 factorizar, añadir nuevos factores encontrados, modificar el candidato máximo para el
 proceso o acabar su operación (salir), pero no le impide continuar probando candidatos.

 Luego, por razones técnicas relacionadas con la combinación de python y linux, tengo que
 ejecutar una orden join para permitir que el segundo proceso termine ordenadamente si ya
 había concluido su trabajo.  Esta como esperando que le habran la puerta para salir.

 Después de darle la oportunidad de acabar ordenadamente, compruebo si el proceso aun está
 vivo, si es así le envío una señal asincrona para obtener el valor del último candidato
 probado.

 Espero a que la funcion asociada a la señal asíncrona se ejecute, esto se controla con un
 objeto de tipo "Event", y entonces mato el proceso 2.

-A continuación construimos un nuevo proceso 2 con los valores actualizados: un nuevo
 número a factorizar y un nuevo candidato inicial.  El candidato final se mantiene igual,
 y dentro del proceso se calculará un nuevo candidato máximo a partir del nuevo número a
 factorizar. Si este proceso había encontrado algún factor lo mantengo en la lista de
 factores del proceso a relanzar.

Cuando el segundo proceso termina repetimos el proceso con respecto al tercero, y cuando
el tercero termina lo repetimos con respecto al cuarto.  Cuando el cuarto termina, si es
que hemos llegado tan lejos se ha completado la factorización.

Dado que el número de segmentos es muy pequeño, puesto que equivale al número de
cores/cpus de la máquina, esta mejora de "paralelismo secuencial" solo supone una ventaja
en casos muy particulares.  Lo más probable es que los factores se encuentren en uno solo
de los segmentos y que este sea el primero, en cuyo caso la factorización terminará
rápido.  Si hay factores en segmentos superiores, estos segmentos terminarán antes que
los inferiores, por ser los factores mayores y al dividir el número a factorizar el
problema en este segmento se reduce más rápido.





### ATOMIZADO DEL PARALELISMO
**Versión 2.3**

Para aprovechar mejor el código del paralelismo secuencial vamos a dividir el problema en
un número mayor de segmentos.  Al haber más segmentos, estos serán más pequeños, la
busqueda dentro de ellos terminará más rápido, y podremos aprovechar mejor la potencia de
la máquina en factorizaciones de números grandes.

Por ejemplo si tenemos 10 segmentos, y en el segmento 5 encontramos un factor que al
dividir al número a factorizar nos da un resultado que está por debajo de cadidato máximo
global, esto implica que a partir de este segmento la factorización ha concluido, por lo
tanto los segmentes del 5 en adelante se dan por procesados, y solo quedarían pendientes
los segmentos del 1 al 4.

Una cuestión que surge es ¿Que tamaño deben tener los segmentos?.  Dependiendo de la
potencia de la máquina estos tendrán un tamaño distinto.  Para una máquina más potente
los segmentos serán mayores, y para una menos potente serán menores.

Para calcular el tamaño de los segmentos hacemos lo siguiente:

-En primer lugar lanzamos un proceso de factorización sobre el espacio completo de
 candidatos, que se ejecutará por un tiempo determinado, definible por el usuario, por
 ejemplo 10 segundos.  Si la factorización se ha completado en este tiempo, el programa
 termina. Si no se ha completado calculamos los candidatos procesados en esta primera
 fase, los que quedan por procesar hasta finalizar la factorización, dividimos los que
 quedan por procesar entre los ya procesados y obtengo un posible número de segmentos.
 Si este número supera al máximo definido en el programa, por ejemplo 100, calculamos un
 multiplicador para aumentar el tamaño del segmento de tal manera que el número de
 segmentos quede cerca del número máximo permitido.  Finalmente se generan los
 segmentos, y si en la primera fase se ha encontrado algún factor se obtiene el nuevo
 número a factorizar.
 
-Una vez definidos los segmentos, creamos un proceso de factorización por cada una de las
 CPUs que tiene la máquina, tomando un segmento de candidatos de la lista para cada
 proceso, y los lanzamos.  El proceso principal (padre) esperará a que termine cualquiera
 de los procesos de factorizacion.  

-Cuando un proceso de factorización termina, informa al padre, que comprueba si este
 proceso ha revisado hasta el máximo candidato posible, no solo en su segmento sino a
 nivel global del problema total.  Si es así se eliminan de la lista todos los segmentos
 superiores al que se asignó a este proceso, y se matan los procesos que están trabajando
 en segmentos superiores.  Una vez terminado un proceso de factorización, si aun quedan
 segmentos por procesar, se crea un nuevo proceso de factorización sobre uno de estos
 segmentos y se lanza.



#### Comunicación entre padre e hijos (Condiciones)

Para que el proceso padre se entere de cuando ha terminado un hijo, y pueda lanzar otro
nuevo, se utiliza una variable de tipo _multiprocessing Condition_.  Este tipo de
variable es una combinación de _Event_ y _Lock_, tienen un Lock que es necesario adquirir
antes de realizar otras operacines y tiene un metodo notify que sirve para avisar a otros
procesos.

En este caso, el proceso padre, desde la función `factor_broker`, crea un objeto de tipo
Lock que usa para crear un objeto de tipo Condition, este objeto Condition es compartido
por todos los procesos, padre e hijos.

El padre adquiere el Lock del objeto _Condition_ llamando a su método acquire, entonces crea
el primer grupo de procesos hijo (factorizadores) y libera el Lock llamando al metodo
wait.  Esta llamada no solo libera el Lock sino que detiene la ejecución del proceso padre
a la espera que de alguno de los hijos llame al método notify. 

Cuando alguno de los hijos llega la final de su "tarea" intenta adquirir el Lock del
objeto Condition, si no puede hacerlo se quedará esperando hasta que quede liberado por el
proceso que lo tenga, si por el contrario lo puede adquirir, ejecutará algunas últimas
ordenes y notifica al resto de procesos llamando al metodo notify; esta llamada provoca en
los procesos que estan esperando, que despierten e intenten adquirir el Lock, que unos
instantes depues es liberado por el mismo proceso que ha ejecutado notify, llamando al
metodo release.  

Lo ideal sería que el proceso padre fuera siempre el primero en ser notificado y
adquiriera el Lock, sin embargo es muy probable que otro proceso hijo se
adelante.  Como consecuencia de esto, cuando por fin el proceso padre adquiere el Lock de
la condición, puede que haya más de un proceso hijo que ha terminaod y por lo tanto la
busqueda de procesos finalizados no puede terminar en cuanto encontramos el primero.  Lo
que hacemos es recorrer la lista de procesos en ejecución y guardar aquellos que aun están
ejecutandose en otra lista temporal, los que no copiemos serán borrados por el recolector
de basura.  Cuando se ha recorrido toda la lista y tenemos todos los procesos en ejecución
en la lita temporal, copiamos esta sobre la lista de procesos en ejecución.  Esta es una
forma efectiva de recorrer una lista y modificarla, ya que no es seguro recorrer una única
lista y eliminar elementos intermedios de esta.


#### Validación de resultados 
**Versión 2.3.4**

Además de comprobar que el producto de los factores obtenidos da como resultado el número
original, se utiliza el módulo [gmpy2](https://gmpy2.readthedocs.io/en/latest/) para
comprobar que cada uno de los factores es probablemente un número primo:

`if gmpy2.is_prime(item):`


#### Debilidades del modelo v2.3


El modelo basado en multiples segmentos de pequeño tamaño que se ejecutan en paralelo
tiene un problema, y es que para aprovechar al máximo las CPUs de la máquina no esperamos
que los procesos terminen en orden secuencial, como hacíamos hasta ahora, sino que en
cuanto un proceso en ejecución termina, lanzamos otro nuevo sin esperar que terminen
los que viene antes, según el orden de segmentos de factorización.  

Si el proceso que termina no ha encontrado factores no hay problema, pero si se ha
encontrado algún factor se nos presenta una situación complicada.  Si este proceso no es
el primero en el conjunto de procesos en ejecución, no podemos asegurar que los factores
encontrados sean números primos.  Si el proceso no ha revisado hasta el máximo candidato
posible a nivel global, debemos seguir factorizando los segmentos posteriores, pero puesto
que hemos encontrado algún factor, el número a factorizar debe ser el resultado de
dividir el número original entre los factores encontrados, esto es bueno porque se reduce
el problema para los procesos y segmentos posteriores.  Por otra parte para los posibles
procesos anteriores el número a factorizar debe seguir siendo el original, puesto que el
factor encontrado en el proceso "no ordenado" puede no ser primo.

Por lo anterior se deduce que debemos lanzar los procesos de forma secuencial ordenada, y
en ningún caso aleatoria.  Por ejemplo si tenemos 10 segmentos estos deben ser procesados
del 1 al 10 en orden ascendente.  Si por ejemplo la máquina tiene 4 CPUs, tendremos 4
procesos ejecutandose al mismo tiempo, y el proceso 3 termina antes que los procesos 1 y
2, el nuevo proceso que debo lanzar será el 5, y luego el 6 y así sucesivamente.  Esto
evitará que se produzcan problemas relacionados con distintos numeros a factorizar según
el segmento que estemos revisando.

El escenario que daría problemas con este modelo sería el que se produciría en el caso de
lanzar los procesos de factorización de forma aleatoria sobre el espacio de segmentos.
Por ejemplo para 10 segmentos y 2 CPUs, si procesamos los segmentos 1 y 5, y el segmento
5 termina habiendo encontrado un factor X y el nuevo número a factorizar resultante es Y;
para los segmentos del 6 al 10 (o hasta el que se llegue según los segmentos que defina
el nuevo número Y) el nuevo número a factorizar es Y, pero para los segmentos del 2 al 4
el número a factorizar debería ser X ó el número original.  Si ahora lanzo un proceso de
factorización sobre el segmento 3 y este termina habiendo encontrado factores de nuevo
tengo un número a factorizar distinto según el segmento sobre el que busque factores sea
mayor o menor que el segmeto 3.


Pruebas con la versión 2.3.3

-Nivel 16
 1-Número compuesto múltiple
    3644792236778694 = [2, 3, 101, 42473, 141607813L] In 0.027 seconds

    3644792236778694 = [2, 3, 101, 42473, 141607813L] In 0.1581 seconds
 2-Número compuesto por dos primos
    3849788417036503 = [59423701, 64785403L] In 39.324 seconds

    3849788417036503 = [59423701, 64785403L] In 21.8403 seconds
 3-Número primo
    5332147896211517 = [5332147896211517L] In 49.0334 seconds

    5332147896211517 = [5332147896211517L] In 22.9942 seconds

Nivel batido

-Nivel 17
 1-Número compuesto múltiple
    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.0039 seconds

    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.1259 seconds
 2-Número compuesto por dos primos
    32563672784171761 = [67894373, 479622557L] In 45.8701 seconds    

    32563672784171761 = [67894373, 479622557L] In 22.0377 seconds
 3-Número primo
    55641397544639089 = [55641397544639089L] In 158.3416 seconds    

    55641397544639089 = [55641397544639089L] In 67.2372 seconds

Nivel batido


-Nivel 18

 1-Número compuesto múltiple
    954788612384655179 = [53077, 118429, 151894763L] In 0.0768 seconds

    954788612384655179 = [53077, 118429, 151894763L] In 0.2071 seconds
 2-Número compuesto por dos primos
    498542964342543929 = [652231511, 764365039L] In 145.8587 seconds

    498542964342543929 = [652231511, 764365039L] In 163.3792 seconds
 3-Número primo
    546698741123646019 = [546698741123646019L] In 163.37 seconds

    546698741123646019 = [546698741123646019L] In 172.9918 seconds

Nivel batido.


-Nivel 19
 1-Número compuesto múltiple
    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 357.5535 seconds

    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 0.2086 seconds
 2-Número compuesto por dos primos
    2537675226119470571 = [548997653, 4622379007L] In 335.733 seconds

    2537675226119470571 = [548997653, 4622379007L] In 136.3474 seconds
 3-Número primo
    5977455832169755667 = [5977455832169755667L] In 685.0041 seconds

    5977455832169755667 = [5977455832169755667L] In 558.3124 seconds

Nivel batido.


-Nivel 20
 1-Número compuesto múltiple
    59774558321697556676 = [2, 2, 23, 2069, 314027771879387L] In 11.8885 seconds

 2-Número compuesto por dos primos
    36579649644065170163 = [5568743671L, 6568743653L] In 1434.5462 seconds
    25841129207805312677 = [3526889461L, 7326889457L] In 884.3702 seconds (casi 15 min.)

 3-Número primo
    52369844786321568503 = [52369844786321568503L] In 1845.6705 seconds (30 minutos aprox.)

Nivel batido.  Con las mejoras introducidas en esta versión 2.3 el rendimiento vuelve a
 mejorar mucho en los números de tipo (1), ya que si un proceso completa la factorización
 del número no se espera a que los demas procesos terminen, se los mata.  
 
 En los números de tipo (2) puede mejorar o mantenerse similar, pero no empeorar; esto se
 debe a que el proceso de factorización termina cuando se encuentran los factores primos,
 y no hay que esperar a que acaben los otros procesos paralelos; dependiendo de lo pronto
 que se encuentren los factores así de rápida será la factorización.  
 
 En lo números de tipo (3) el tiempo de factorización no cambia sustancialmente, ya que
 aquí hay que recorrer todo el espacio de candidatos.



### PARALELISMO ALEATORIO
**Version 2.4**

En esta versión vamos a procesar los segmentos de forma aleatoria, en lugar de
secuencial.  Se definen dos partes en la factorización claramente diferenciadas: _fase 1_;
_fase general_

+ **fase 1**.- En esta fase se recorre el primer grupo de candidatos, durante un tiempo
  determinado; si se encuentran factores, se guardan como definitivos.  Si no se ha
  terminado la factorización en esta fase se define el conjunto de segmentos en que se
  devide el espacio de candidatos.
+ **fase general**.- En esta fase se procesan los segmentos en busqueda de factores de
  forma aleatoria, ya no es necesario procesar los segmentos de forma secuencial.  En
  cuanto se encuentra un factor se detiene la factorización y el factor encontrado junto
  con el resultado de dividir en número entre el factor se guardan en una lista de
  elementos a factorizar.
  
La factorización _paralela aleatoria_ no necesariamente supone una mejora en el
rendimiento de la aplicación.  Cada vez que factoricemos un número, y este supere la fase
1, el tiempo que tarde en factorizarse dependerá del orden en que se hayan procesado los
segemtos, es decir en genral el tiempo de factorización será distinto en cada ejecución de
la factorización; a no ser que el número sea primo, en cuyo caso la factorización deberá
recorrer todos los segmentos y el tiempo será el mismo en cada ejecución. 


#### Requisitos de esta versión

+ Los factores que se encuentren en la fase 1 se guardan como factores primos, es decir
  factores definitivos.
+ Cuando se encuentre un factor fuera de la fase 1 comprobaremos cuantas veces divide al
  número a factorizar pero solo guardaremos una copia del factor.  Esto se hace así para
  que no se factorice dos veces un mismo factor 
+ Tan pronto como se encuentre un factor fuera de la fase 1, se detiene la factorización y
  se guardan en una cola dos nuevos números a factorizar: el factor encontrado y el
  resultado de divivir el número a factorizar entre el factor encontrado.
+ El candidato inicial para un nivel de factorización se actualizará tras la finalizacón
  de la fase 1 y tras la finalización de un segmento que esté al principio de la lista (el
  más bajo).  Este requisito y el siguiente puede que no merezca la pena incluirlo debido
  a que la ganancia al econtrar factores en la fase general supera con creces la de
  actualizar el candidato inicial, sin embargo la complejidad en la modificación de la
  aplicación para añadir este requisito es grande.
+ Cada candidato encolado, se guardará junto con su valor de candidato mínimo a partir del
  cual buscar factores.  El valor del candidato mínimo es facil de obtener, es el menor
  valor de menor segmento en la lista de segmentos pendientes de procesar.
+ The mission acomplished concept makes no sense anymore: either you found a factor and
  the segment processing is done, or you didn't and the segment processing continues.
  Just store with the primer factors the number to factor remaining when all segments have
  been processed.
+ In this version the option to pass the segments in the command line has to be removed to
  make sure the phase 1 is executed.


#### Pruebas de la version 2.4

+ Nivel 16
 1. Número compuesto múltiple  
    3644792236778694 = [2, 3, 101, 42473, 141607813L] In 0.139 seconds

 2. Número compuesto por dos primos  
    3849788417036503 = [59423701, 64785403L] In 21.8415 seconds

 3. Número primo  
    5332147896211517 = [5332147896211517L] In 22.9942 seconds

    5332147896211517 = [5332147896211517L] In 23.6767 seconds

**Nivel batido**

+ Nivel 17
 1. Número compuesto múltiple  
    64795512344765945 = [5, 31, 83, 157, 653, 49127233L] In 0.1051 seconds

 2. Número compuesto por dos primos  
    32563672784171761 = [67894373, 479622557L] In 32.3036 seconds

 3. Número primo  
    55641397544639089 = [55641397544639089L] In 63.5148 seconds

**Nivel batido**. El tiempo de factorización del número del tipo (2) depende de la
ejecución, cada una tarda un tiempo distinto.


+ Nivel 18

 1. Número compuesto múltiple  
    954788612384655179 = [53077, 118429, 151894763L] In 0.1867 seconds

 2. Número compuesto por dos primos  
    498542964342543929 = [652231511, 764365039L] In 27.4718 seconds

 3. Número primo  
    546698741123646019 = [546698741123646019L] In 164.9989 seconds

**Nivel batido**


+ Nivel 19

 1. Número compuesto múltiple
    3689445781236985154 = [2, 7, 11, 37, 121267, 5339444219L] In 0.1868 seconds

 2. Número compuesto por dos primos
    2537675226119470571 = [548997653, 4622379007L] In 143.3016 seconds

 3. Número primo
    5977455832169755667 = [5977455832169755667L] In 606.9941 seconds

**Nivel batido**


+ Nivel 20

 1. Número compuesto múltiple  
    59774558321697556676 = [2, 2, 23, 2069, 314027771879387L] In 11.8584 seconds

 2. Número compuesto por dos primos  
    36579649644065170163 = [5568743671L, 6568743653L] In 13.4473 seconds   
    25841129207805312677 = [3526889461L, 7326889457L] In 502.3551 seconds
    
 3. Número primo  
    52369844786321568503 = [52369844786321568503L] In 1845.6705 seconds (30 minutos aprox.)

    52369844786321568503 = [52369844786321568503L] In 2371.4282 seconds (más de 39
    minutos)

**Nivel batido**


#### Ajuste del candidato inicial (_v2.4.2_)

En esta versión se ha modificado el ajuste del candidato inicial en la función
factorize_with_limits.  Al principio de la función se define un diccionario:

```
cand_adj_increments= {0:('1',[2,4,2,2]),
                      1:('1',[2,4,2,2]),
                      2:('3',[4,2,2,2]),
                      3:('3',[4,2,2,2]),
                      4:('7',[2,2,2,4]),
                      5:('7',[2,2,2,4]),
                      6:('7',[2,2,2,4]),
                      7:('7',[2,2,2,4]),
                      8:('9',[2,2,4,2]),
                      9:('9',[2,2,4,2])}
 
```

+ La clave del diccionario es la última cifra del candidato a ajustar.
+ El valor del diccionario es una tupla compuesta por:
  + La última cifra que se debe asignar al candidato
  + La lista de incrementos que se usará durante la busqueda de factores

Si el candidato inicial es menor que 5 no se hace ningún procesamiento sobre él y la lista
de incremento que se utiliza es la que se corresponde con la clave 7 del diccionario.

Si el candidato es mayor que 5 se extrae su última cifra `candidate%10` y se usa este
valor como clave para extraer una tupla del diccionario; la segunda parte de la tupla es
la lista de incrementos para el actual candidato; la primera parte de la tupla es la nueva
cifra en que tiene que terminar el candidato.

Este nuevo código tiene menos líneas y es más simple y rápido, aunque probablemente es más
dificil de entender, de ahí esta explicación.



### PARALELISMO EN RED
**Version 3.0**

El siguiente paso en la mejora de la aplicación consiste en añadir la posibilidad de
distribuir el trabajo de factorización entre distintos procesos conectados a través de la
red.  Existirá un proceso principal que se encargará de dividir el trabajo de
factorización en una serie de subtrabajos y de distribuir dichos subtrabajos entre los
clientes que los soliciten.

+ Usamos Twisted para conectar a los distintos factorizadores.
+ El código de red se ejecuta en un proceso independiente, por el tipo de funcionamiento
  de programación asincrona orientada a eventos.
+ La comunicación entre el proceso de red y el proceso padre la haremos mediante colas
  (Queue)

#### FactorClient
**Version 1.0.0**

Para poder distribuir el trabajo de factorización entre distintos equipos en red
necesitamos un cliente que sea capaz de conectarse al servidor, solicitar parte del
trabajo, procesarlo y devolverlo al servidor.

Este cliente usará código asíncrono basado en twisted

Necesitará soportar algunas opciones y parametros de linea de comandos como:

+ Modo verbose, activado o desactivado
+ Direccion de red para conectarse al servidor; estará compuesta por un nombre de host o
IP correspondiente, y un puerto.

El cliente no soportará opciones como:

+ Número a factorizar; lo recibirá del servidor
+ Segmento dentro del cual buscar los factores; lo recibirá del servidor
+ Generar casos de prueba
+ Ejecutar casos de prueba


