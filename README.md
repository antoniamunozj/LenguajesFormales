# Analizador Sintáctico LL(1) y SLR(1)

Este proyecto es una implementación en Python de un analizador sintáctico capaz de trabajar con gramáticas LL(1) y SLR(1). El programa lee una gramática libre de contexto desde un archivo, calcula sus conjuntos First y Follow, determina si la gramática es LL(1) y/o SLR(1), y permite analizar cadenas de texto utilizando el parser correspondiente.

## Integrantes

* Maria Antonia Muñoz
* Leidy Dayhana Roldan

## Características

- **Cálculo de Conjuntos First y Follow:** Calcula y muestra los conjuntos First y Follow para todos los no-terminales de la gramática.
- **Verificación de Gramáticas:**
  - Verifica si una gramática cumple las condiciones para ser LL(1).
  - Verifica si una gramática cumple las condiciones para ser SLR(1).
- **Parsers Implementados:**
  - Parser Predictivo **LL(1)** (Top-Down).
  - Parser **SLR(1)** (Bottom-Up).
- **Menú Interactivo:** Si una gramática es tanto LL(1) como SLR(1), el programa ofrece un menú para que el usuario elija qué parser utilizar.
- **Modo Detallado (Verbose):** Incluye una opción para visualizar el proceso de análisis paso a paso, mostrando el estado de la pila, la entrada restante y la acción tomada en cada momento. Ideal para depuración y sustentaciones.

## Requisitos

- Python 3.11

## Instalación

No se requiere la instalación de paquetes o librerías adicionales. Solo es necesario tener Python 3 instalado en el sistema.

1. Clona o descarga todos los archivos del proyecto en una misma carpeta.
2. Asegúrate de que todos los archivos `.py` estén en el mismo directorio.

## Modo de Empleo

1.  **Crear el archivo `input.txt`**: En la misma carpeta donde se encuentran los scripts de Python, crea un archivo de texto llamado `input.txt`.

2.  **Definir la Gramática**: Edita el archivo `input.txt` para definir la gramática que deseas analizar, siguiendo el formato especificado a continuación.

3.  **Ejecutar el Programa**: Abre una terminal o línea de comandos en la carpeta del proyecto y ejecuta el siguiente comando:
    ```bash
    python main.py
    ```

4.  **Interactuar**: El programa imprimirá los conjuntos First y Follow, y luego te informará sobre el tipo de gramática. Sigue las instrucciones en la consola para activar el modo detallado, seleccionar un parser (si es aplicable) e introducir las cadenas que deseas analizar.

## Formato del Archivo `input.txt`

El archivo debe seguir una estructura estricta para ser leído correctamente:

- **Línea 1:** Un único número entero `N` que representa la cantidad de no-terminales que se definirán.
- **Líneas Siguientes (N líneas):** Cada una de las `N` líneas siguientes define las producciones para un no-terminal.

#### Reglas de Formato para las Producciones:
- El formato es `A -> α | β | ...`, donde `A` es el no-terminal y `α`, `β` son las producciones.
- El símbolo inicial **debe ser `S`**.
- Los no-terminales se representan con **letras mayúsculas**.
- Los terminales se representan con **letras minúsculas o símbolos** (ej: `+`, `*`, `(`).
- La cadena vacía (épsilon) se representa con la letra `e`.
- **Importante:** Debe haber espacios alrededor de la flecha `->` y de la barra `|` que separa las alternativas.

#### Ejemplos de `input.txt`:
```
5
S -> T X
X -> + T X | e
T -> F Y
Y -> * F Y | e
F -> ( S ) | i
```
```
3
S -> A B
A -> a A | e
B -> b
```
