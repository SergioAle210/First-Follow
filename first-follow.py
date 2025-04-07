# Gramática para expresiones aritméticas que vimos en clase
# E  -> T E'
# E' -> + T E' | λ
# T  -> F T'
# T' -> * F T' | λ
# F  -> ( E ) | id

# Definición de la gramática como un diccionario
grammar = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["λ"]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["λ"]],
    "F": [["(", "E", ")"], ["id"]],
}


# Función para calcular el conjunto FIRST de una gramática
# El conjunto FIRST de un no terminal es el conjunto de símbolos terminales que pueden aparecer al inicio de una cadena derivada de ese no terminal.
def compute_first(grammar):
    # Inicializamos FIRST para cada no terminal
    first = {nonterm: set() for nonterm in grammar}

    # Función auxiliar para determinar si un símbolo es terminal
    def is_terminal(symbol):
        return symbol not in grammar or symbol == "λ"

    changed = True
    while changed:
        changed = False
        # Recorremos cada no terminal y sus producciones
        for nonterm in grammar:
            for production in grammar[nonterm]:
                # Si la producción es la cadena vacía, agregamos 'λ'
                if production == ["λ"]:
                    if "λ" not in first[nonterm]:
                        first[nonterm].add("λ")
                        changed = True
                    continue
                # Recorremos los símbolos de la producción
                for i, symbol in enumerate(production):
                    if is_terminal(symbol):
                        if symbol not in first[nonterm]:
                            first[nonterm].add(symbol)
                            changed = True
                        break  # terminamos la producción actual
                    else:
                        before = len(first[nonterm])
                        first[nonterm].update(first[symbol] - {"λ"})
                        if len(first[nonterm]) > before:
                            changed = True
                        if "λ" in first[symbol]:
                            if i == len(production) - 1:
                                if "λ" not in first[nonterm]:
                                    first[nonterm].add("λ")
                                    changed = True
                            continue
                        else:
                            break
    return first


first = compute_first(grammar)


print("Conjuntos FIRST:")
for nonterm in first:
    print(f"{nonterm}: {first[nonterm]}")
