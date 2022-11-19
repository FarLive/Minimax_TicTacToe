import sys
import pygame
import numpy as np

from constants import *
from ai import *

# Inicializacion de la interfaz
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # Definicion del ancho y alto
pygame.display.set_caption('TIC TAC TOE AI')        # Titulo de la ventana
screen.fill(BG_COLOR)                               # Color de fondo

# Tablero logico
class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS)) # Tupla de 3x3
        print(self.squares)
        self.empty_squares = self.squares     # Lista de casillas
        self.marked_squares = 0

    def final_state(self, show = False):
        '''
            @return 0 si no hay un ganador todavia
            @return 1 si el jugador 1 gana
            @return 2 si el jugador 2 gana
        '''
        # Jugadas ganadoras verticales
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]         # Regresara 1 porque ganara el jugador 1

        # Jugadoras ganadoras horizontales
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # Jugadores ganadoras diagonales
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        # Jugadores ganadoras diagonales inversas
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        # Sin ganadores aun
        return 0
        
    # Marcar posicion del jugador
    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1                   # Incremento cada vez marca una casilla

    # Verificar si la posicion esta vacia
    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    # Obtener casillas vacias y devuelve en forma de lista
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))

        return empty_squares
    
    # Si el tablero esta lleno
    def isfull(self):
        return self.marked_squares == 9

    # Si el tablero esta vacio
    def isempty(self):
        return self.marked_squares == 0
        

class Game:    
    # Metodo Init
    def __init__(self):         # Se ejecutara cada vez llamemos un objeto game
        self.board = Board()
        self.ai = AI()
        self.player = 1         # Jugador que jagara con:       1 --> Cruz      2 --> Circulo
        self.gamemode = 'ai' 
        self.running = True     # Si el juego aun no termina
        self.show_lines()

    # Marcar casillas
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        print(self.board.squares)
        self.next_turn()

    # Division de tablero
    def show_lines(self):
        screen.fill(BG_COLOR)
        
        # Lineas verticales
        # ventana(tablero), color de fondo, (punto inicial de la linea), (punto final), tamaño de la linea
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        
        # Lineas horizontales 
        # ventana(tablero), color de fondo, (punto inicial de la linea), (punto final), tamaño de la linea
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # Dibujar cruz
            # Diagonal inversa
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            # Diagonal
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player ==	2:
            # Dibujar circulo
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
        
    def next_turn(self):
        self.player = self.player % 2 + 1           # 1 % 2 = 1 + 1 = 2    ---->    jugador 2
                                                    # 2 % 2 = 0 + 1 = 1    ---->    jugador 1

    # Fin del juego
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    # Reiniciar tablero
    def reset(self):
        self.__init__()             # Reestablece todos los valores por defecto (como si iniciara un nuevo juego)

def main():

    # Objeto game
    game = Game()   # objeto / clase
    board = game.board
    ai = game.ai

    while True:   # Loop infinito que evita que se cierre la ventana a no ser que se le indique otra cosa

        for event in pygame.event.get():

            if event.type == pygame.QUIT:   # Cerrara el juego
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # r-Reiniciar
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                
                # 0-Random IA
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1-Minimax IA
                if event.key == pygame.K_1:
                    ai.level = 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:    # Al hacer click en el tablero
                # Conversion de coordenadas(pixeles) a posiciones(filas y columnas)    
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                print(row,col)

                # Marcar posicion en tablero del jugador
                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False
            
        # Marcar posicion en tablero de la IA
        if game.player == ai.player and game.running:
            pygame.display.update()

            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
        
        pygame.display.update()
        
main()