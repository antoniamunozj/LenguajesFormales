from first import calcular_conjuntos_first
from follow import calcular_conjuntos_follow
from verificador_ll1 import es_gramatica_ll1, calcular_first_de_produccion
from verificador_slr1 import es_gramatica_slr1
from tabla_ll1 import construir_tabla_ll1
from parser_ll1 import parse_ll1
from parser_slr1 import construir_tabla_slr1, parse_slr1

def analizar_gramatica_input(texto_entrada):
    """
    Analiza el texto de entrada de la gramática y lo convierte en una estructura de diccionario.

    Parametros:
    - texto_entrada (str): El contenido completo del archivo input.txt.

    Retorna:
    - dict: Un diccionario que representa la gramática, ej: {'S': ['aA', 'b']}.
    """
    lineas = texto_entrada.strip().splitlines()
    num_no_terminales = int(lineas[0])
    gramatica = {}
    
    # Itera sobre cada línea que define una producción de un no-terminal
    for i in range(1, num_no_terminales + 1):
        linea = lineas[i]
        if '->' not in linea:
            continue
        
        # Separa la cabeza (no-terminal) del cuerpo de la producción
        no_terminal, producciones_str = linea.split('->', 1)
        no_terminal = no_terminal.strip()
        
        # Separa las diferentes alternativas de producción
        alternativas = producciones_str.split('|')
        
        producciones_finales = []
        for alt in alternativas:
            alt = alt.strip()
            if alt == 'e':
                producciones_finales.append('e')
            else:
                # Une los símbolos de la producción (ej: 'a A' se convierte en 'aA')
                producciones_finales.append("".join(alt.split()))

        gramatica[no_terminal] = producciones_finales
            
    return gramatica

def main():
    """
    Función principal que orquesta todo el proceso del analizador sintáctico.

    - Lee la gramática de entrada.
    - Calcula los conjuntos First y Follow.
    - Verifica si la gramática es LL(1) y/o SLR(1).
    - Maneja la interacción con el usuario para el análisis de cadenas.
    """
    # --- 1. Lectura y Preparación de la Gramática ---
    try:
        with open('input.txt', 'r') as archivo:
            texto_entrada = archivo.read()
    except FileNotFoundError:
        print("Error: No se encontro el archivo 'input.txt'.")
        return

    gramatica = analizar_gramatica_input(texto_entrada)
    
    # El símbolo inicial 'S' es un requisito del programa
    if 'S' not in gramatica:
        print("Error: La gramatica debe contener un simbolo inicial 'S'.")
        return

    # --- 2. Cálculos y Verificaciones ---
    conjuntos_first = calcular_conjuntos_first(gramatica)
    conjuntos_follow = calcular_conjuntos_follow(gramatica, conjuntos_first)

    # Imprimir conjuntos First y Follow para el usuario
    import json
    print("\n--- First Sets ---")
    for key, value in conjuntos_first.items():
        print(f'"{key}": {json.dumps(sorted(list(value)))}')

    print("\n--- Follow Sets ---")
    for key, value in conjuntos_follow.items():
        print(f'"{key}": {json.dumps(sorted(list(value)))}')
    print("--------------------\n")

    # Determinar el tipo de gramática
    es_ll1 = es_gramatica_ll1(gramatica, conjuntos_first, conjuntos_follow)
    es_slr1 = es_gramatica_slr1(gramatica, conjuntos_follow)

    # --- 3. Construcción de Tablas y Menú Interactivo ---
    tabla_ll1 = None
    tabla_slr1_acciones = None
    tabla_slr1_goto = None

    if es_ll1:
        tabla_ll1 = construir_tabla_ll1(gramatica, conjuntos_first, conjuntos_follow)
    if es_slr1:
        tabla_slr1_acciones, tabla_slr1_goto = construir_tabla_slr1(gramatica, conjuntos_follow)

    # Función auxiliar para llamar al parser correspondiente
    def parse_cadena(cadena, parser_type, verbose=False):
        if parser_type == 'll1':
            return parse_ll1(cadena, tabla_ll1, 'S', verbose)
        elif parser_type == 'slr1':
            return parse_slr1(cadena, tabla_slr1_acciones, tabla_slr1_goto, 'S', verbose)
        return False

    # Caso 1: La gramática es tanto LL(1) como SLR(1)
    if es_ll1 and es_slr1:
        print("Grammar is both LL(1) and SLR(1).")
        verbose_mode = input("Enable step-by-step view? (y/n): ").lower() == 'y'
        while True:
            seleccion = input("Select a parser (T: for LL(1), B: for SLR(1), Q: quit): ").upper()
            if seleccion == 'Q':
                break
            elif seleccion == 'T':
                parser_seleccionado = 'll1'
            elif seleccion == 'B':
                parser_seleccionado = 'slr1'
            else:
                print("Invalid selection.")
                continue
            
            # Bucle para analizar múltiples cadenas
            while True:
                cadena = input(f"Input string for {parser_seleccionado.upper()} parser (or press Enter to re-select): ")
                if not cadena:
                    break
                if parse_cadena(cadena, parser_seleccionado, verbose_mode):
                    print("yes")
                else:
                    print("no")

    # Caso 2: La gramática es solo LL(1)
    elif es_ll1:
        print("Grammar is LL(1).")
        verbose_mode = input("Enable step-by-step view? (y/n): ").lower() == 'y'
        while True:
            cadena = input("Input string to parse (or press Enter to quit): ")
            if not cadena:
                break
            if parse_cadena(cadena, 'll1', verbose_mode):
                print("yes")
            else:
                print("no")

    # Caso 3: La gramática es solo SLR(1)
    elif es_slr1:
        print("Grammar is SLR(1).")
        verbose_mode = input("Enable step-by-step view? (y/n): ").lower() == 'y'
        while True:
            cadena = input("Input string to parse (or press Enter to quit): ")
            if not cadena:
                break
            if parse_cadena(cadena, 'slr1', verbose_mode):
                print("yes")
            else:
                print("no")

    # Caso 4: La gramática no es ni LL(1) ni SLR(1)
    else:
        print("Grammar is neither LL(1) nor SLR(1).")

if __name__ == "__main__":
    main()
