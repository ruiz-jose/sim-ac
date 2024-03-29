# Aprender arquitectura de compputadoras!!

Objetivo: comprender el funcionamiento de la computadora a traves de la arquitectura acumulador

## Tabla de contenido

* [Arquitectura Acumulador](#Arquitectura_Acumulador)
* [Usando ensamblador](#Usando_ensamblador)
   * [Repertorio de instrucciones](#Repertorio_de_instrucciones)
      * [Instrucciones implementadas](#Instrucciones_implementadas)
   * [Comentarios](#comentarios)
   * [Etiquetas](#etiquetas)
   * [Espacio en blanco](#Espacio_en_blanco)
* [Ejecutar código](#Ejecutar_código)
* [Para hacer1](#Para_hacer1)
    * [Ciclos instrucciones](#Ciclos_instrucciones)
* [Para hacer2](#Para_hacer2) 


## Arquitectura_Acumulador 

La arquitectura del CPU permite gestionar un bus de direcciones de 5 bits = 2**5 = 32 posiciones y cada posicion de memoria contiene un 1 byte. El bus de datos de 8 bits (1 byte). Ergo, la CPU procesa datos de 1 byte (8 bits), puede acceder solo 32 bytes de RAM, por lo tanto, el programa debe caber en 32 bytes y esto incluye cualquier variable que utilice.


# logisim-cpu8bit Harvard-Logisim
<img src="./assets/sim-AC-Harvard-logisim.png" >

# circuitverse-cpu8bit  (on-line)
<img src="./assets/AC-7.png" >
https://circuitverse.org/simulator/embed/sim-ac-harvard

Basado en:
En base EaterEmulator emulates [Ben Eater's](https://www.youtube.com/channel/UCS0N5baNlQWJCUrhCEo8WlA) trabajaremos con python para aprender la arquitectura acumulador de 8 bits.

La implementación del cpu de Ben Eater:
https://eater.net/8bit/control

Hecha en Python se copio descaradamente de este link:
https://github.com/jaychandra86/EaterEmulator

En base al simulador Von Neumann Machine Simulator de Autor: Lorenzo Ganni

Link simulador: https://ruiz-jose.github.io/arq-acc/

Link codigo fuente: https://github.com/ruiz-jose/arq-acc


## Usando_ensamblador

Este proyecto incluye un Ensamblador que admite algunas de las capacidades estándar que esperaría encontrar en un ensamblador.

Cree un archivo .asm y escriba su programa en ensamblador. 
El programa puede tener un maximo de 32 líneas.

El ensamblador se encarga de traducir el programa a codigo maquina que entiende el CPU.

Por ejemplo: si desea escribir un programa que sume 5 + 3, debería ser algo como esto

``` asm
0 LDA [4]
1 ADD [5]
2 STA [6]
3 HLT
4 2
5 3
6 0
```

En la `línea 0`, podemos ver `LDA [4]`, esto significa que carga el valor de la `dirección 4` en el `registro AC`. Esta `dirección 4` está en la `línea 4` que tiene un valor de `52`. Por lo tanto, carga `2` en el `registro AC`.

En la `línea 1`, tenemos `ADD [5]`, esto sumará el contenido de la `dirección 5` con el `registro AC`, luego  el resultado queda almacenado en el `registro AC` será `5`.

En la `línea 2`, tenemos `STA 6`, esto almacenará el contenido `registro AC` en la `dirección 6`.

En la `línea 3`, tenemos `HLT`, esto detiene el programa.


### Repertorio_de_instrucciones

| # | OpCode | Nemonico             | Acción
| - |--------|----------------------|------------
| 0 | 000    | **ADD** [Dirección]  | Sumar el registro AC con el contenido de memoria xxx
| 1 | 001    | **SUB** [Dirección]  | Restar el registro AC con el contenido de memoria xxx
| 2 | 010    | **LDA** [Dirección]  | Cargar el contenido de la dirección de memoria xxx en el registro AC
| 3 | 011    | **STA** [Dirección]  | Almacenar el contenido del registro AC en la dirección de memoria xxx
| 4 | 100    | **JMP** Dirección    | Saltar a la dirección de memoria
| 5 | 101    | **JZ**  Dirección    | Saltar a la dirección de memoria, Si Z= 1
| 6 | 110    | **JC**  Dirección    | Saltar a la dirección de memoria, Si C= 1
| 7 | 111    | **HLT**              | Detiene la ejecución



## Usando_ensamblador

Este proyecto incluye un Ensamblador que admite algunas de las capacidades estándar que esperaría encontrar en un ensamblador.

Cree un archivo .asm y escriba su programa en ensamblador. 
El programa puede tener un maximo de 64 líneas.

El ensamblador se encarga de traducir el programa a codigo maquina que entiende el CPU.

Por ejemplo: si desea escribir un programa que sume 5 + 3, debería ser algo como esto

``` asm
0 LDA [4]
1 ADD [5]
2 STA [6]
3 HLT
4 5
5 3
6 0
```

En la `línea 0`, podemos ver `LDA 4`, esto significa que carga el valor de la `dirección 4` en el `registro ACC`. Esta `dirección 4` está en la `línea 4` que tiene un valor de `5`. Por lo tanto, carga `5` en el `registro ACC`.

En la `línea 1`, tenemos `ADD 5`, esto almacenará el contenido de la `dirección 5` en el `registro MDR`, luego agrega este valor al contenido del `registro ACC`, por lo tanto, el valor final del `registro ACC` será `8`.

En la `línea 2`, tenemos `STA 6`, esto almacenará el contenido `registro ACC` en la `dirección 6`.

En la `línea 3`, tenemos `HLT`, esto detiene el programa.


### Repertorio_de_instrucciones

| OpCode | Mnemonic     | Description
|--------|--------------|------------
| 00     | **LDA** xxx  | Cargar el contenido de la dirección de memoria xxx en el registro ACC
| 01     | **STA** xxx  | Almacenar el contenido del registro ACC en la dirección de memoria xxx
| 10     | **ADD** xxx  | Sumar el registro ACC con el contenido de memoria xxx
| 11     | **HLT**      | Detiene la ejecución


#### Instrucciones_implementadas

- [x] LDA
- [x] STA
- [x] ADD
- [x] HLT
- [ ] SUB



### Comentarios

Los comentarios son ignorados por el ensamblador y siempre van precedidos por un punto y coma. (`;`)

``` asm
; Este es un comentario en una línea por sí mismo.
  LDA 15 ; Este es un comentario en línea y debe estar al final de una línea.
  ```


### Etiquetas

* Las etiquetas deben estar en una línea por sí mismas.
* Sin espacios en blanco antes de la etiqueta.
* El ensamblador buscará una etiqueta basada en esta expresión regular: `"^\w*:$"` IE: Inicio de línea, cualquier número de caracteres alfanuméricos y guiones bajos, pero sin espacios en blanco y dos puntos (`:`) al final.
* Cuando utilice una etiqueta en una instrucción, NO incluya los dos puntos al final.


``` asm
; programa simple
start:
    LDA [x]
    ADD [y]
    STA [z]
    HLT
x:
    3
y:
    2
z:
    2
```

En este ejemplo, las etiquetas: 'start', 'x', 'y' y 'z' actúan como punteros a direcciones de memoria. El ensamblador pasará primero por el código para encontrar todas las etiquetas y registrar sus direcciones de memoria. Luego, en la segunda pasada, sustituirá las etiquetas por las direcciones reales. 


### Espacio_en_blanco

Se requiere al menos un carácter de espacio en blanco entre los mnemotécnicos que requieren argumentos y sus argumentos.


## Ejecutar_código

Se requiere la instalación de la versión `Python 3.x`.
Clone este repositorio `git clone https://github.com/ruiz-jose/tudw-arq.git` 
Ejecute:

```
 python cpu.py <nombre de archivo asm>
```

## Para_hacer1

Teniendo en cuenta las medidas de rendimiento vistas en la Semana 2 y los pasos del ciclo de instrucción vistas en la Semana 3.

A partir de la implementacion de la arquitectura acumulador hecha en python que se encuentra en el respositorio **[arq-acc-py](https://github.com/ruiz-jose/arq-acc-py)**, calcular:

- Ciclos de reloj para el programa (**Program-Cycles**)

- Recuento de instruccoines para el programa (**RI**)

- Promedio de ciclos por instruccion para el programa (**CPI**)

- Tiempo de CPU para el programa (**Time CPU**) sabiendo que:

- La Duración del ciclo o Frecuencia (Hz) necesarias para calcular el Tiempo de CPU se debe tener en cuenta los siguientes datos:
    * El CPU funciona a 20 Hz por lo que:

        - La duracion de un ciclo de CPU es --> 1/Hz = 1/20 = 0.05 segundos 

    * La memoria RAM funciona a 10 Hz por lo que:

        - Como la memoria RAM es más lenta el CPU debe esperar a que la memoria responda.
        
        - La duracion del ciclo de la memoria RAM es --> 1/HZ = 1/10 = 0.1 segundos.

        - Cada orden de lectura o escritura (read/write) a memoria RAM tarda 2 ciclos de RAM, entonces una operacion en memoria tarda 0.2 segundos.

        - 0.2 segundos de una operacion de memoria RAM representa 4 ciclos de CPU (0.05 ciclos de CPU * 4 = 0.2 segundos), entonces el CPU espera (wait) por 4 ciclos cada vez que hay una operacion de lectura o escritura en la memoria RAM

    Por ejemplo los ciclos de reloj para la instruccion LDA x  son 14 ciclos debido a que:

    - La etapa captación de la instrucción lleva:
        * 7 ciclos = 3 ciclos CPU (pasos para captar instruccion) + 4 ciclos que el CPU espera para que la memoria devuelva la instrucción LDA

    - Etapa ejecucion:
        * 7 ciclos = 3 ciclos CPU (pasos para ejecutar la instruccion) + 4 ciclos que el CPU espera para que la memoria devuelva el dato x solicitado por la instruccion 

### Ciclos_instrucciones
| Mnemonic | Ciclos
|----------|------------
| LDA      | 14 ciclos
| STA      | 14 ciclos
| ADD      | 14 ciclos
| HLT      | 8 ciclos

## Para_hacer2
1- Realizar un Fork de este repositorio a tu cuenta de github.

2- Abrir el repositorio de tu cuenta de github con el editor online https://insiders.vscode.dev/ o realizar desde un editor en la maquina local.

3- Actualizar los cambios del repositorio en tu cuenta de github.

4- Desde el repositorio en github crear un pull request para contribuir al repositorio **[arq-acc-py](https://github.com/ruiz-jose/arq-acc-py)**
