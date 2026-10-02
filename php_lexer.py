#!/usr/bin/env python3
"""
Analizador Léxico para PHP construido con PLY
================================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Descripción:
    Este módulo implementa un análisis léxico completo para PHP
    utilizando PLY.

    El lexer es modular y organizado en los siguientes componentes:
    - lexer_config: Configuración y definiciones de palabras reservadas
    - lexer_excepciones: Excepciones personalizadas
    - lexer_reglas: Todas las reglas de tokenización
    - lexer_builder: Constructor del lexer
    - lexer_analizador: Funciones de análisis de nivel superior

Instalación:
    pip install ply

Uso como línea de comandos:
    python php_lexer.py                        # Analizar programa demo
    python php_lexer.py archivo.php            # Analizar archivo PHP

Uso como biblioteca:
    from php_lexer import analizar
    tokens = analizar(open('pagina.php').read())
"""

import sys
from lexer_analizador import (
    analizar, mostrar_tokens, resumir_tokens, obtener_errores, mostrar_errores
)
from demo import DEMO_PHP


def main():
    """
    Función principal - punto de entrada para el programa

    Proceso:
    1. Verifica los argumentos de línea de comandos
    2. Si se proporciona un archivo, lo abre y lo lee
    3. Si no, utiliza el código PHP de demostración
    4. Analiza el código obteniendo los tokens
    5. Muestra los tokens en formato tabular
    6. Genera un resumen con estadísticas
    """

    # Determinar la fuente de código a analizar
    if len(sys.argv) > 1:
        # Se proporcionó un archivo como argumento
        try:
            with open(sys.argv[1], encoding='utf-8', errors='replace') as fh:
                codigo_fuente = fh.read()
        except OSError as excepcion:
            sys.exit(f"No se puede leer {sys.argv[1]}: {excepcion}")
    else:
        # Sin archivo - usar el código de demostración
        print('(Sin archivo - analizando código de demostración)\n')
        codigo_fuente = DEMO_PHP

    # Realizar el análisis léxico
    flujo_tokens = analizar(codigo_fuente)

    # Mostrar los tokens encontrados
    mostrar_tokens(flujo_tokens)

    # Mostrar estadísticas
    resumir_tokens(flujo_tokens)

    # Mostrar los errores léxicos acumulados durante el análisis
    errores = obtener_errores()
    mostrar_errores(errores, codigo_fuente)

    # Código de salida distinto de 0 si hubo errores (útil en scripts/CI)
    if errores:
        sys.exit(1)


if __name__ == '__main__':
    main()
