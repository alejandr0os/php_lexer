"""
Reglas y funciones del Analizador Léxico de PHP
================================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Este módulo contiene todas las reglas de tokenización, tokens de caracteres
simples, operadores, palabras clave, etc. utilizadas por el lexer de PHP.

Las reglas en PLY se definen como:
- Strings para expresiones regulares simples (t_php_TOKEN)
- Funciones para lógica más compleja (t_php_TOKEN_FUNCTION)
"""

import re
import sys
from lexer_config import PALABRAS_RESERVADAS
from lexer_excepciones import (
    registrar_error,
    CARACTER_ILEGAL, CADENA_SIN_CERRAR, COMENTARIO_SIN_CERRAR,
    NUMERO_MAL_FORMADO, VARIABLE_INVALIDA,
    HEREDOC_MALFORMADO, HEREDOC_SIN_CERRAR,
)


def _resumen(texto, maximo=30):
    """Recorta un lexema largo para mostrarlo en un mensaje de error."""
    texto = texto.replace('\n', '\\n')
    return texto if len(texto) <= maximo else texto[:maximo] + '...'


# ============================================================================
# 1. MODO HTML - Reglas para contenido fuera de tags PHP
# ============================================================================

def t_open_tag(t):
    # Reconoce las etiquetas de apertura de PHP: <?php, <?, <?=
    #
    # Cuando se encuentra una etiqueta de apertura:
    # - Cambia el estado del lexer de INITIAL a 'php'
    # - Determina si es una etiqueta con echo (<?=) o normal (<?php o <?)
    #
    r'<\?[pP][hH][pP]\b|<\?=|<\?'
    t.lexer.begin('php')
    t.type = 'T_OPEN_TAG_WITH_ECHO' if '=' in t.value else 'T_OPEN_TAG'
    return t


def t_inline_html(t):
    # Reconoce cualquier texto que NO sea una etiqueta de apertura PHP
    #
    # El contenido HTML se mantiene como un único token.
    # Se actualiza el contador de líneas para mantener la precisión
    # en los números de línea reportados.
    #
    r'(?:[^<]|<(?!\?))+'
    t.type = 'T_INLINE_HTML'
    t.lexer.lineno += t.value.count('\n')
    return t


# ============================================================================
# 2. MODO PHP - Etiqueta de cierre y espacios en blanco
# ============================================================================

def t_php_T_CLOSE_TAG(t):
    # Reconoce la etiqueta de cierre PHP: ?>
    #
    # Cuando se encuentra, cambia el estado del lexer de 'php' a INITIAL
    # (volviendo al modo HTML).
    #
    r'\?>'
    t.lexer.begin('INITIAL')
    return t


# Los espacios en blanco en modo PHP se ignoran
# (espacios, tabulaciones, retornos de carro, etc.)
t_php_ignore = ' \t\r\f\v'


def t_php_newline(t):
    # Maneja los saltos de línea dentro del código PHP
    #
    # Los saltos de línea se cuentan pero no se emiten como tokens.
    # Esto mantiene preciso el contador de líneas del lexer.
    #
    r'\n+'
    t.lexer.lineno += len(t.value)
    # No retornamos nada - el token se descarta


# ============================================================================
# 3. ATRIBUTOS PHP 8 y COMENTARIOS
# ============================================================================

def t_php_T_ATTRIBUTE(t):
    # Reconoce los atributos de PHP 8: #[
    #
    # Los atributos son anotaciones que se pueden aplicar a clases,
    # funciones, parámetros, etc. en PHP 8+
    #
    r'\#\['
    return t


def t_php_T_COMMENT(t):
    # Reconoce comentarios en PHP: //, #, y /* */
    #
    # Las reglas de comentario:
    # - Comentarios de una línea: // y #
    # - Comentarios de bloque: /* ... */
    # - Los comentarios /** */ se clasifican como T_DOC_COMMENT
    # - Los demás se clasifican como T_COMMENT
    #
    r'//(?:(?!\?>)[^\n])*|\#(?:(?!\?>)[^\n])*|/\*[\s\S]*?\*/'
    t.type = 'T_DOC_COMMENT' if t.value.startswith('/**') else 'T_COMMENT'
    t.lexer.lineno += t.value.count('\n')
    return t


def t_php_ERR_COMENTARIO(t):
    # ERROR LÉXICO: comentario de bloque que abre con /* y nunca cierra con */
    #
    # Solo se llega aquí si T_COMMENT (que exige el cierre */) no coincidió.
    # Se consume hasta el final del archivo, igual que haría PHP.
    #
    r'/\*[\s\S]*'
    registrar_error(
        t.lexer, COMENTARIO_SIN_CERRAR,
        "comentario de bloque sin cerrar: falta '*/'",
        t.lexpos, _resumen(t.value)
    )
    t.lexer.lineno += t.value.count('\n')
    # No se retorna token: el texto del comentario se descarta


# ============================================================================
# 4. LITERALES: Cadenas, números y variables
# ============================================================================

def t_php_T_CONSTANT_ENCAPSED_STRING(t):
    # Reconoce cadenas entre comillas: 'texto' o "texto"
    #
    # Caracteres especiales:
    # - En comillas simples: solo \' y \\ son especiales
    # - En comillas dobles: toda la cadena se mantiene como un único token
    # (sin interpolación en esta fase de análisis léxico)
    #
    r'''
    '([^'\\]|\\[\s\S])*'   # Comillas simples
    |
    "([^"\\]|\\[\s\S])*"   # Comillas dobles
    '''
    # Las cadenas pueden ocupar varias líneas: mantener el contador al día
    t.lexer.lineno += t.value.count('\n')
    return t


def t_php_ERR_CADENA(t):
    # ERROR LÉXICO: cadena que abre con ' o " y nunca se cierra
    #
    # Solo se llega aquí si la regla anterior (que exige la comilla de cierre)
    # no coincidió. Se consume hasta el final del archivo, como PHP.
    #
    r'''
    '([^'\\]|\\[\s\S])*
    |
    "([^"\\]|\\[\s\S])*
    '''
    tipo = 'simples' if t.value[0] == "'" else 'dobles'
    registrar_error(
        t.lexer, CADENA_SIN_CERRAR,
        f"cadena entre comillas {tipo} sin cerrar: falta {t.value[0]}",
        t.lexpos, _resumen(t.value)
    )
    t.lexer.lineno += t.value.count('\n')
    # No se retorna token


def t_php_T_LNUMBER(t):
    # Reconoce números: enteros (hexadecimales, binarios, octales, decimales)
    # y números flotantes (incluyendo notación científica)
    #
    # Formatos soportados:
    # - Hexadecimal:   0x1AF, 0X1AF
    # - Binario:       0b1010
    # - Octal:         0o755, 0755 (formato antiguo)
    # - Decimal:       1_000_000 (con separadores)
    # - Flotante:      3.14, 6.02e23, 3.14e-2
    #
    # PHP permite separadores de dígitos (_) para legibilidad.
    # Se clasifica como T_DNUMBER si es un flotante, T_LNUMBER si es entero.
    #
    # DETECCIÓN DE ERRORES: la regla captura todo lo que "parece" un número
    # (un dígito seguido de letras, dígitos, '_' o puntos con dígito detrás) y
    # DESPUÉS lo valida con _NUMERO_VALIDO. Así, '123abc', '0x', '0b102',
    # '1.2.3' o '089' se reportan como UN error en lugar de partirse en
    # tokens falsos (por ejemplo T_LNUMBER + T_STRING).
    #
    r'[0-9](?:[0-9a-zA-Z_\x80-\xff]|\.(?=[0-9])|(?<=[eE])[+-](?=[0-9]))*'
    v = t.value

    # '0xE+1' es 14 + 1: el signo no pertenece a un literal hexadecimal
    signo = re.search(r'[+-]', v)
    if signo and v[:2].lower() == '0x':
        v = t.value = v[:signo.start()]
        t.lexer.lexpos = t.lexpos + len(v)

    if not _numero_valido(v):
        registrar_error(
            t.lexer, NUMERO_MAL_FORMADO,
            f"número mal formado '{_resumen(v)}': {_motivo_numero_invalido(v)}",
            t.lexpos, _resumen(v)
        )
        return None

    # Determinar si es un número flotante o entero
    if '.' in v or (('e' in v or 'E' in v) and v[:2].lower() != '0x'):
        t.type = 'T_DNUMBER'
    else:
        t.type = 'T_LNUMBER'
    return t


_NUMERO_VALIDO = re.compile(r'''
    (?:
        0[xX][0-9a-fA-F][0-9a-fA-F_]*         # Hexadecimal
      | 0[bB][01][01_]*                       # Binario
      | 0[oO][0-7][0-7_]*                     # Octal (nuevo)
      | 0[0-7][0-7_]*                         # Octal (antiguo)
      | [0-9][0-9_]*\.[0-9][0-9_]*            # Flotante básico
        (?:[eE][+-]?[0-9][0-9_]*)?            # Con exponente opcional
      | [0-9][0-9_]*[eE][+-]?[0-9][0-9_]*     # Notación científica
      | [0-9][0-9_]*                          # Decimal simple
    )
''', re.VERBOSE)


def _numero_valido(v):
    """True si v es un literal numérico completo y bien formado."""
    if not _NUMERO_VALIDO.fullmatch(v):
        return False
    # Octal antiguo con dígito 8 o 9 (ej. 089); un flotante como 09.5 sí vale
    if re.fullmatch(r'0[0-9_]*[89][0-9_]*', v):
        return False
    # El separador '_' solo puede ir ENTRE dígitos
    if '__' in v or v.endswith('_'):
        return False
    if v[:2].lower() != '0x' and re.search(r'_[.eE]|[.eE]_|[.eE][+-]_', v):
        return False
    return True


def _motivo_numero_invalido(v):
    """Explica por qué un literal numérico no es válido."""
    prefijo = v[:2].lower()
    if '__' in v or v.endswith('_'):
        return "el separador '_' debe ir entre dos dígitos"
    if prefijo == '0x':
        return "literal hexadecimal inválido (se esperan dígitos 0-9 y a-f)"
    if prefijo == '0b':
        return "literal binario inválido (solo se permiten 0 y 1)"
    if prefijo == '0o' or re.fullmatch(r'0[0-9_]+', v):
        return "literal octal inválido (solo se permiten dígitos 0-7)"
    if re.fullmatch(r'[0-9][0-9_]*[A-Za-z\x80-\xff][A-Za-z0-9_\x80-\xff]*', v):
        return "identificador pegado a un número (¿falta un operador o un espacio?)"
    return "formato numérico inválido"


def t_php_T_VARIABLE(t):
    # Reconoce variables PHP: $nombre, $this, etc.
    #
    # Una variable comienza con $ seguido de:
    # - Una letra o guion bajo
    # - Caracteres de 8 bits, para caracteres no ASCII
    # - Seguido de letras, números, guiones bajos o caracteres de 8 bits
    #
    r'\$[a-zA-Z_\x80-\xff][a-zA-Z0-9_\x80-\xff]*'
    return t


def t_php_ERR_VARIABLE(t):
    # ERROR LÉXICO: variable cuyo nombre empieza con un dígito ($1abc)
    #
    # Sin esta regla se partiría en DOLLAR + número, sin avisar del problema.
    #
    r'\$[0-9][a-zA-Z0-9_\x80-\xff]*'
    registrar_error(
        t.lexer, VARIABLE_INVALIDA,
        f"nombre de variable inválido '{t.value}': no puede empezar con un dígito",
        t.lexpos, t.value
    )
    # No se retorna token


def t_php_T_STRING(t):
    # Reconoce identificadores y palabras clave
    #
    # Un identificador comienza con letra o guion bajo,
    # seguido de letras, números, guiones bajos o caracteres de 8 bits.
    #
    # Si el identificador coincide con una palabra reservada (sin distinguir
    # mayúsculas/minúsculas), se clasifica como la correspondiente palabra clave.
    # De lo contrario, se clasifica como T_STRING.
    #
    r'[a-zA-Z_\x80-\xff][a-zA-Z0-9_\x80-\xff]*'
    # Buscar en palabras reservadas case-insensitive
    t.type = PALABRAS_RESERVADAS.get(t.value.lower(), 'T_STRING')
    return t


# ============================================================================
# 5. HEREDOC y NOWDOC, documentos incrustados
# ============================================================================

def t_php_T_HEREDOC(t):
    # Reconoce heredoc y nowdoc: <<<ID ... ID  y  <<<'ID' ... ID
    #
    # Heredoc permite interpolación de variables:
    # $x = <<<EOT
    # Contenido con $variables
    # EOT;
    #
    # Nowdoc (entre comillas simples) no permite interpolación:
    # $x = <<<'EOT'
    # Contenido sin $interpolación
    # EOT;
    #
    # El lexer manual busca:
    # 1. La línea de encabezado con la etiqueta (ID)
    # 2. Todas las líneas de contenido
    # 3. La línea de terminación (que comienza con la etiqueta)
    #
    # No se puede usar una sola expresión regular para esto porque
    # se necesita una referencia hacia atrás a la etiqueta de inicio.
    #
    r'<<<'
    lexer = t.lexer
    data = lexer.lexdata

    # Encontrar el final de la línea de encabezado
    nl = data.find('\n', lexer.lexpos)
    header = data[lexer.lexpos:nl] if nl >= 0 else data[lexer.lexpos:]

    # Validar formato: <<<EOT o <<<'EOT' o <<<EOT (con espacios)
    m = re.match(
        r"[ \t]*(?P<q>['\"]?)(?P<label>[A-Za-z_]\w*)(?P=q)[ \t]*\r?$",
        header
    )
    if not m:
        # ERROR LÉXICO recuperable: se registra, se descarta el resto de la
        # línea del encabezado y el análisis continúa en la línea siguiente.
        registrar_error(
            lexer, HEREDOC_MALFORMADO,
            "encabezado heredoc/nowdoc malformado después de '<<<': "
            "se esperaba <<<ETIQUETA o <<<'ETIQUETA' y luego un salto de línea",
            t.lexpos, _resumen('<<<' + header.strip())
        )
        lexer.lexpos = nl if nl >= 0 else len(data)
        return None

    label, nowdoc = m.group('label'), m.group('q') == "'"

    # Crear patrón para la línea de terminación
    term = re.compile(r'[ \t]*' + re.escape(label) + r'(?![A-Za-z0-9_])')

    # Buscar la línea de terminación
    body_start, end, pos = nl + 1, -1, nl + 1
    while pos <= len(data):
        line_end = data.find('\n', pos)
        if line_end < 0:
            line_end = len(data)

        # ¿Coincide la línea actual con el patrón de terminación?
        if term.match(data, pos, line_end):
            end = pos
            break

        if line_end == len(data):
            break

        pos = line_end + 1

    if end < 0:
        # ERROR LÉXICO: no existe la línea de cierre. Se consume hasta el
        # final del archivo (todo lo que sigue sería contenido del heredoc).
        registrar_error(
            lexer, HEREDOC_SIN_CERRAR,
            f"heredoc/nowdoc '{label}' sin cerrar: no se encontró la línea "
            f"que termina con '{label}'",
            t.lexpos, _resumen('<<<' + header.strip())
        )
        lexer.lineno += data[t.lexpos:].count('\n')
        lexer.lexpos = len(data)
        return None

    # Extraer el contenido y clasificar el token
    t.value = data[body_start:end]
    lexer.lexpos = term.match(data, end).end()
    lexer.lineno += data[t.lexpos:lexer.lexpos].count('\n')
    t.type = 'T_NOWDOC' if nowdoc else 'T_HEREDOC'
    return t


# ============================================================================
# 6. OPERADORES DE MÚLTIPLES CARACTERES
# ============================================================================
# PLY ordena automáticamente estas reglas de más largo a más corto,
# asegurando que === se intente antes de == antes de =, etc.

# Operadores de 3+ caracteres
t_php_T_NULLSAFE_OBJECT_OPERATOR = r'\?->'        # ?->
t_php_T_COALESCE_EQUAL            = r'\?\?='      # ??=
t_php_T_SPACESHIP                 = r'<=>'        # <=>
t_php_T_IS_IDENTICAL              = r'==='        # ===
t_php_T_IS_NOT_IDENTICAL          = r'!=='        # !==
t_php_T_SL_EQUAL                  = r'<<='        # <<=
t_php_T_SR_EQUAL                  = r'>>='        # >>=
t_php_T_POW_EQUAL                 = r'\*\*='      # **=

# Operadores de 2 caracteres
t_php_T_IS_SMALLER_OR_EQUAL       = r'<='         # <=
t_php_T_IS_GREATER_OR_EQUAL       = r'>='         # >=
t_php_T_BOOLEAN_AND               = r'&&'         # &&
t_php_T_BOOLEAN_OR                = r'\|\|'       # ||
t_php_T_POW                       = r'\*\*'       # **
t_php_T_CONCAT_EQUAL              = r'\.='        # .=
t_php_T_PLUS_EQUAL                = r'\+='        # +=
t_php_T_MINUS_EQUAL               = r'-='         # -=
t_php_T_MUL_EQUAL                 = r'\*='        # *=
t_php_T_DIV_EQUAL                 = r'/='         # /=
t_php_T_MOD_EQUAL                 = r'%='         # %=
t_php_T_AND_EQUAL                 = r'&='         # &=
t_php_T_OR_EQUAL                  = r'\|='        # |=
t_php_T_XOR_EQUAL                 = r'\^='        # ^=
t_php_T_SL                        = r'<<'         # <<
t_php_T_SR                        = r'>>'         # >>
t_php_T_IS_EQUAL                  = r'=='         # ==
t_php_T_IS_NOT_EQUAL              = r'!=(?!=)|<>' # != <>  (no consume el '!=' de '!==')
t_php_T_DOUBLE_ARROW              = r'=>'         # =>
t_php_T_OBJECT_OPERATOR           = r'->'         # ->
t_php_T_DOUBLE_COLON              = r'::'         # ::
t_php_T_ELLIPSIS                  = r'\.\.\.'     # ...
t_php_T_COALESCE                  = r'\?\?'       # ??
t_php_T_NS_SEPARATOR              = r'\\'         # \ (separador de namespace)
t_php_T_INC                       = r'\+\+'       # ++
t_php_T_DEC                       = r'--'         # --


# ============================================================================
# 7. DELIMITADORES Y OPERADORES DE UN CARÁCTER
# ============================================================================

t_php_LPAREN                      = r'\('
t_php_RPAREN                      = r'\)'
t_php_LBRACE                      = r'\{'
t_php_RBRACE                      = r'\}'
t_php_LBRACKET                    = r'\['
t_php_RBRACKET                    = r'\]'
t_php_SEMI                        = r';'
t_php_COMMA                       = r','
t_php_COLON                       = r':'
t_php_QUESTION                    = r'\?'
t_php_AT                          = r'@'         # Supresión de errores
t_php_BACKTICK                    = r'`'
t_php_DOLLAR                      = r'\$'        # Para $$variable
t_php_PLUS                        = r'\+'
t_php_MINUS                       = r'-'
t_php_TIMES                       = r'\*'
t_php_DIVIDE                      = r'/'
t_php_MOD                         = r'%'
t_php_CONCAT                      = r'\.'
t_php_EQUALS                      = r'='
t_php_LT                          = r'<'
t_php_GT                          = r'>'
t_php_NOT                         = r'!'
t_php_AMP                         = r'&'
t_php_PIPE                        = r'\|'
t_php_CARET                       = r'\^'
t_php_TILDE                       = r'~'


# ============================================================================
# 8. MANEJO DE ERRORES LÉXICOS
# ============================================================================

def t_php_error(t):
    """
    Carácter que ninguna regla reconoce en modo PHP (por ejemplo ¿ § € ¬).

    Se registra como ErrorLexico (con línea y columna) y se salta ese único
    carácter para seguir analizando el resto del archivo.
    """
    _caracter_ilegal(t)


def t_error(t):
    """Carácter ilegal en modo HTML (INITIAL). Mismo tratamiento."""
    _caracter_ilegal(t)


def _caracter_ilegal(t):
    c = t.value[0]
    registrar_error(
        t.lexer, CARACTER_ILEGAL,
        f"carácter ilegal {c!r} (U+{ord(c):04X}): no pertenece al alfabeto de PHP",
        t.lexpos, c
    )
    t.lexer.skip(1)
