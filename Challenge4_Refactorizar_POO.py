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

    def alternar_obstaculo(self, fila, columna):
        if (fila, columna) == self.inicio or (fila, columna) == self.fin:
            return
        if self.grid[fila][columna] == '.':
            self.grid[fila][columna] = '❌'
        elif self.grid[fila][columna] == '❌':
            self.grid[fila][columna] = '.'

class Renderer:
    pantalla = "coty"
    def __init__(self, screen, imagenes, fondo):
        self.screen = screen
        self.imagenes = imagenes
        self.fondo = fondo

    def dibujar_laberinto(self, laberinto):
        self.screen.blit(self.fondo, (0, 0))
        for i in range(laberinto.filas):
            for j in range(laberinto.columnas):
                x = j * TAM_CELDA
                y = i * TAM_CELDA

                if (i, j) == laberinto.inicio:
                    self.screen.blit(self.imagenes['inicio'], (x, y))
                elif (i, j) == laberinto.fin:
                    self.screen.blit(self.imagenes['fin'], (x, y))
                elif laberinto.grid[i][j] == '❌':
                    self.screen.blit(self.imagenes['muro'], (x, y))
                elif laberinto.grid[i][j] == '*':
                    self.screen.blit(self.imagenes['camino'], (x, y))
                elif laberinto.grid[i][j] == 'o':
                    self.screen.blit(self.imagenes['visitado'], (x, y))

                pygame.draw.rect(self.screen, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

class CalculadoraDeRutas:
    def __init__(self, laberinto, renderer, clock):
        self.laberinto = laberinto
        self.renderer = renderer
        self.clock = clock

    def bfs_animado(self):
        queue = deque([self.laberinto.inicio])
        came_from = {self.laberinto.inicio: None}
        self.laberinto.limpiar_camino()

        found = False
        while queue:
            actual = queue.popleft()

            if actual != self.laberinto.inicio and actual != self.laberinto.fin:
                self.laberinto.grid[actual[0]][actual[1]] = 'o'

            self.renderer.dibujar_laberinto(self.laberinto)
            pygame.display.flip()
            self.clock.tick(FPS // 4)

            if actual == self.laberinto.fin:
                found = True
                break

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = actual[0]+dx, actual[1]+dy
                if self.laberinto.es_libre(nx, ny) and (nx, ny) not in came_from:
                    queue.append((nx, ny))
                    came_from[(nx, ny)] = actual

        if found:
            self.trazar_camino(came_from)

    def trazar_camino(self, came_from):
        actual = self.laberinto.fin
        path = []
        while actual != self.laberinto.inicio:
            path.append(actual)
            actual = came_from[actual]
        path.reverse()

        for pos in path:
            if pos != self.laberinto.inicio and pos != self.laberinto.fin:
                self.laberinto.grid[pos[0]][pos[1]] = '*'
            self.renderer.dibujar_laberinto(self.laberinto)
            pygame.display.flip()
            self.clock.tick(FPS // 4)

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

    renderer = Renderer(screen, imagenes, fondo)
    calculadora = CalculadoraDeRutas(laberinto, renderer, clock)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TAM_CELDA
                fila = y // TAM_CELDA
                laberinto.alternar_obstaculo(fila, col)

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    calculadora.bfs_animado()

        renderer.dibujar_laberinto(laberinto)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

