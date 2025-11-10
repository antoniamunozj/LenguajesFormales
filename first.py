def calcular_conjuntos_first(gramatica):
    """
    Calcula los conjuntos First para todos los no terminales en la gramatica.

    Parametros:
    - gramatica (dict): Un diccionario que representa la gramatica, donde las claves son no terminales y los valores
                        son listas de producciones.

    Retorna:
    - first (dict): Un diccionario donde cada clave es un no terminal y cada valor es el conjunto First 
                    de ese no terminal.
    """
    # Inicializamos el conjunto First 
    # Cada no terminal empieza con un conjunto vacio
    first = {nt: set() for nt in gramatica}

    # Recorremos cada no terminal y calculamos su conjunto FIRST usando recursión.
    for no_terminal in gramatica:
        calcular_first(no_terminal, gramatica, first, set())
    return first

def calcular_first(simbolo, gramatica, first, visitados):
    """
    Calcula recursivamente el conjunto First para un simbolo dado.

    Parametros:
    - simbolo (str): El simbolo (no terminal o terminal) para calcular el conjunto First.
    - gramatica (dict): El diccionario que representa la gramatica.
    - first (dict): El diccionario que contiene los conjuntos First.
    - visitados (set): Un conjunto para rastrear los no terminales visitados y evitar bucles de recursion.

    Retorna:
    - set: El conjunto First para el simbolo dado.
    """
     # Si el simbolo ya fue visitado, retornamos su conjunto First (evitamos recalcularlo, previene bucles)
    if simbolo in visitados:
        return first[simbolo]
    
    # Si el simbolo es terminal, su conjunto First es el mismo
    if simbolo not in gramatica:  
        return {simbolo}
    
    # Marcamos el simbolo actual como visitado para evitar bucles
    visitados.add(simbolo)

    # Recorremos cada producción del no terminal actual
    for produccion in gramatica[simbolo]:
        # Recorremos los símbolos de la producción, de izquierda a derecha
        for caracter in produccion:
            # Calculamos el conjunto First del caracter actual
            first_del_caracter = calcular_first(caracter, gramatica, first, visitados)
            # Agregamos todos los elementos de First menos 'ε'
            first[simbolo].update(first_del_caracter - {'e'})
            # Si el carácter actual no puede derivar 'ε', dejamos de analizar la producción
            if 'e' not in first_del_caracter:
                break
        else:
            # Si todos los símbolos de la producción pueden producir 'ε', se agrega al FIRST
            first[simbolo].add('e')
            
    # Quitamos el simbolo de visitados al terminar (permite reutilizarlo en otras ramas)
    visitados.remove(simbolo)
    
    return first[simbolo]
