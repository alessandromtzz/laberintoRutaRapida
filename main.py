import pygame
import sys
from collections import deque

# Configuración de la ventana
WIDTH, HEIGHT = 600, 600
ROWS = 25  # Número de filas y columnas de la cuadrícula
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Algoritmos de Laberinto - Diseño de Algoritmos")

# Paleta de Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)      # Paredes (Obstáculos)
RED = (231, 76, 60)       # Nodo Destino (Fin)
GREEN = (46, 204, 113)    # Nodo Inicio
BLUE = (52, 152, 219)     # Camino óptimo encontrado
GREY = (189, 195, 199)    # Celdas visitadas durante la exploración
LINE_COLOR = (220, 225, 230)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_path(self):
        self.color = BLUE

    def make_visited(self):
        if self.color != GREEN and self.color != RED:
            self.color = GREY

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, LINE_COLOR, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, LINE_COLOR, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# Algoritmo BFS (Búsqueda en Anchura) - Complejidad O(V + E)
def bfs(grid, start, end):
    queue = deque([start])
    came_from = {start: None}
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == end:
            # Reconstruir el camino óptimo hacia atrás
            while current in came_from and came_from[current]:
                current = came_from[current]
                if current != start:
                    current.make_path()
            return True

        # Explorar vecinos (Arriba, Abajo, Izquierda, Derecha)
        r, c = current.row, current.col
        neighbors_pos = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        
        for nr, nc in neighbors_pos:
            if 0 <= nr < ROWS and 0 <= nc < ROWS:
                neighbor = grid[nr][nc]
                if not neighbor.is_barrier() and neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
                    neighbor.make_visited()
                    
        pygame.time.delay(5) # Pequeño retraso para ver la animación paso a paso
        draw(WIN, grid, ROWS, WIDTH)

    return False

def main():
    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None
    run = True

    print("INSTRUCCIONES:")
    print("1. Click izquierdo 1 vez: Colocar PUNTO DE INICIO (Verde)")
    print("2. Click izquierdo 2 vez: Colocar PUNTO DE DESTINO (Rojo)")
    print("3. Click izquierdo arrastrando: Dibujar PAREDES (Negro)")
    print("4. Presiona ESPACIO: Ejecutar el algoritmo BFS")
    print("5. Presiona 'C': Limpiar tablero\n")

    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Controles del Mouse
            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho (borrar celda)
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # Controles del Teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    bfs(grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)

    pygame.quit()

if __name__ == "__main__":
    main()