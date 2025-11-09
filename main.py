from first import calcular_conjuntos_first
from follow import calcular_conjuntos_follow
from verificador_ll1 import es_gramatica_ll1, calcular_first_de_produccion
from verificador_slr1 import es_gramatica_slr1
from tabla_ll1 import construir_tabla_ll1
from parser_ll1 import parse_ll1
from parser_slr1 import construir_tabla_slr1, parse_slr1

def analizar_gramatica_input(texto_entrada):
    """
    Analiza el texto de entrada para extraer la gramatica.
    Formato esperado:
    - N
    - S -> a S b | c
    - ...
    """
    lineas = texto_entrada.strip().splitlines()
    num_no_terminales = int(lineas[0])
    gramatica = {}
    
    for i in range(1, num_no_terminales + 1):
        linea = lineas[i]
        if '->' not in linea:
            continue
        
        no_terminal, producciones_str = linea.split('->', 1)
        no_terminal = no_terminal.strip()
        
        alternativas = producciones_str.split('|')
        
        producciones_finales = []
        for alt in alternativas:
            alt = alt.strip()
            if alt == 'e':
                producciones_finales.append('e')
            else:
                producciones_finales.append("".join(alt.split()))

        gramatica[no_terminal] = producciones_finales
            
    return gramatica

def main():
    """
    Funcion principal que orquesta el analisis de la gramatica y la interaccion con el usuario.
    """
    try:
        with open('input.txt', 'r') as archivo:
            texto_entrada = archivo.read()
    except FileNotFoundError:
        print("Error: No se encontro el archivo 'input.txt'.")
        return

    gramatica = analizar_gramatica_input(texto_entrada)
    
    if 'S' not in gramatica:
        print("Error: La gramatica debe contener un simbolo inicial 'S'.")
        return

    conjuntos_first = calcular_conjuntos_first(gramatica)

    conjuntos_follow = calcular_conjuntos_follow(gramatica, conjuntos_first)

    # Imprimir conjuntos First y Follow
    import json
    print("\n--- First Sets ---")
    for key, value in conjuntos_first.items():
        print(f'"{key}": {json.dumps(sorted(list(value)))}')

    print("\n--- Follow Sets ---")
    for key, value in conjuntos_follow.items():
        print(f'"{key}": {json.dumps(sorted(list(value)))}')
    print("--------------------\n")


    es_ll1 = es_gramatica_ll1(gramatica, conjuntos_first, conjuntos_follow)
    es_slr1 = es_gramatica_slr1(gramatica, conjuntos_follow)

    tabla_ll1 = None
    tabla_slr1_acciones = None
    tabla_slr1_goto = None

    if es_ll1:
        tabla_ll1 = construir_tabla_ll1(gramatica, conjuntos_first, conjuntos_follow)
    if es_slr1:
        tabla_slr1_acciones, tabla_slr1_goto = construir_tabla_slr1(gramatica, conjuntos_follow)

    def parse_cadena(cadena, parser_type, verbose=False):
        if parser_type == 'll1':
            return parse_ll1(cadena, tabla_ll1, 'S', verbose)
        elif parser_type == 'slr1':
            return parse_slr1(cadena, tabla_slr1_acciones, tabla_slr1_goto, 'S', verbose)
        return False

    if es_ll1 and es_slr1:
        print("Grammar is both LL(1) and SLR(1).")
        verbose_mode = input("Enable step-by-step view? (y/n): ").lower() == 'y'
        while True:
            seleccion = input("Select a parser (L: for LL(1), S: for SLR(1), Q: quit): ").upper()
            if seleccion == 'Q':
                break
            elif seleccion == 'L':
                parser_seleccionado = 'll1'
            elif seleccion == 'S':
                parser_seleccionado = 'slr1'
            else:
                print("Invalid selection.")
                continue
            
            while True:
                cadena = input(f"Input string for {parser_seleccionado.upper()} parser (or press Enter to re-select): ")
                if not cadena:
                    break
                if parse_cadena(cadena, parser_seleccionado, verbose_mode):
                    print("yes")
                else:
                    print("no")

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

    else:
        print("Grammar is neither LL(1) nor SLR(1).")

if __name__ == "__main__":
    main()