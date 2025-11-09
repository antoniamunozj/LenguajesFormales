from verificador_slr1 import closure, goto

def construir_tabla_slr1(gramatica, conjuntos_follow):
    """
    Construye la tabla de analisis SLR(1) para la gramatica.

    Parámetros:
    - gramatica (dict): Representación de la gramática libre de contexto.
                        Ejemplo: {'S': ['AB'], 'A': ['aA', 'e'], 'B': ['b']}
    - conjuntos_follow (dict): Diccionario con los conjuntos FOLLOW de cada no terminal.

    Retorna:
    - (tabla_acciones, tabla_goto): Dos diccionarios que representan la tabla ACTION y GOTO
      del analizador SLR(1).

    """

    # Se crea una copia de la gramática para añadir una producción inicial aumentada.
    # Por ejemplo, si S es el símbolo inicial, se añade S' → S
    gramatica_aumentada = gramatica.copy()
    simbolo_inicial_aumentado = "S'"
    if simbolo_inicial_aumentado in gramatica:
        simbolo_inicial_aumentado = "S''" # Evita colisión de nombres
    
    gramatica_aumentada[simbolo_inicial_aumentado] = ['S']
    
    # Calculamos el estado inicial usando la función CLOSURE
    # closure devuelve el conjunto de items iniciales, por ejemplo: S' → •S
    estado_inicial = closure({(simbolo_inicial_aumentado, 'S', 0)}, gramatica_aumentada)
    estados = [estado_inicial] # Lista con todos los estados (conjuntos de items LR(0))
    pendientes = [estado_inicial] # Cola de estados por procesar
    
    transiciones = {} # Almacena las transiciones (estado, símbolo) → nuevo estado

    # Construir la coleccion de estados (Colección Canónica)
    while pendientes:
        estado_actual = pendientes.pop(0) # Tomamos un estado pendiente
        i = estados.index(estado_actual) # Su índice (número de estado)
        
        # Obtenemos todos los símbolos posibles (no terminales + terminales)
        simbolos_posibles = list(gramatica.keys()) + list(set(c for prod_list in gramatica.values() for p in prod_list for c in p if c not in gramatica and c != 'e'))

        # Para cada símbolo, aplicamos GOTO y generamos nuevos estados
        for simbolo in simbolos_posibles:
            nuevo_estado = goto(estado_actual, simbolo, gramatica_aumentada)
            if nuevo_estado:
                # Si es un estado nuevo, lo agregamos
                if nuevo_estado not in estados:
                    estados.append(nuevo_estado)
                    pendientes.append(nuevo_estado)
                j = estados.index(nuevo_estado)
                transiciones[(i, simbolo)] = j # Guardamos la transición

    # 4. Inicializamos las tablas ACTION y GOTO
    tabla_acciones = {}
    tabla_goto = {}

     # 5. Llenamos las tablas de acción y salto (goto)
    for i, estado in enumerate(estados):
        tabla_acciones[i] = {}
        tabla_goto[i] = {}

        # Cada estado contiene items de la forma (A, αβ, punto)
        for (no_terminal, produccion, punto) in estado:
            # Caso 1: Produccion de epsilon (siempre es una reduccion)
            if produccion == 'e':
                for simbolo_follow in conjuntos_follow[no_terminal]:
                    tabla_acciones[i][simbolo_follow] = ('reduce', (no_terminal, produccion))
                continue

            # Caso 2: El punto no esta al final (accion Shift)
            if punto < len(produccion):
                simbolo = produccion[punto]
                if simbolo not in gramatica: # Si es un terminal
                    if (i, simbolo) in transiciones:
                        tabla_acciones[i][simbolo] = ('shift', transiciones[(i, simbolo)])
            # Caso 3: El punto esta al final (accion Reduce o Accept)
            else:
                # Si es la producción aumentada (S' → S.), entonces se acepta
                if no_terminal == simbolo_inicial_aumentado: 
                    tabla_acciones[i]['$'] = ('accept', None)
                else:
                    # En otro caso, se reduce por cada símbolo del conjunto FOLLOW
                    for simbolo_follow in conjuntos_follow[no_terminal]:
                        tabla_acciones[i][simbolo_follow] = ('reduce', (no_terminal, produccion))
    
    # 6. Llenamos la tabla GOTO (solo para no terminales)
    for i in range(len(estados)):
        for nt in gramatica.keys():
            if (i, nt) in transiciones:
                tabla_goto[i][nt] = transiciones[(i, nt)]

    return tabla_acciones, tabla_goto

def parse_slr1(cadena, tabla_acciones, tabla_goto, simbolo_inicial, verbose=False):
    """
    Analiza la cadena de entrada usando el parser SLR(1).

    Parámetros:
    - cadena (str): La cadena de entrada (por ejemplo, 'i*i').
    - tabla_acciones (dict): Tabla ACTION generada por construir_tabla_slr1.
    - tabla_goto (dict): Tabla GOTO generada por construir_tabla_slr1.
    - simbolo_inicial (str): Símbolo inicial de la gramática.
    - verbose (bool): Si es True, muestra el proceso paso a paso.

    Retorna:
    - bool: True si la cadena es aceptada, False si hay error sintáctico.

    """
    # Inicializamos la pila con el estado 0 (estado inicial)
    pila = [0]
    cadena += '$' # Agregamos el marcador de fin de entrada
    posicion = 0 # Índice del símbolo actual

    # Encabezado para impresión si se activa el modo verbose
    if verbose:
        print("\n--- SLR(1) Parsing Process ---")
        print(f"{'STACK':<40} {'INPUT':<20} {'ACTION'}")
        print("-" * 80)

    # Bucle principal del analizador SLR(1)
    while True:
        estado = pila[-1] # Estado actual (último número en la pila)
        simbolo = cadena[posicion] # Símbolo actual de la entrada

        # Mostrar estado actual de la pila y la entrada
        if verbose:
            pila_str = " ".join(map(str, pila))
            input_str = cadena[posicion:]
            print(f"{pila_str:<40} {input_str:<20}", end="")

        # Consultamos la acción correspondiente en la tabla ACTION
        if simbolo in tabla_acciones.get(estado, {}):
            accion, valor = tabla_acciones[estado][simbolo]

            # Acción SHIFT → desplazamiento
            if accion == 'shift':
                if verbose:
                    print(f"Shift to state {valor}")
                pila.append(simbolo) # Metemos el símbolo
                pila.append(valor) # Luego el nuevo estado
                posicion += 1 # Avanzamos al siguiente símbolo

            # Acción REDUCE → aplicamos una producción
            elif accion == 'reduce':
                nt, prod = valor
                if verbose:
                    print(f"Reduce by {nt} -> {prod}")
                # Por cada símbolo en la producción, sacamos dos elementos de la pila (símbolo y estado)
                if prod != 'e':
                    pila = pila[:-2 * len(prod)]
                
                # Tomamos el estado que quedó en la cima
                estado_anterior = pila[-1]
                # Colocamos el no terminal reducido y el nuevo estado GOTO
                pila.append(nt)
                pila.append(tabla_goto[estado_anterior][nt])

            # Acción ACCEPT → cadena aceptada
            elif accion == 'accept':
                if verbose:
                    print("Accept")
                return True
        # Si no existe acción válida → error sintáctico
        else:
            if verbose:
                print("Error")
            return False
