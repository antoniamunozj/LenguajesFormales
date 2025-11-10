from verificador_ll1 import calcular_first_de_produccion

def construir_tabla_ll1(gramatica, conjuntos_first, conjuntos_follow):
    """
    Construye la tabla de análisis predictivo LL(1) para la gramática dada.

    La tabla es un diccionario de diccionarios, donde `tabla[NoTerminal][Terminal]`
    contiene la producción que se debe aplicar.

    Parametros:
    - gramatica (dict): La gramática en forma de diccionario.
    - conjuntos_first (dict): Los conjuntos First precalculados para cada no-terminal.
    - conjuntos_follow (dict): Los conjuntos Follow precalculados para cada no-terminal.

    Retorna:
    - dict: La tabla de análisis LL(1) completa.
    """
    tabla = {}
    
    # Itera sobre cada no-terminal y sus producciones para llenar la tabla
    for no_terminal, producciones in gramatica.items():
        tabla[no_terminal] = {}  # Inicializa un diccionario vacío para este 'no_terminal'.
        
         # Itera sobre cada producción del 'no_terminal' actual
        for produccion in producciones:
            # Calcula el conjunto First de la producción actual
            first_de_produccion = calcular_first_de_produccion(produccion, conjuntos_first)
            
            # Regla 1: Para cada terminal 'a' en First(producción), añade la producción a la celda [no_terminal][simbolo] de la tabla
            # Esto significa que si el parser ve 'no_terminal' en la pila y 'simbolo' en la entrada, debe aplicar esta 'produccion'
            for simbolo in first_de_produccion - {'e'}:
                tabla[no_terminal][simbolo] = produccion
            
            # Regla 2: Si 'e' está en First(producción), para cada terminal 'b' en Follow(A),
            # añadir A -> producción a tabla[A][b]
            if 'e' in first_de_produccion:
                for simbolo in conjuntos_follow[no_terminal]:
                    tabla[no_terminal][simbolo] = produccion # debe aplicar esta 'produccion' (que es la producción a épsilon)

    return tabla