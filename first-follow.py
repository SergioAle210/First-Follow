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


def compute_follow(grammar, first, start_symbol):
    # Inicializamos FOLLOW para cada no terminal
    follow = {nonterm: set() for nonterm in grammar}
    # Regla 1: Si es el símbolo inicial, agregar '$'
    follow[start_symbol].add("$")

    changed = True
    while changed:
        changed = False
        # Para cada producción B -> α
        for left in grammar:
            for production in grammar[left]:
                # Recorremos la producción para buscar apariciones de no terminales
                for i, symbol in enumerate(production):
                    # Solo se calcula FOLLOW para no terminales (y se ignora 'λ')
                    if symbol in grammar and symbol != "λ":
                        beta = production[i + 1 :]
                        # Regla 2: Si hay beta, agregar FIRST(beta) sin 'λ'
                        first_beta = set()
                        for b in beta:
                            if b not in grammar:  # b es terminal
                                first_beta.add(b)
                                break
                            else:
                                first_beta.update(first[b] - {"λ"})
                                if "λ" in first[b]:
                                    continue
                                else:
                                    break
                        before = len(follow[symbol])
                        follow[symbol].update(first_beta)
                        if len(follow[symbol]) > before:
                            changed = True

                        # Regla 3: Si beta es vacío o beta =>* λ, se añade FOLLOW(B) (FOLLOW(left))
                        # La condición se cumple si beta está vacía o, para cada símbolo en beta,
                        # éste es no terminal y puede derivar la cadena vacía.
                        if not beta or (
                            beta and all(b in grammar and "λ" in first[b] for b in beta)
                        ):
                            before = len(follow[symbol])
                            follow[symbol].update(follow[left])
                            if len(follow[symbol]) > before:
                                changed = True
    return follow


first = compute_first(grammar)
# Cálculo de FIRST y FOLLOW para la gramática dada
follow = compute_follow(grammar, first, "E")


print("Conjuntos FIRST:")
for nonterm in first:
    print(f"{nonterm}: {first[nonterm]}")


print("\nConjuntos FOLLOW:")
for nonterm in follow:
    print(f"{nonterm}: {follow[nonterm]}")
