Laberinto del Gato y del Raton
Es un juego por turnos en un tablero de 8x8 ( inicialmente) que se puede modificar, donde un gato (jugador mediante input) intenta atrapar a un ratón (IA), mientras el ratón intenta llegar al queso 🧀, o en su defecto lograr escapar.
El ratón comienza moviéndose aleatoriamente, pero después de unos turnos, ¡empieza a usar inteligencia artificial con el algoritmo Minimax para escapar!

Ganas si:

Eres el gato y atrapas al ratón 🐱🐭
Eres el raton y comes el queso
Eres el raton y logras escapar despues de todos los turnos, incluso si no comes el queso
Pierdes si:
El ratón llega al queso antes que tú lo atrapes 🧀
El ratón escapa de ti, incluso si no ha comido el queso
Que funciono
El minimax, funcionaba como queria que funcione y poder elegir yo como usuario manejarle al gato

MEJOR ajá
Lograr que el raton se mueva de forma aleatoria para poder tener una oportunidad contra el mismo y luego que utilice el algoritmo de minimax.

Cómo ejecutar el juego
Asegúrate de tener Python 3 instalado. Puedes verificarlo con:

python --version

Descarga o clona este repositorio

Ejecuta el archivo principal

Reglas del Juego
El tablero inicial es de 8x8 celdas.
Hay tres personajes:
Gato (Jugador humano): se mueve en diagonales como un alfil de ajedrez.
Ratón (IA): se mueve en todas las direcciones, como una reina de ajedrez.
Queso: está fijo en una posición del tablero.
Objetivo
El ratón gana si llega al queso 🧀.
El gato gana si atrapa al ratón (ocupando la misma casilla).
Si pasan 10 turnos sin que nadie gane, el ratón escapa, tambien gana y el juego termina.
Turnos
El juego alterna turnos:

Primero juega el ratón (IA).
Luego juega el gato (usuario).
Durante los primeros 4 turnos, el ratón se mueve aleatoriamente.

Tecnologías utilizadas
Python 3
Programación orientada a objetos (POO)
Algoritmo Minimax con copias profundas (copy.deepcopy)
Uso básico de entrada por consola (input)
Cómo ejecutar el juego
Asegúrate de tener Python 3 instalado.
Guarda el archivo como  minimax_lab.py.
Abre una terminal y ejecuta:
python --- nombre del archivo

Posibles mejoras
Agregar interfaz gráfica.
Mejorar la IA con mayor profundidad en Minimax.
Soporte multijugador.
Añadir niveles de dificultad.
