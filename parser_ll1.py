def parse_ll1(cadena, tabla_ll1, simbolo_inicial, verbose=False):
    """
    Analiza la cadena de entrada usando el parser LL(1) y la tabla de analisis predictivo.

    Parametros:
    - cadena (str): La cadena de entrada a analizar.
    - tabla_ll1 (dict): La tabla de analisis predictivo LL(1).
    - simbolo_inicial (str): El simbolo inicial de la gramatica.
    - verbose (bool): Si es True, imprime el proceso paso a paso.

    Retorna:
    - bool: True si la cadena es aceptada, False si no lo es.
    """
    
    pila = ['$', simbolo_inicial] # Inicializamos la pila con el símbolo inicial y el marcador de fin de cadena '$'
    cadena += '$' # Tambien se añade el marcador de fin de cadena '$' al final de la entrada
    posicion = 0 # índice del símbolo actual que estamos leyendo de la cadena

    # Impresión del encabezado del proceso (solo si verbose=True)
    if verbose:
        print("\n--- LL(1) Parsing Process ---")
        print(f"{'STACK':<30} {'INPUT':<20} {'ACTION'}")
        print("-" * 70)

    # El ciclo principal, se ejecuta hasta que la pila esté vacía
    while len(pila) > 0:
        tope = pila[-1] # Obtenemos el símbolo en la cima de la pila (tope)
        simbolo_actual = cadena[posicion] # Obtenemos el símbolo actual de la cadena de entrada
        
        # Si verbose=True, mostramos el estado actual de la pila, la entrada y la acción
        if verbose:
            pila_str = " ".join(reversed(pila)) # Mostramos la pila de arriba hacia abajo (por eso se usa reversed)
            input_str = cadena[posicion:] # Mostramos la parte de la cadena que falta por leer
            print(f"{pila_str:<30} {input_str:<20}", end="")

        # Caso 1: el tope de la pila coincide con el símbolo actual de entrada
        if tope == simbolo_actual:
             # Si ambos son '$', significa que llegamos al final de la pila y la entrada → Aceptado
            if tope == '$':
                if verbose:
                    print("Accept")
                return True # La cadena pertenece al lenguaje
            
            # Si no es '$', simplemente consumimos ese símbolo (lo sacamos de la pila y avanzamos en la cadena)
            pila.pop()
            posicion += 1
            if verbose:
                print(f"Match '{simbolo_actual}'")

        # Caso 2: el tope de la pila es un no terminal y hay una producción en la tabla LL(1)
        elif tope in tabla_ll1 and simbolo_actual in tabla_ll1[tope]:
            # Sacamos el no terminal de la pila
            pila.pop()
            # Obtenemos la producción correspondiente de la tabla LL(1)
            produccion = tabla_ll1[tope][simbolo_actual]

            # Si la producción no es 'ε', añadimos sus símbolos a la pila en orden inverso
            # (porque el análisis LL(1) expande el no terminal reemplazándolo por su producción)
            if produccion != 'e':
                pila.extend(reversed(list(produccion)))
            if verbose:
                print(f"Produce with {tope} -> {produccion}")
        
        # Caso 3: no hay coincidencia ni regla en la tabla LL(1) → Error
        else:
            if verbose:
                print("Error")
            return False
    
    return False