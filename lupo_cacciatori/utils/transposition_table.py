from random import *
from math import *


def scelta_casuale():
    high = 2**64
    dizionario = dict()
    dizionario['O'] = tuple([randint(0, high) for x in range(64)])
    dizionario['X'] = tuple([randint(0, high) for x in range(64)])
    dizionario[0] = randint(0, high)
    dizionario[1] = randint(0, high)
    return dizionario


class transposition_table():
    def __init__(self):
        self.possibilita = scelta_casuale()
        self.strategie_viste = dict()

    def from_board_to_hash(self, board, contatore):
        tavola_associata = 0
        for cacciatore in board.find('O'):
            tavola_associata ^= self.possibilita['O'][cacciatore]
        tavola_associata ^= self.possibilita['X'][board.find('X')]
        if contatore % 2 == 0:
            tavola_associata ^= self.possibilita[0]
        else:
            tavola_associata ^= self.possibilita[1]
        return tavola_associata

    def add_hash(self, board, contatore):
        strategia = self.from_board_to_hash(board, contatore)
        self.strategie_viste[strategia] = dict()
        self.strategie_viste[strategia]['lowerbound'] = - inf
        self.strategie_viste[strategia]['upperbound'] = inf

    def add_lower(self, strategia, lowerbound):
        self.strategie_viste[strategia]['lowerbound'] = lowerbound

    def add_upper(self, strategia, upperbound):
        self.strategie_viste[strategia]['upperbound'] = upperbound

    def get_lower(self, strategia):
        return self.strategie_viste[strategia]['lowerbound']

    def get_upper(self, strategia):
        return self.strategie_viste[strategia]['upperbound']
