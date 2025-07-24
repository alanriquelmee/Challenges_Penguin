import pygame
import sys
from collections import deque

# Configuración
TAM_CELDA = 40
FPS = 60

class Laberinto:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.grid = [['.' for _ in range(columnas)] for _ in range(filas)]
        self.inicio = None
        self.fin = None

    def colocar_inicio_fin(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin

    def limpiar_camino(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.grid[i][j] in ('*', 'o'):
                    self.grid[i][j] = '.'

    def es_libre(self, x, y):
        return 0 <= x < self.filas and 0 <= y < self.columnas and self.grid[x][y] == '.'

def dibujar_laberinto(screen, laberinto, imagenes, fondo):
    screen.blit(fondo, (0, 0))
    for i in range(laberinto.filas):
        for j in range(laberinto.columnas):
            x = j * TAM_CELDA
            y = i * TAM_CELDA

            if (i, j) == laberinto.inicio:
                screen.blit(imagenes['inicio'], (x, y))
            elif (i, j) == laberinto.fin:
                screen.blit(imagenes['fin'], (x, y))
            elif laberinto.grid[i][j] == '❌':
                screen.blit(imagenes['muro'], (x, y))
            elif laberinto.grid[i][j] == '*':
                screen.blit(imagenes['camino'], (x, y))
            elif laberinto.grid[i][j] == 'o':
                screen.blit(imagenes['visitado'], (x, y))

            # Rejilla opcional
            pygame.draw.rect(screen, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

def bfs_animado(screen, laberinto, clock, imagenes, fondo):
    queue = deque([laberinto.inicio])
    came_from = {laberinto.inicio: None}
    laberinto.limpiar_camino()

    found = False
    while queue:
        actual = queue.popleft()

        if actual != laberinto.inicio and actual != laberinto.fin:
            laberinto.grid[actual[0]][actual[1]] = 'o'

        dibujar_laberinto(screen, laberinto, imagenes, fondo)
        pygame.display.flip()
        clock.tick(FPS // 4)

        if actual == laberinto.fin:
            found = True
            break

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = actual[0]+dx, actual[1]+dy
            if laberinto.es_libre(nx, ny) and (nx, ny) not in came_from:
                queue.append((nx, ny))
                came_from[(nx, ny)] = actual

    if found:
        trazar_camino(screen, laberinto, came_from, clock, imagenes, fondo)

def trazar_camino(screen, laberinto, came_from, clock, imagenes, fondo):
    actual = laberinto.fin
    path = []
    while actual != laberinto.inicio:
        path.append(actual)
        actual = came_from[actual]
    path.reverse()

    for pos in path:
        if pos != laberinto.inicio and pos != laberinto.fin:
            laberinto.grid[pos[0]][pos[1]] = '*'
        dibujar_laberinto(screen, laberinto, imagenes, fondo)
        pygame.display.flip()
        clock.tick(FPS // 4)

def main():
    filas = int(input("Número de filas: "))
    columnas = int(input("Número de columnas: "))

    ancho = columnas * TAM_CELDA
    alto = filas * TAM_CELDA

    pygame.init()
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Mapa del Merodeador: Camino BFS")
    clock = pygame.time.Clock()

    # Cargar imágenes
    imagenes = {
        'muro': pygame.transform.scale(pygame.image.load("assets/muro.png"), (TAM_CELDA, TAM_CELDA)),
        'inicio': pygame.transform.scale(pygame.image.load("assets/inicio.png"), (TAM_CELDA, TAM_CELDA)),
        'fin': pygame.transform.scale(pygame.image.load("assets/fin.png"), (TAM_CELDA, TAM_CELDA)),
        'camino': pygame.transform.scale(pygame.image.load("assets/camino.png"), (TAM_CELDA, TAM_CELDA)),
        'visitado': pygame.transform.scale(pygame.image.load("assets/visitado.png"), (TAM_CELDA, TAM_CELDA))
    }
    fondo = pygame.transform.scale(pygame.image.load("assets/fondo.jpg"), (ancho, alto))

    laberinto = Laberinto(filas, columnas)

    print("Selecciona el inicio (fila,columna): ")
    laberinto.inicio = tuple(map(int, input().split(',')))
    print("Selecciona el fin (fila,columna): ")
    laberinto.fin = tuple(map(int, input().split(',')))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TAM_CELDA
                fila = y // TAM_CELDA
                if (fila, col) != laberinto.inicio and (fila, col) != laberinto.fin:
                    if laberinto.grid[fila][col] == '.':
                        laberinto.grid[fila][col] = '❌'
                    elif laberinto.grid[fila][col] == '❌':
                        laberinto.grid[fila][col] = '.'

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bfs_animado(screen, laberinto, clock, imagenes, fondo)

        dibujar_laberinto(screen, laberinto, imagenes, fondo)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
