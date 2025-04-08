# Análisis de Gramática: Cálculo de FIRST y FOLLOW

Este programa implementa el análisis de una gramática libre de contexto para expresiones aritméticas y calcula automáticamente los conjuntos **FIRST** y **FOLLOW** de cada no terminal.

## Gramática Utilizada

La gramática que se analiza representa expresiones aritméticas con suma, multiplicación, paréntesis e identificadores.

Esta gramática se representa en el código mediante un diccionario en Python, donde cada no terminal está asociado con sus producciones.

## Funcionalidades del Programa

### 1. Cálculo del conjunto FIRST

Se implementa la función `compute_first(grammar)` que calcula el conjunto **FIRST** de cada no terminal. Este conjunto contiene los símbolos terminales que pueden aparecer al inicio de alguna cadena derivada a partir del no terminal.

**Lógica:**

- Se inicializa un diccionario vacío para cada no terminal.
- Para cada producción:
  - Si la producción es \( \lambda \), se agrega \( \lambda \) al conjunto FIRST.
  - Si el primer símbolo es terminal, se agrega directamente.
  - Si es no terminal, se agregan sus símbolos del conjunto FIRST (excepto \( \lambda \)), y si este puede derivar \( \lambda \), se continúa con el siguiente símbolo.

### 2. Cálculo del conjunto FOLLOW

Se implementa la función `compute_follow(grammar, first, start_symbol)` para calcular el conjunto **FOLLOW** de cada no terminal. Este conjunto contiene los símbolos terminales que pueden aparecer inmediatamente después del no terminal en alguna derivación válida.

**Lógica:**

- Se inicializa un diccionario vacío para cada no terminal.
- Se añade el símbolo especial \$ al conjunto FOLLOW del símbolo inicial.
- Se recorren todas las producciones:
  - Si un no terminal es seguido por una cadena \( \beta \), se añade el conjunto FIRST de \( \beta \) (excepto \( \lambda \)).
  - Si \( \beta \) puede derivar \( \lambda \), se añade el conjunto FOLLOW del no terminal izquierdo de la producción.

## 🧪 Ejecución y Resultados

El programa ejecuta ambas funciones `compute_first` y `compute_follow` usando la gramática proporcionada, e imprime los resultados por pantalla.


