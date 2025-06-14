# 🇵🇾 Laberinto del Himno Paraguayo 🎶🧠

Este es un juego de consola en C++ donde cada nivel es un laberinto **resoluble automáticamente** mediante algoritmos de **Backtracking** y **BFS** (Breadth-First Search). Cada laberinto representa un verso del **Himno Nacional de Paraguay**. ¡Tu objetivo es visualizar cómo la inteligencia encuentra el camino correcto mientras se revela el himno línea por línea! 🇵🇾

---

## 🎯 Objetivo del juego

- Generar automáticamente 5 laberintos distintos.
- Cada laberinto tiene un único camino correcto desde `🚪 Inicio` hasta `🏁 Final`.
- El camino se revela visualmente con colores en consola:
  - 🔴 Backtracking (exploración fallida)
  - 🟢 BFS (camino correcto)
- Al completar cada laberinto, se muestra un verso del himno nacional.

---

## ⚙️ Tecnologías y algoritmos

- Lenguaje: **C++**
- Librerías:
  - `<iostream>`: Entrada/Salida
  - `<vector>` y `<queue>`: Estructuras de datos
  - `<cstdlib>`, `<ctime>`: Aleatoriedad
  - `<windows.h>`: Animaciones y `Sleep()`
- Algoritmos:
  - `Backtracking`: para marcar caminos explorados
  - `BFS (Breadth-First Search)`: para encontrar el **camino más corto**

---

## 🎮 Controles y experiencia

- Se ejecuta desde consola (Windows)
- Cada paso del algoritmo BFS es **animado**
- Se muestran los pasos exactos que conforman la solución
- Verso del himno revelado tras resolver cada nivel

---

## 📸 Ejemplo de salida (simplificada)

