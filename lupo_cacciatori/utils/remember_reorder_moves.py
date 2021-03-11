def type_table(board):
    giocatori = [x for x in board.find('O')]
    giocatori.sort()
    giocatori.append(board.find('X'))
    return tuple(giocatori)


class next_moves():
    def __init__(self, initial_deep):
        self.initial_deep = initial_deep
        self.segno = ''
        self.move = dict()

    def ripristino(self):
        self.move = dict()

    # True -----> devo memorizzare le mosse migliori
    # False ----> non devo memorizzarle
    def check_start_memory(self, deep):
        if self.initial_deep - deep == 2:
            return True
        else:
            return False

    def add_move(self, mossa, board):
        self.move[type_table(board)] = mossa
