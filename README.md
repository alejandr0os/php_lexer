# Analizador Léxico para PHP

**Autores:** Alejandro Osorio Osorio, Maria Paula Ruiz

## Descripción

Este proyecto implementa un **analizador léxico** (lexer) completo para PHP utilizando **PLY** (Python Lex-Yacc). El lexer analiza código PHP y lo divide en tokens, identificando palabras clave, operadores, literales, identificadores y comentarios.

## Características

Soporta todas las características principales de PHP:
- Etiquetas PHP estándar (`<?php`, `<?=`, `?>`)
- Palabras clave del lenguaje (control de flujo, OOP, excepciones)
- Operadores (aritméticos, lógicos, de comparación, bitwise)
- Literales (cadenas, números en múltiples formatos, heredoc/nowdoc)
- Variables y identificadores
- Comentarios (de una línea y de bloque)
- Atributos de PHP 8 (`#[Attribute]`)
- HTML mixto con bloques PHP

Estructura modular y bien organizada:
- Separación clara entre configuración, reglas y análisis
- Código comentado en español
- Fácil de mantener y extender

Uso flexible:
- Como programa de línea de comandos
- Como biblioteca Python importable

## Estructura del Proyecto

```
php_lexer/
├── php_lexer.py           # Punto de entrada principal
├── lexer_config.py        # Configuración y palabras reservadas
├── lexer_excepciones.py   # Excepciones personalizadas
├── lexer_reglas.py        # Reglas de tokenización
├── lexer_builder.py       # Constructor del lexer
├── lexer_analizador.py    # Funciones de análisis
├── demo.py                # Código PHP de demostración
└── README.md              # Este archivo
```

### Descripción de módulos

#### `lexer_config.py`
Contiene todas las configuraciones estáticas:
- Estados del lexer (INITIAL para HTML, 'php' para código PHP)
- Palabras reservadas de PHP
- Definición de tokens básicos

#### `lexer_excepciones.py`
Define excepciones personalizadas:
- `PHPLexError`: Se lanza cuando hay errores en el análisis léxico

#### `lexer_reglas.py`
Implementa todas las reglas de tokenización:
- Reglas para modo HTML
- Reglas para modo PHP
- Manejo de etiquetas, comentarios, literales
- Definición de operadores
- Manejo de errores

#### `lexer_builder.py`
Responsable de construir el lexer:
- Importa todas las reglas
- Configura PLY
- Proporciona la instancia global del lexer

#### `lexer_analizador.py`
Proporciona funciones de alto nivel:
- `analizar`: Tokeniza código PHP
- `mostrar_tokens`: Imprime tokens en formato tabular
- `resumir_tokens`: Genera estadísticas

#### `demo.py`
Código PHP de demostración que ejercita la mayoría de características del lexer

#### `php_lexer.py`
Punto de entrada principal que coordina todo el sistema

## Instalación

### Requisitos

- Python 3.6 o superior
- PLY (Python Lex-Yacc)

### Pasos de instalación

```bash
# Instalar PLY
pip install ply

```

## Uso

### Como programa de línea de comandos

```bash
# Analizar código PHP de demostración
python php_lexer.py

# Analizar un archivo PHP específico
python php_lexer.py archivo.php
python php_lexer.py /ruta/a/archivo.php

# Guardar resultados en un archivo
python php_lexer.py archivo.php > resultados.txt
```

### Como biblioteca Python

```python
from lexer_analizador import analizar, mostrar_tokens, resumir_tokens

# Analizar código PHP
codigo = """<?php
$x = 42;
echo $x;
?>"""

tokens = analizar(codigo)

# Mostrar tokens
mostrar_tokens(tokens)

# Ver estadísticas
resumir_tokens(tokens)
```

## Ejemplo de salida

```
LÍNEA    POS  TIPO                            LEXEMA
-----------------------------------------------------------------------------------
   1      0  T_OPEN_TAG                      '<?php'
   2      8  T_VARIABLE                      '$x'
   2     11  EQUALS                          '='
   2     13  T_LNUMBER                       '42'
   2     15  SEMI                            ';'
   3     17  T_ECHO                          'echo'
   3     22  T_VARIABLE                      '$x'
   3     24  SEMI                            ';'
   4     26  T_CLOSE_TAG                     '?>'
-----------------------------------------------------------------------------------
8 tokens

FRECUENCIA DE TOKENS
-----------------------------------------------------------------------------------
  EQUALS                               1
  SEMI                                 2
  T_CLOSE_TAG                          1
  T_ECHO                               1
  T_LNUMBER                            1
  T_OPEN_TAG                           1
  T_VARIABLE                           2
  TOTAL                                8
```

## Tipos de token soportados

### Etiquetas y HTML
- `T_OPEN_TAG`: `<?php`
- `T_OPEN_TAG_WITH_ECHO`: `<?=`
- `T_CLOSE_TAG`: `?>`
- `T_INLINE_HTML`: Contenido HTML

### Identificadores y literales
- `T_VARIABLE`: Variables como `$nombre`
- `T_STRING`: Identificadores
- `T_LNUMBER`: Números enteros
- `T_DNUMBER`: Números flotantes
- `T_CONSTANT_ENCAPSED_STRING`: Cadenas entrecomilladas
- `T_HEREDOC`: Heredoc con interpolación
- `T_NOWDOC`: Nowdoc sin interpolación

### Comentarios y atributos
- `T_COMMENT`: Comentarios `//`, `#`, `/* */`
- `T_DOC_COMMENT`: Comentarios de documentación `/**`
- `T_ATTRIBUTE`: Atributos de PHP 8 `#[...]`

### Operadores
- Operadores aritméticos: `+`, `-`, `*`, `/`, `%`, `**`
- Operadores de comparación: `==`, `===`, `!=`, `!==`, `<`, `>`, `<=`, `>=`, `<=>`
- Operadores lógicos: `&&`, `||`, `and`, `or`, `xor`
- Operadores de asignación: `=`, `+=`, `-=`, `*=`, `/=`, `.=`, etc.
- Operadores bitwise: `&`, `|`, `^`, `~`, `<<`, `>>`
- Otros: `->`, `=>`, `::`, `...`, `??`, `?->`, etc.

### Delimitadores
- Paréntesis: `(`, `)`
- Llaves: `{`, `}`
- Corchetes: `[`, `]`
- Punto y coma, coma, dos puntos, etc.

## Características especiales

### Heredoc y Nowdoc

El lexer reconoce correctamente la sintaxis de heredoc y nowdoc:

```php
// Heredoc (permite interpolación)
$texto = <<<EOT
Esto es $una variable
EOT;

// Nowdoc (sin interpolación)
$raw = <<<'EOT'
Esto NO es $una variable
EOT;
```

### Números en múltiples formatos

```php
$decimal = 42;
$flotante = 3.14159;
$cientifico = 6.02e-23;
$hexadecimal = 0x1AF;
$binario = 0b1010;
$octal = 0755;
$octal_nuevo = 0o755;
$separadores = 1_000_000;
```

### Atributos de PHP 8

```php
#[Attribute]
class MiAtributo {}
```

### Operador nullsafe y coalescencia nula

```php
$valor = $objeto?->propiedad ?? 'predeterminado';
```

## Limitaciones

- El lexer no valida la sintaxis completa (eso es tarea del parser)
- Los heredoc/nowdoc se analizan manualmente (limitación de expresiones regulares)
- No incluye validación de encoding de caracteres especiales de 8 bits

## Extensiones futuras

Posibles mejoras y extensiones:

1. Integrar con un parser yacc para análisis sintáctico
2. Agregar soporte para más características de PHP (templates, etc.)
3. Optimizar rendimiento para archivos muy grandes
4. Generar reportes de complejidad del código
5. Integración con herramientas de análisis estático

## Referencias

- [Sitio oficial de PLY](https://www.dabeaz.com/ply/)
- [Documentación oficial de PHP](https://www.php.net/manual/es/)
- [Manual de PHP - Tokenización](https://www.php.net/manual/es/function.token-get-all.php)

## Licencia

Este proyecto es de código abierto. Úsalo libremente en tus proyectos.

## Autores

- **Alejandro Osorio Osorio**
- **Maria Paula Ruiz**

---

Última actualización: 2026-09-24