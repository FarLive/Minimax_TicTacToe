import copy
import random

class AI:
    # Iniciacion de la IA
    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player

    # Forma de actuar de la IA calculando las casillas vacias hasta llenar todas al azar
    def rnd(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]

    # Algoritmo MiniMax
    def minimax(self, board, maximizing):
        
        # Caso final
        case = board.final_state()

        # Jugandor 1 gana
        if case == 1:
            return 1, None # eval, move

        # Jugador 2 gana
        if case == 2:
            return -1, None

        # Empate
        elif board.isfull():
            return 0, None

        # Si la IA juega MAX
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        # Si la IA juega MIN
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    
    # Funcion de evaluacion
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # fila, columna