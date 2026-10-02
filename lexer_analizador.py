"""
Analizador del Analizador Léxico de PHP
========================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Este módulo proporciona funciones de alto nivel para:
1. Analizar código PHP y obtener tokens
2. Mostrar los tokens en formato tabular
3. Generar estadísticas sobre los tokens encontrados
"""

import re
import sys
from collections import Counter

from lexer_builder import obtener_lexer
from lexer_excepciones import PHPLexError, registrar_error


def analizar(codigo_fuente):
    """
    Tokeniza un fragmento de código PHP

    Parámetros:
        codigo_fuente: Un string contenant code PHP o HTML con bloques PHP

    Proceso:
        1. Obtiene la instancia global del lexer
        2. Configura el lexer con el código fuente
        3. Determina el estado inicial:
           - INITIAL si el código contiene tags <?
           - 'php' si el código es PHP puro sin tags
        4. Extrae todos los tokens
        5. Captura cualquier PHPLexError y lo reporta

    Retorna:
        Una lista de tokens encontrados en el código fuente.
        Si hay errores, se reportan en stderr y se retorna
        la lista de tokens encontrados hasta el error.
    """
    lexer = obtener_lexer()
    lexer.input(codigo_fuente)
    lexer.lineno = 1  # reiniciar el contador de líneas en cada análisis
    lexer.errores = []  # reiniciar los errores léxicos acumulados

    # Detectar el estado inicial:
    # Si hay un tag PHP explícito, comenzar en INITIAL modo HTML
    # De lo contrario, asumir que es código PHP puro
    if re.search(r'<\?', codigo_fuente):
        lexer.begin('INITIAL')
    else:
        lexer.begin('php')

    # Extraer todos los tokens
    flujo_tokens = []
    try:
        while True:
            token = lexer.token()
            if token is None:
                break
            flujo_tokens.append(token)
    except PHPLexError as error:
        # Fallo estructural inesperado: se registra como un error más
        registrar_error(lexer, 'ERROR_INTERNO', str(error), lexer.lexpos)

    return flujo_tokens


def obtener_errores():
    """Errores léxicos del último análisis, en orden de aparición."""
    return list(getattr(obtener_lexer(), 'errores', []))


def mostrar_errores(errores, codigo_fuente=None):
    """
    Imprime el reporte de errores léxicos.

    Por cada error: número, posición (línea:columna), tipo, descripción y,
    si se pasa el código fuente, la línea afectada con una flecha (^)
    señalando la columna exacta.
    """
    print('\nERRORES LÉXICOS')
    print('-' * 74)

    if not errores:
        print('  Sin errores léxicos.')
        return

    lineas = codigo_fuente.splitlines() if codigo_fuente else []

    for i, e in enumerate(errores, 1):
        print(f"  [{i}] línea {e.linea}, columna {e.columna}  {e.tipo}")
        print(f"      {e.mensaje}")
        if 1 <= e.linea <= len(lineas):
            texto = lineas[e.linea - 1].replace('\t', ' ')
            print(f"      {e.linea:>4} | {texto}")
            print(f"           | {' ' * (e.columna - 1)}^")

    por_tipo = Counter(e.tipo for e in errores)
    print('-' * 74)
    print(f"  {len(errores)} error(es): " +
          ', '.join(f"{t} x{n}" for t, n in sorted(por_tipo.items())))


def mostrar_tokens(flujo_tokens):
    """
    Imprime los tokens en un formato tabular legible

    Muestra:
        - Número de línea de cada token
        - Posición en el archivo (lexpos)
        - Tipo de token
        - Valor del token (lexema)

    Parámetros:
        flujo_tokens: Lista de tokens a mostrar
    """
    print(f"{'LÍNEA':>4} {'POS':>6}  {'TIPO':<32}LEXEMA")
    print('-' * 74)

    for token in flujo_tokens:
        # Obtener el valor del token como string
        lexema = repr(str(token.value))

        # Si el lexema es muy largo, truncarlo con puntos suspensivos
        if len(lexema) > 38:
            lexema = lexema[:35] + '...'

        print(f"{token.lineno:>4} {token.lexpos:>6}  {token.type:<32}{lexema}")

    print('-' * 74)
    print(f"{len(flujo_tokens)} tokens")


def resumir_tokens(flujo_tokens):
    """
    Genera y muestra estadísticas sobre los tokens

    Muestra:
        1. Frecuencia de cada tipo de token
        2. Total de tokens
        3. Identificadores únicos encontrados
        4. Variables únicas encontradas

    Parámetros:
        flujo_tokens: Lista de tokens a analizar
    """
    # Contar la frecuencia de cada tipo de token
    frecuencias = Counter(t.type for t in flujo_tokens)

    print('\nFRECUENCIA DE TOKENS')
    print('-' * 74)

    for tipo_token, cantidad in sorted(frecuencias.items()):
        print(f"  {tipo_token:<32}{cantidad:>5}")

    print(f"  {'TOTAL':<32}{len(flujo_tokens):>5}")

    # Extraer identificadores y variables únicas
    identificadores = sorted(
        set(t.value for t in flujo_tokens if t.type == 'T_STRING')
    )
    variables = sorted(
        set(t.value for t in flujo_tokens if t.type == 'T_VARIABLE')
    )

    # Mostrar identificadores
    print(f"\n  IDENTIFICADORES ({len(identificadores)}): " +
          f"{', '.join(identificadores) or '-'}")

    # Mostrar variables
    print(f"  VARIABLES   ({len(variables)}): " +
          f"{', '.join(variables) or '-'}")
