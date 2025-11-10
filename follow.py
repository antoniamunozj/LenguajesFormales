
def calcular_conjuntos_follow(gramatica, conjuntos_first):
    """
    Calcula los conjuntos Follow para todos los no terminales en la gramatica.

    Parametros:
    - gramatica (dict): Un diccionario que representa la gramatica.
    - conjuntos_first (dict): Un diccionario con los conjuntos First para cada no terminal.

    Retorna:
    - follow (dict): Un diccionario donde cada clave es un no terminal y cada valor es 
                     el conjunto Follow de ese no terminal.
    """
    # Inicializamos el conjunto Follow de cada no terminal como un conjunto vacio
    follow = {nt: set() for nt in gramatica}

    # Agregamos '$' al conjunto Follow del símbolo inicial (Por convención el símbolo inicial (S) siempre contiene el marcador de fin de cadena)
    follow['S'].add('$')

    # Usamos un ciclo para aplicar cambios hasta que no haya mas modificaciones
    cambio = True
    while cambio:
        cambio = False
        # Recorremos cada no terminal y sus producciones
        for no_terminal in gramatica:
            for produccion in gramatica[no_terminal]:

                # Inicializamos la cola con el Follow del no_terminal actual
                # Esta cola se usa para propagar símbolos hacia la izquierda.
                cola = follow[no_terminal].copy()

                # Recorremos la producción al revés (de derecha a izquierda)
                for simbolo in reversed(produccion):
                    if simbolo in gramatica:  # Es un no terminal

                        # Actualizamos el conjunto Follow del simbolo actual si hay elementos nuevos para agregar
                        if cola - follow[simbolo]:
                            follow[simbolo].update(cola)
                            cambio = True # Indicamos que hubo un cambio y debemos seguir iterando

                        # Si 'ε' esta en First, agregamos tambien los terminales de First menos 'ε' a la cola
                        if 'e' in conjuntos_first[simbolo]:
                            cola.update(conjuntos_first[simbolo] - {'e'})
                        else:
                            # Si 'ε' no esta en First, la cola se convierte en First del simbolo
                            cola = conjuntos_first[simbolo].copy()
                    else:
                        # Si es un terminal, la cola pasa a ser solo ese terminal (se convierte en {simbolo})
                        cola = {simbolo}
    
    return follow