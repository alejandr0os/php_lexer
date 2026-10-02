"""
Constructor del Analizador Léxico de PHP
==========================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Este módulo es responsable de:
1. Importar todas las reglas y configuraciones
2. Construir el lexer usando PLY
3. Proporcionar funciones para tokenizar código PHP

La construcción del lexer debe hacerse una sola vez, por lo que
se realiza al momento de importar este módulo.
"""

import sys

try:
    import ply.lex as lex
except ImportError:
    sys.exit("PLY es requerido: pip install ply")

# Importar configuración y excepciones
from lexer_config import LEXER_STATES
from lexer_config import TOKENS_COMPLETOS
from lexer_excepciones import PHPLexError

# Importar todas las reglas (esto los registra en PLY)
import lexer_reglas


def construir_lexer():
    """
    Construye y retorna una instancia del lexer de PHP

    El proceso:
    1. Configura los estados (INITIAL para HTML, 'php' para código PHP)
    2. Configura la lista de tokens
    3. Usa ply.lex.lex() para generar el lexer automáticamente
       a partir de las reglas definidas en lexer_reglas

    Retorna:
        Un objeto lexer de PLY configurado y listo para usar
    """
    lexer_reglas.states = LEXER_STATES
    lexer_reglas.tokens = TOKENS_COMPLETOS

    lexer_generado = lex.lex(module=lexer_reglas)
    return lexer_generado


# Construir una única instancia del lexer (singleton)
# Esta instancia se reutiliza para todas las tokenizaciones
lexer = construir_lexer()


def obtener_lexer():
    """
    Retorna la instancia global del lexer

    Se proporciona como función para permitir acceso controlado
    a la instancia única del lexer.

    Retorna:
        La instancia global del lexer de PHP
    """
    return lexer
