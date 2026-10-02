"""
Errores y excepciones del Analizador Léxico de PHP
====================================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Define:
- PHPLexError: excepción para fallos estructurales del lexer.
- ErrorLexico: registro de un error léxico (tipo, mensaje, línea, columna).
- Tipos de error léxico reconocidos.
- registrar_error(): lo usan las reglas para ACUMULAR errores (en vez de
  imprimirlos al vuelo) y poder reportarlos todos, ordenados, al final.
"""

from dataclasses import dataclass


class PHPLexError(Exception):
    """Excepción para fallos estructurales del lexer (uso interno)."""
    pass


# ----------------------------------------------------------------------------
# Tipos de error léxico
# ----------------------------------------------------------------------------
CARACTER_ILEGAL = 'CARACTER_ILEGAL'              # símbolo fuera del alfabeto
CADENA_SIN_CERRAR = 'CADENA_SIN_CERRAR'          # "texto  o  'texto
COMENTARIO_SIN_CERRAR = 'COMENTARIO_SIN_CERRAR'  # /* sin */
NUMERO_MAL_FORMADO = 'NUMERO_MAL_FORMADO'        # 0x, 0b2, 123abc, 1.2.3 ...
VARIABLE_INVALIDA = 'VARIABLE_INVALIDA'          # $1abc
HEREDOC_MALFORMADO = 'HEREDOC_MALFORMADO'        # <<< sin etiqueta válida
HEREDOC_SIN_CERRAR = 'HEREDOC_SIN_CERRAR'        # falta la línea de cierre


@dataclass
class ErrorLexico:
    tipo: str
    mensaje: str
    linea: int
    columna: int
    lexema: str = ''


def calcular_posicion(datos, lexpos):
    """Devuelve (línea, columna), ambas desde 1, de una posición absoluta."""
    linea = datos.count('\n', 0, lexpos) + 1
    inicio_linea = datos.rfind('\n', 0, lexpos) + 1
    return linea, lexpos - inicio_linea + 1


def registrar_error(lexer, tipo, mensaje, lexpos, lexema=''):
    """Agrega un ErrorLexico a la lista lexer.errores."""
    linea, columna = calcular_posicion(lexer.lexdata, lexpos)
    if not hasattr(lexer, 'errores'):
        lexer.errores = []
    lexer.errores.append(ErrorLexico(tipo, mensaje, linea, columna, lexema))
