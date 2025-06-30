
# 🧀🐱🐭 Laberinto del Gato y el Ratón

Este proyecto es un **juego de consola en Python** donde un gato y un ratón compiten en un tablero de ajedrez de 8x8.  
El ratón intenta llegar al queso mientras el gato trata de atraparlo.  
El juego combina **POO (Programación Orientada a Objetos)** y **algoritmo Minimax** para simular la inteligencia del ratón.

---

## 🎮 ¿Cómo funciona?

- **Turnos alternos**:
  - El ratón mueve primero.
  - Los primeros 4 turnos del ratón son **movimientos aleatorios**.
  - A partir del turno 5, el ratón usa **Minimax** para elegir el movimiento más inteligente.
  - El gato se mueve de forma manual según tu elección (movimientos en diagonal como un alfil).

- **Final del juego**:
  - El ratón gana si llega al queso.
  - El gato gana si atrapa al ratón.
  - Si se cumplen 10 turnos sin atraparlo, el ratón escapa.

---

## ⚙️ Tecnologías y conceptos aplicados

✅ **Python**  
✅ **Programación Orientada a Objetos**:
  - Clases `Pieza`, `Gato`, `Raton`  
✅ **Herencia de clases**  
✅ **Minimax recursivo** (sin poda alfa-beta)  
✅ **Interacción por consola**  
✅ **Tablero representado con emojis**  

---

## 🐍 Ejecución

1️⃣ Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
