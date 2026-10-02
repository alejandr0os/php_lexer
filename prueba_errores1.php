<?php
// Errores lexicos: numeros, variables, caracteres y heredoc
$ok = 10;
$a = 123abc;
$b = 0x;
$c = 0b102;
$d = 1.2.3;
$e = 089;
$f = 1__000;
$g = $ok € 5;
$1abc = 3;
$h = <<<
$z = 9;
echo $ok;
