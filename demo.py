"""
Código de demostración para el Analizador Léxico de PHP
========================================================

Autores:
    Alejandro Osorio Osorio
    Maria Paula Ruiz

Ejemplo de PHP que ejercita la mayoría de características del lexer:
- Declaraciones y namespaces
- Definiciones de clases y métodos
- Números en diversos formatos
- Cadenas y heredoc/nowdoc
- Comentarios
- Operadores y expresiones
- Atributos de PHP 8
- Funciones flecha
"""

DEMO_PHP = r'''<?php
// demotración.php - Ejercita la mayoría de tipos de token

declare(strict_types=1);

namespace App;

use App\Contracts\UserInterface;

/** Comentario de documentación - se emite como T_DOC_COMMENT */
#[Attribute]
final class User implements UserInterface
{
    public const MAX_AGE = 100;

    public function __construct(
        private string $name,
        protected ?int $age = null
    ) {}

    public function greet(string $greeting = "Hola"): string
    {
        return $greeting . ', ' . $this->name . '!';
    }
}

$usuario = new User('Ada', 36);

// Números en diferentes formatos
$hexadecimal = 0x1AF;              // Hexadecimal
$binario     = 0b1010;             // Binario
$octal       = 0755;               // Octal
$grande      = 1_000_000;          // Con separadores
$pi          = 3.14159;            // Punto flotante
$cientifico  = 6.02e-23;           // Notación científica

// Cadenas de caracteres
$comillas_simples = 'literal \'entrecomillado\' $sin interpolación';
$comillas_dobles = "Hola, $usuario->name!";

// Heredoc y nowdoc
$mensaje = <<<TXT
    Estimado $name, bienvenido!
    TXT;

$raw = <<<'TXT'
    Sin interpolación de $variables aquí.
    TXT;

// Control de flujo
if ($pi > 3 && $hexadecimal !== 0) {
    echo "Número grande\n";
} elseif ($pi == 3) {
    # Comentario con hash
} else {
    print 'Número pequeño';
}

$total = $hexadecimal + $binario - $octal * $grande / $pi % 2 ** 3;

// Iteración con foreach
foreach (['a' => 1, 'b' => 2] as $clave => $valor) {
    $lista[] = [$clave, $valor];
}

// Bucles while y do-while
while ($total < 10) {
    $total++;
}
do {
    $total--;
} while ($total > 0);

// Switch case
switch ($total) {
    case 0:
        break;
    default:
        continue;
}

// Manejo de excepciones
try {
    throw new \RuntimeException("¡Error!");
} catch (\Exception | \Error $e) {
    error_log($e->getMessage());
} finally {
    unset($e);
}

$etiqueta = match ($total) {
    0 => 'cero',
    default => 'muchos'
};

// Operadores especiales
$coalesce = $a ?? $b ?? 'predeterminado';    // Coalescencia nula
$comparacion = $total <=> 42;                 // Nave espacial
$bits = ~$x | ($y ^ $z) << 2 >> 1;           // Operaciones bitwise
$mascara &= 0xFF;
$referencia = $usuario;                      // Referencia
$silencioso = @filemtime('x') or die();      // Supresión, o
$nulable = $usuario?->name ?? 'anónimo';     // Nullsafe + coalesce
$expansion = [...$lista, ...$resto];         // Expansión de array

User::MAX_AGE;                                // Constante de clase

$funcion_flecha = fn($x) => $x * 2;          // Función flecha
$esUsuario = $usuario instanceof UserInterface;

exit(0);
?>
<b>Fuera de PHP:</b> HTML plano aquí - se emite como T_INLINE_HTML
<?= $usuario->greet() ?>
'''
