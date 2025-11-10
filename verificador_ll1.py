def es_gramatica_ll1(gramatica, conjuntos_first, conjuntos_follow):
    """
    Verifica si una gramática dada cumple con las condiciones para ser LL(1).

    Una gramática es LL(1) si y solo si para cada no-terminal A con dos producciones
    distintas A -> α y A -> β, se cumplen dos condiciones:
    1. First(α) y First(β) son disjuntos (no tienen elementos en común).
    2. Si una de las producciones puede derivar en épsilon (ej: β ->* e), entonces
       First(α) y Follow(A) deben ser disjuntos.

    Parametros:
    - gramatica (dict): La gramática en forma de diccionario.
    - conjuntos_first (dict): Los conjuntos First precalculados.
    - conjuntos_follow (dict): Los conjuntos Follow precalculados.

    Retorna:
    - bool: True si la gramática es LL(1), False en caso contrario.
    """

    for no_terminal, producciones in gramatica.items():
        # Condición 1: First(α) y First(β) deben ser disjuntos para A -> α | β 
        # Comparamos cada par distinto de producciones de un mismo no-terminal
        for i in range(len(producciones)):
            for j in range(i + 1, len(producciones)):
                p1 = producciones[i]
                p2 = producciones[j]
                first_p1 = calcular_first_de_produccion(p1, conjuntos_first)
                first_p2 = calcular_first_de_produccion(p2, conjuntos_first)
                
                # Condición 1: La intersección de los First de dos producciones debe ser vacía.
                if not first_p1.isdisjoint(first_p2):
                    # Si ambas derivan en 'e', el conflicto real es First/Follow, no First/First.
                    if 'e' in first_p1 and 'e' in first_p2:
                        continue
                    return False

                # Condición 2: Si una producción deriva en 'e', su First no puede intersectar el Follow del no-terminal.
                # (Esta condición se simplifica al verificar First(A) y Follow(A) al final)
    
        # Si un no-terminal puede derivar en épsilon, su conjunto First y Follow no deben tener elementos en común.
        if 'e' in conjuntos_first[no_terminal]:
            if not conjuntos_first[no_terminal].isdisjoint(conjuntos_follow[no_terminal]):
                return False
                
    return True

def calcular_first_de_produccion(produccion, conjuntos_first):
    """
    Calcula el conjunto First para una cadena de símbolos específica (una producción).

    Parametros:
    - produccion (str): La cadena de producción a analizar.
    - conjuntos_first (dict): Los conjuntos First precalculados de los no-terminales.

    Retorna:
    - set: El conjunto First de la cadena de producción.
    """
    # Caso base: Si la producción es directamente 'e', su First es {e}.
    if produccion == 'e':
        return {'e'}
    
    first_set = set()
    todos_tienen_epsilon = True
    for simbolo in produccion:
        # Obtiene el conjunto First del símbolo actual (sea terminal o no-terminal)
        simbolo_first = conjuntos_first.get(simbolo, {simbolo})
        
        # Agrega todo el First del símbolo actual, excepto épsilon
        first_set.update(simbolo_first - {'e'})
        
        # Si el símbolo actual no puede producir épsilon entonces la producción completa no puede derivar en épsilon y detenemos el análisis de esta producción
        if 'e' not in simbolo_first:
            todos_tienen_epsilon = False
            break
            
    # Si todos los símbolos en la producción pueden derivar en épsilon, entonces la producción entera puede hacerlo.
    if todos_tienen_epsilon:
        first_set.add('e')
        
    return first_set