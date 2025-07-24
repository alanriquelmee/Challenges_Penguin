#include <iostream>
#include <vector> // vector dx[]
#include <cstdlib> // rand srand
#include <ctime> //metronomo time
#include <queue> // cola
#include <utility> // pair
#include <windows.h> // Para Sleep en Windows
using namespace std;

const int FILAS = 10;
const int COLUMNAS = 10;
char laberinto[FILAS][COLUMNAS];
bool visitado[FILAS][COLUMNAS];
pair<int, int> anterior[FILAS][COLUMNAS];

string versos[] = {
    "\"Paraguayos, República o muerte!\"",
    "\"Nuestros brios nos dio libertad.\"",
    "\"Ni opresores, ni ciervos alientan.\"",
    "\"Donde reinan union e igualdad.\"",
    "Paraguayos, República o muerte!\nNuestros brios nos dio libertad\nNi opresores ni ciervos alientan\nDonde reina unión e igualdad\nGracias"
};

// Pausa general
void pausa(int ms = 100) {
    Sleep(ms);
}

// Pausa especial para BFS (0.70 segundos → 700 ms)
void pausaBFS() {
    Sleep(400);
}

// Mostrar laberinto animado (con limpiar pantalla) → para el BFS
void mostrarLaberintoAnimado() {
    system("cls"); // Limpia pantalla para animación
    for (int i = 0; i < FILAS; i++) {
        for (int j = 0; j < COLUMNAS; j++) {
            char c = laberinto[i][j];

            if (c == 'S') cout << "🚪 ";
            else if (c == 'E') cout << "🏁 ";
            else if (c == 'g') cout << "🟢 ";
            else if (c == 'r') cout << "🔴 ";
            else if (c == '#') cout << "⬛ ";
            else cout << "⬜ ";
        }
        cout << endl;
    }
    pausaBFS(); // Pausa de 0.70 s en cada paso
}

// Mostrar laberinto final (sin limpiar pantalla)
void mostrarLaberintoFinal() {
    for (int i = 0; i < FILAS; i++) {
        for (int j = 0; j < COLUMNAS; j++) {
            char c = laberinto[i][j];

            if (c == 'S') cout << "🚪 ";
            else if (c == 'E') cout << "🏁 ";
            else if (c == 'g') cout << "🟢 ";
            else if (c == 'r') cout << "🔴 ";
            else if (c == '#') cout << "⬛ ";
            else cout << "⬜ ";
        }
        cout << endl;
    }
}

// Marcar caminos con backtracking (silencioso)
void explorarBacktracking(int x, int y) {
    if (x < 0 || y < 0 || x >= FILAS || y >= COLUMNAS) return;
    if (laberinto[x][y] == '#' || visitado[x][y]) return;

    visitado[x][y] = true;

    if (laberinto[x][y] != 'S' && laberinto[x][y] != 'E') {
        laberinto[x][y] = 'r'; // Camino explorado (silencioso)
    }

    explorarBacktracking(x + 1, y);
    explorarBacktracking(x - 1, y);
    explorarBacktracking(x, y + 1);
    explorarBacktracking(x, y - 1);
}

// Generar laberinto aleatorio
void generarLaberinto() {
    for (int i = 0; i < FILAS; i++)
        for (int j = 0; j < COLUMNAS; j++)
            laberinto[i][j] = '#';

    for (int i = 0; i < FILAS; i++) {
        for (int j = 0; j < COLUMNAS; j++) {
            if (rand() % 100 < 50) {
                laberinto[i][j] = ' ';
            }
        }
    }

    laberinto[0][0] = 'S';
    laberinto[FILAS - 1][COLUMNAS - 1] = 'E';
}

// Reiniciar matriz de visitados
void reiniciarVisitados() {
    for (int i = 0; i < FILAS; i++)
        for (int j = 0; j < COLUMNAS; j++)
            visitado[i][j] = false;
}

// BFS para encontrar camino más corto (animado)
bool resolverBFS(int sx, int sy) {
    queue<pair<int, int>> cola;
    cola.push({sx, sy});
    visitado[sx][sy] = true;

    int dx[] = {1, -1, 0, 0};
    int dy[] = {0, 0, 1, -1};

    while (!cola.empty()) {
        int x = cola.front().first;
        int y = cola.front().second;
        cola.pop();

        if (laberinto[x][y] == 'E') {
            pair<int, int> p = anterior[x][y];
            while (laberinto[p.first][p.second] != 'S') {
                laberinto[p.first][p.second] = 'g'; // Camino correcto
                mostrarLaberintoAnimado(); // Animación en tiempo real del camino verde
                p = anterior[p.first][p.second];
            }
            return true;
        }

        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i];
            int ny = y + dy[i];

            if (nx >= 0 && nx < FILAS && ny >= 0 && ny < COLUMNAS &&
                !visitado[nx][ny] &&
                (laberinto[nx][ny] == ' ' || laberinto[nx][ny] == 'E' || laberinto[nx][ny] == 'r')) {
                cola.push({nx, ny});
                visitado[nx][ny] = true;
                anterior[nx][ny] = {x, y};
            }
        }
    }
    return false;
}

// Función principal
int main() {
    srand(time(0));

    for (int k = 0; k < 5; k++) {
        bool resuelto = false;

        while (!resuelto) {
            generarLaberinto();
            reiniciarVisitados();
            explorarBacktracking(0, 0);
            reiniciarVisitados();
            resuelto = resolverBFS(0, 0);
        }

        cout << "\n🎼 Laberinto #" << (k + 1) << ":\n";
        mostrarLaberintoFinal(); // Imprimir laberinto completo

        // Contar pasos del camino correcto
        int pasos = 0;
        for (int i = 0; i < FILAS; i++)
            for (int j = 0; j < COLUMNAS; j++)
                if (laberinto[i][j] == 'g')
                    pasos++;

        cout << "\n🧮 Pasos del camino correcto: " << pasos << "\n";

        // Mostrar verso correspondiente
        cout << "\n🎵 Himno Paraguayo (fragmento #" << (k + 1) << "):\n";

        if (k == 4) {
            cout << "━━━━━━━━━━━━━━━━━━━━━━━\n";
            cout << "🎉 ¡Verso completo del himno! 🎉\n";
            cout << "━━━━━━━━━━━━━━━━━━━━━━━\n";
            cout << versos[k] << "\n";
            cout << "━━━━━━━━━━━━━━━━━━━━━━━\n";
        } else {
            cout << versos[k] << "\n";
        }

        // Mantener laberinto visible durante 5 segundos
        cout << "\n⏳ Mostrando el laberinto durante 5 segundos...\n";
        Sleep(5000);

        cout << "\n============================================\n\n";
    }

    return 0;
}
