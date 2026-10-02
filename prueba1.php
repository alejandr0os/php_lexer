<?php
// Función sin parámetros ni retorno
function mostrarSaludo() {
    echo "¡Hola, bienvenido a PHP!<br>";
}

// Función con parámetros y valor de retorno (return)
function sumarNumeros($num1, $num2) {
    $ resultado = $num1 + $num2;
    return $resultado;
}

// Invocación de las funciones
mostrarSaludo(); // Muestra el saludo

$total = sumarNumeros(5, 10); // Guarda el valor retornado
echo "La suma es: " . $total;
?>