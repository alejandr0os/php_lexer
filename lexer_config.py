"""
Configuración y definiciones del Analizador Léxico de PHP
===========================================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Este módulo contiene todas las constantes, configuraciones y definiciones
de palabras reservadas que utiliza el lexer de PHP construido con PLY.
"""


# Definición de estados del lexer
# El estado INITIAL corresponde al modo HTML fuera de tags PH
# El estado 'php' corresponde al interior de bloques <?php ... ?>
LEXER_STATES = (
    ('php', 'exclusive'),
)


# Palabras reservadas de PHP
# Estas palabras se reconocen sin distinguir mayúsculas de minúsculas,
# tal como lo hace el PHP real. Los nombres de tokens siguen la
# convención de PHP's token_get_all()

PALABRAS_RESERVADAS = {
    # Control de flujo: if, else, while, for, foreach, switch, etc.
    'if': 'T_IF',
    'else': 'T_ELSE',
    'elseif': 'T_ELSEIF',
    'endif': 'T_ENDIF',
    'while': 'T_WHILE',
    'endwhile': 'T_ENDWHILE',
    'do': 'T_DO',
    'for': 'T_FOR',
    'endfor': 'T_ENDFOR',
    'foreach': 'T_FOREACH',
    'endforeach': 'T_ENDFOREACH',
    'as': 'T_AS',
    'switch': 'T_SWITCH',
    'endswitch': 'T_ENDSWITCH',
    'case': 'T_CASE',
    'default': 'T_DEFAULT',
    'break': 'T_BREAK',
    'continue': 'T_CONTINUE',
    'goto': 'T_GOTO',
    'return': 'T_RETURN',

    # Manejo de excepciones: try, catch, finally, throw
    'try': 'T_TRY',
    'catch': 'T_CATCH',
    'finally': 'T_FINALLY',
    'throw': 'T_THROW',

    # Programación Orientada a Objetos
    'class': 'T_CLASS',
    'interface': 'T_INTERFACE',
    'trait': 'T_TRAIT',
    'enum': 'T_ENUM',
    'extends': 'T_EXTENDS',
    'implements': 'T_IMPLEMENTS',
    'abstract': 'T_ABSTRACT',
    'final': 'T_FINAL',
    'readonly': 'T_READONLY',
    'public': 'T_PUBLIC',
    'private': 'T_PRIVATE',
    'protected': 'T_PROTECTED',
    'static': 'T_STATIC',
    'var': 'T_VAR',
    'const': 'T_CONST',
    'new': 'T_NEW',
    'clone': 'T_CLONE',
    'instanceof': 'T_INSTANCEOF',
    'function': 'T_FUNCTION',
    'fn': 'T_FN',
    'namespace': 'T_NAMESPACE',
    'use': 'T_USE',
    'insteadof': 'T_INSTEADOF',

    # Construcciones del lenguaje: echo, print, isset, etc.
    'echo': 'T_ECHO',
    'print': 'T_PRINT',
    'eval': 'T_EVAL',
    'exit': 'T_EXIT',
    'die': 'T_EXIT',
    'isset': 'T_ISSET',
    'unset': 'T_UNSET',
    'empty': 'T_EMPTY',
    'list': 'T_LIST',
    'array': 'T_ARRAY',
    'callable': 'T_CALLABLE',
    'global': 'T_GLOBAL',
    'include': 'T_INCLUDE',
    'include_once': 'T_INCLUDE_ONCE',
    'require': 'T_REQUIRE',
    'require_once': 'T_REQUIRE_ONCE',
    'declare': 'T_DECLARE',
    'enddeclare': 'T_ENDDECLARE',
    'match': 'T_MATCH',
    'yield': 'T_YIELD',

    # Operadores de palabra: and, or, xor
    'and': 'T_LOGICAL_AND',
    'or': 'T_LOGICAL_OR',
    'xor': 'T_LOGICAL_XOR',

    # Literales especiales: true, false, null
    'true': 'T_TRUE',
    'false': 'T_FALSE',
    'null': 'T_NULL',
}


# Definición de los tipos de token
# Estos tokens incluyen:
# - Etiquetas HTML y de apertura/cierre de PHP
# - Identificadores y literales
# - Comentarios y atributos
# - Operadores de múltiples caracteres
# - Tokens de caracteres simples

TOKENS_BASICOS = [
    # Etiquetas y HTML inline
    'T_OPEN_TAG',
    'T_OPEN_TAG_WITH_ECHO',
    'T_CLOSE_TAG',
    'T_INLINE_HTML',

    # Identificadores y literales (variables, números, cadenas)
    'T_VARIABLE',
    'T_STRING',
    'T_LNUMBER',
    'T_DNUMBER',
    'T_CONSTANT_ENCAPSED_STRING',
    'T_HEREDOC',
    'T_NOWDOC',

    # Comentarios y atributos
    'T_COMMENT',
    'T_DOC_COMMENT',
    'T_ATTRIBUTE',

    # Operadores de múltiples caracteres
    'T_OBJECT_OPERATOR',
    'T_NULLSAFE_OBJECT_OPERATOR',
    'T_DOUBLE_ARROW',
    'T_DOUBLE_COLON',
    'T_ELLIPSIS',
    'T_INC',
    'T_DEC',
    'T_POW',
    'T_POW_EQUAL',
    'T_IS_EQUAL',
    'T_IS_IDENTICAL',
    'T_IS_NOT_EQUAL',
    'T_IS_NOT_IDENTICAL',
    'T_IS_SMALLER_OR_EQUAL',
    'T_IS_GREATER_OR_EQUAL',
    'T_SPACESHIP',
    'T_BOOLEAN_AND',
    'T_BOOLEAN_OR',
    'T_COALESCE',
    'T_COALESCE_EQUAL',
    'T_CONCAT_EQUAL',
    'T_PLUS_EQUAL',
    'T_MINUS_EQUAL',
    'T_MUL_EQUAL',
    'T_DIV_EQUAL',
    'T_MOD_EQUAL',
    'T_AND_EQUAL',
    'T_OR_EQUAL',
    'T_XOR_EQUAL',
    'T_SL_EQUAL',
    'T_SR_EQUAL',
    'T_SL',
    'T_SR',
    'T_NS_SEPARATOR',

    # Tokens de caracteres simples
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'SEMI',
    'COMMA',
    'COLON',
    'QUESTION',
    'AT',
    'BACKTICK',
    'DOLLAR',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'CONCAT',
    'EQUALS',
    'LT',
    'GT',
    'NOT',
    'AMP',
    'PIPE',
    'CARET',
    'TILDE',
]

# Construir la lista completa de tokens combinando
# los tokens básicos con las palabras reservadas
TOKENS_COMPLETOS = TOKENS_BASICOS + sorted(set(PALABRAS_RESERVADAS.values()))
