from random import *


def scelta_casuale():
    high = 2**64
    dizionario = dict()
    dizionario['O'] = tuple([randint(0, high) for x in range(64)])
    dizionario['X'] = tuple([randint(0, high) for x in range(64)])
    return dizionario


class transposition_table():
    def __init__(self):
        self.possibilita = scelta_casuale()
        self.strategie_viste = dict()

    def from_board_to_hash(self, board):
        tavola_associata = 0
        for cacciatore in board.find('O'):
            tavola_associata ^= self.possibilita['O'][cacciatore]
        tavola_associata ^= self.possibilita['X'][board.find('X')]
        return tavola_associata

    def add_hash(self, board, valore):
        self.strategie_viste[self.from_board_to_hash(board)] = valore
