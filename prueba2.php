<!DOCTYPE html>
<html>
<head><title>Prueba 2</title></head>
<body>
<h1><?= $titulo ?></h1>
<?php
/**
 * Clase de ejemplo (doc comment)
 */
namespace App\Modelos;

#[Attribute]
class Persona
{
    private string $nombre;
    public const MAX = 100;

    public function __construct(string $nombre)
    {
        $this->nombre = $nombre;
    }

    public function getNombre(): ?string
    {
        return $this->nombre ?? 'sin nombre';
    }
}

$p = new Persona('Maria');
echo $p?->getNombre();
echo Persona::MAX;

// Numeros en distintos formatos
$dec = 42;
$flo = 3.14159;
$cie = 6.02e-23;
$hex = 0x1AF;
$bin = 0b1010;
$oct = 0o755;
$sep = 1_000_000;

// Operadores variados
$x = 5 <=> 3;
$y = $x << 2;
$z = $y & 1 | 2 ^ 3;
$w ??= 10;
$cmp = ($x <> $y) and ($z !== $w);

// Cadenas
$a = 'comillas simples con \' escapada';
$b = "comillas dobles con \"escape\" y $x";

// Heredoc y nowdoc
$h = <<<EOT
Hola $a, esto es heredoc
EOT;

$n = <<<'EOT'
Esto es nowdoc con $variable sin interpolar
EOT;

try {
    throw new Exception("error");
} catch (Exception $e) {
    echo $e->getMessage();
} finally {
    echo "fin";
}
?>
<p>Texto HTML final</p>
</body>
</html>
