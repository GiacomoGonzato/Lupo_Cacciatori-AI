class next_moves():
    def __init__(self, initial_deep):
        self.initial_deep = initial_deep
        self.hash_values = dict()
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

    def from_board_to_hash(self, board, contatore):
        tavola_associata = 0
        for cacciatore in board.find('O'):
            tavola_associata ^= self.hash_values['O'][cacciatore]
        tavola_associata ^= self.hash_values['X'][board.find('X')]
        if contatore % 2 == 0:
            tavola_associata ^= self.hash_values[0]
        else:
            tavola_associata ^= self.hash_values[1]
        return tavola_associata

    def add_move(self, mossa, board, tabella):
        if self.segno == 'X':
            contatore = 0
        else:
            contatore = 1
        self.move[tabella.from_board_to_hash(board, contatore)] = mossa
