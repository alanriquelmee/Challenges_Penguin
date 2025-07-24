import copy
import random

Board_size = 8
#Inicia POO clase principal, luego las herencias
class Pieza:
    def __init__(self, x, y, simbolo):  # constructor por eso usa init
        self.x = x
        self.y = y
        self.simbolo = simbolo 
    def mover(self, x, y): #funciones de la clase
        self.x = x 
        self.y = y
    def posicion(self): # que te retorna la posicion actual
        return self.x, self.y
    
class Gato(Pieza): # hereda de pieza
    def movimientos_permitidos(self, tablero):
        movimientos = []
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = self.x, self.y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < Board_size and 0 <= ny < Board_size:
                    movimientos.append((nx, ny))
                else:
                    break
        return movimientos
    
class Raton(Pieza):
    def movimientos_permitidos(self, tablero):
        movimientos = []
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                       (0, 1), (0, -1), (1, 0), (-1, 0)] # se mueve ortogonal + diagonal como reina en ajedrez
        for dx, dy in direcciones:
            nx, ny = self.x, self.y
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < Board_size and 0 <= ny < Board_size:
                    movimientos.append((nx, ny))
                else:
                    break
        return movimientos

def evaluar_estado(gato, raton, queso):
    if gato.posicion() == raton.posicion():
        return -10 #gato come raton, malo para el raton
    elif raton.posicion() == queso: # raton come queso y gana
        return 10
    return 1 #sigue el juego
    
def minimax(gato, raton, queso, profundidad, maximizando):
    if profundidad == 0 or gato.posicion() == raton.posicion() or raton.posicion() == queso:
        return evaluar_estado(gato, raton, queso), raton.posicion()
    
    if maximizando:
        mejor_valor = float("-inf") # cualquier valor sera mejor que menos infinito
        mejor_mov = raton.posicion()
        for mov in raton.movimientos_permitidos(None):
            raton_copia = copy.deepcopy(raton)
            raton_copia.mover(*mov)
            valor, _ = minimax(gato, raton_copia, queso, profundidad -1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = mov
        return mejor_valor, mejor_mov
    else:
        peor_valor = float('inf')
        peor_mov = raton.posicion()
        for mov in raton.movimientos_permitidos(None):
            raton_copia = copy.deepcopy(raton)
            raton_copia.mover(*mov) # investigar * asterisco
            valor, _ = minimax(gato, raton_copia, queso, profundidad - 1, True)
            if valor < peor_valor:  # poda alfa beta 
                peor_valor = valor
                peor_mov = mov
        return peor_valor, peor_mov
        
def imprimir_tablero(gato, raton, queso, movimientos_resaltados=None):
    for y in range(Board_size):
        fila = ""
        for x in range(Board_size):
            pos = (x, y)
            if pos == gato.posicion():
                fila += "🐱 "
            elif pos == raton.posicion():
                fila += "🐭 "
            elif pos == queso:
                fila += "🧀 "
            elif movimientos_resaltados and pos in movimientos_resaltados:
                fila += "🟩 "
            else:
                fila += "⬜ "
        print(fila)
    print("\n")
    
def jugar():
    gato = Gato(0, 0, '🐱') # usuario input 
    raton = Raton(7, 7, '🐭') # computadora primero random y despues minimax
    queso = (3, 3) # estatico 

    turno = 0
    MAX_TURNOS = 10
    turnos_rat = 0

    while (
        gato.posicion() != raton.posicion() and
        raton.posicion() != queso and
        turno < MAX_TURNOS
    ):
        print(f"\n🎵 Turno {turno + 1}")
        imprimir_tablero(gato, raton, queso)

        if turno % 2 == 0:
            turnos_rat += 1
            print(f"🐭 Turno del ratón #{turnos_rat}")
            if turnos_rat <= 4:
                print(" Movimiento aleatorio (aún no piensa)")
                movs = raton.movimientos_permitidos(None)
                if movs:
                    raton.mover(*random.choice(movs))
            else:
                print("Movimiento inteligente (Minimax)")
                _, mov = minimax(gato, raton, queso, 2, True)
                raton.mover(*mov)
        else:
            print("Tu turno (Gato). Movimiento válido como alfil (diagonal).")
            movimientos = gato.movimientos_permitidos(None)
            imprimir_tablero(gato, raton, queso, movimientos_resaltados=movimientos)
            print("Movimientos posibles:", movimientos)
            while True:
                try:
                    x = int(input("Ingresa coordenada X destino (0-7): "))
                    y = int(input("Ingresa coordenada Y destino (0-7): "))
                    if (x, y) in movimientos:
                        gato.mover(x, y)
                        break
                    else:
                        print(" Movimiento inválido. Intenta de nuevo.")
                except ValueError:
                    print("Entrada no válida. Usa números enteros.")

        turno += 1

    print("\n🎬 Resultado final:")
    imprimir_tablero(gato, raton, queso)

    if gato.posicion() == raton.posicion():
        print("Atrapado!!. El gato atrapó al ratón, y ganó.")
    elif raton.posicion() == queso:
        print("El ratón llegó al queso, comió y ganó.")
    else:
        print("El ratón escapó después de todos los turnos")

if __name__ == "__main__":
    jugar()
