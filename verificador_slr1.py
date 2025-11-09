def closure(items, gramatica):
    """
    Calcula la cerradura (closure) de un conjunto de ítems LR(0).

    La cerradura expande un conjunto de ítems. Si un ítem tiene el punto '.'
    justo antes de un no-terminal (ej: [A -> α.Bβ]), se añaden todos los
    ítems correspondientes a las producciones de ese no-terminal (ej: [B -> .γ]).
    Este proceso se repite hasta que no se puedan añadir más ítems.

    Parametros:
    - items (set): Un conjunto de ítems LR(0) iniciales. Un ítem es una tupla (cabeza, cuerpo, pos_punto).
    - gramatica (dict): La gramática del lenguaje.

    Retorna:
    - set: El conjunto de ítems LR(0) cerrado y completo.
    """
    cerrado = set(items)
    cambios = True
    while cambios:
        cambios = False
        # Se itera sobre una copia de la lista para poder modificar el conjunto 'cerrado' durante la iteración
        for (no_terminal, produccion, punto) in list(cerrado):
            # Si el punto no está al final y le sigue un no-terminal...
            if punto < len(produccion) and produccion[punto] in gramatica:
                siguiente_no_terminal = produccion[punto]
                # ...añadir todas las producciones de ese no-terminal al conjunto de ítems.
                for prod_cuerpo in gramatica[siguiente_no_terminal]:
                    item = (siguiente_no_terminal, prod_cuerpo, 0)
                    if item not in cerrado:
                        cerrado.add(item)
                        cambios = True
    return cerrado


def goto(items, simbolo, gramatica):
    """
    Calcula la función de transición GOTO para un conjunto de ítems y un símbolo.

    El GOTO(I, X) representa la transición de un estado 'I' con un símbolo 'X'.
    Se toman todos los ítems en 'I' donde el punto '.' está antes de 'X', se mueve
    el punto un lugar a la derecha, y luego se calcula la cerradura (closure)
    de este nuevo conjunto de ítems.

    Parametros:
    - items (set): El conjunto de ítems LR(0) actual (un estado).
    - simbolo (str): El símbolo de transición (terminal o no-terminal).
    - gramatica (dict): La gramática del lenguaje.

    Retorna:
    - set: El nuevo conjunto de ítems (el nuevo estado) tras la transición.
    """
    nuevos_items = set()
    for (no_terminal, produccion, punto) in items:
        # Si el punto no está al final y el símbolo después del punto es el que buscamos...
        if punto < len(produccion) and produccion[punto] == simbolo:
            # ...movemos el punto una posición a la derecha y añadimos el nuevo ítem.
            nuevos_items.add((no_terminal, produccion, punto + 1))
    
    # Devolvemos la cerradura del nuevo conjunto de ítems.
    return closure(nuevos_items, gramatica)


def es_gramatica_slr1(gramatica, conjuntos_follow):
    """
    Verifica si una gramática dada es SLR(1).

    Construye la colección canónica de ítems LR(0) (los estados del autómata)
    y luego verifica en cada estado si existen conflictos de tipo Shift/Reduce
    o Reduce/Reduce.

    Parametros:
    - gramatica (dict): La gramática del lenguaje.
    - conjuntos_follow (dict): Los conjuntos Follow precalculados.

    Retorna:
    - bool: True si la gramática es SLR(1), False si no.
    """
    # Aumentar la gramática con una nueva regla inicial S' -> S
    gramatica_aumentada = gramatica.copy()
    simbolo_inicial_aumentado = "S'"
    if simbolo_inicial_aumentado in gramatica:
        simbolo_inicial_aumentado = "S''"
    
    gramatica_aumentada[simbolo_inicial_aumentado] = ['S']

    # Generar todos los estados del autómata LR(0)
    estado_inicial = closure({(simbolo_inicial_aumentado, 'S', 0)}, gramatica_aumentada)
    estados = [estado_inicial]
    pendientes = [estado_inicial]

    while pendientes:
        estado_actual = pendientes.pop(0)
        simbolos = list(gramatica.keys()) + list(set(c for prod_list in gramatica.values() for p in prod_list for c in p if c not in gramatica and c != 'e'))

        for simbolo in simbolos:
            nuevo_estado = goto(estado_actual, simbolo, gramatica_aumentada)
            if nuevo_estado and nuevo_estado not in estados:
                estados.append(nuevo_estado)
                pendientes.append(nuevo_estado)

    # Verificar cada estado en busca de conflictos
    for estado in estados:
        items_reduce = []
        simbolos_shift = set()

        # Separar los ítems del estado en acciones de shift y de reduce
        for (no_terminal, produccion, punto) in estado:
            if produccion == 'e':
                if no_terminal != simbolo_inicial_aumentado:
                    items_reduce.append(no_terminal)
                continue

            if punto < len(produccion):
                simbolo_siguiente = produccion[punto]
                if simbolo_siguiente not in gramatica:
                    simbolos_shift.add(simbolo_siguiente)
            else: # El punto está al final, es un ítem de reducción
                if no_terminal != simbolo_inicial_aumentado:
                    items_reduce.append(no_terminal)

        # Conflicto Shift/Reduce: si un símbolo de shift está en el Follow de un ítem de reducción.
        for nt_reduce in items_reduce:
            if not simbolos_shift.isdisjoint(conjuntos_follow[nt_reduce]):
                return False # Conflicto S/R encontrado

        # Conflicto Reduce/Reduce: si hay múltiples ítems de reducción y sus Follow sets se solapan.
        if len(items_reduce) > 1:
            conjuntos_follow_reduce = [conjuntos_follow[nt] for nt in items_reduce]
            for r_i in range(len(conjuntos_follow_reduce)):
                for r_j in range(r_i + 1, len(conjuntos_follow_reduce)):
                    if not conjuntos_follow_reduce[r_i].isdisjoint(conjuntos_follow_reduce[r_j]):
                        return False # Conflicto R/R encontrado
                        
    return True # Si no se encontraron conflictos, la gramática es SLR(1)