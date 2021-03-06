from random import randint, shuffle
from utils.plancia_lupo_cacciatori import plancia, index_to_coo
from utils.transposition_table import transposition_table
from utils.remember_reorder_moves import next_moves, type_table
from math import *
from timeit import default_timer as timer


def check_rotte_possibili(board, simbolo, guess_move=next_moves(0)):
    rotte_possibili = list()
    if simbolo == 'X':
        testa_croce = randint(0, 1)
        if testa_croce:
            tutte_rotte_lupo = ['SO', 'SE', 'NE', 'NO']
        else:
            tutte_rotte_lupo = ['SE', 'SO', 'NE', 'NO']
        rotte_possibili = [rotta for rotta in tutte_rotte_lupo
                           if not board.check_movimento_lupo(rotta)]
    elif simbolo == 'O':
        cacciatori = board.find('O')
        for hunter in cacciatori:
            rotte_possibili.extend([(hunter, rotta) for rotta in ['NE', 'NO']
                                    if not board.check_movimento_cacciatore(hunter, rotta)])
        shuffle(rotte_possibili)
    if guess_move.segno in {'O', 'X'}:
        codice_tavolo = type_table(board)
        if codice_tavolo in guess_move.move.keys():
            mossa = guess_move.move[codice_tavolo]
            rotte_possibili.remove(mossa)
            rotte_possibili.insert(0, mossa)
    return rotte_possibili


# I cacciatori vogliono minimizzare il valore (mandare il lupo verso l'alto)
# Il lupo vuole massimizzarlo (andare verso il basso)
# Vince Cacciatori (O) ----->  1
# Vince Lupo (X) -----------> -1
# In corso ----------------->  0
def valore_mossa(guess_move, tabella, board, contatore, deep, alpha=- inf, beta=inf):
    flag = False
    check_win = board.check_vittoria()
    if check_win == 1:
        flag = True
        risultato = - inf
    elif check_win == -1:
        flag = True
        risultato = inf
    elif deep == 0:
        flag = True
        risultato = 7 - board.find('X')//8

    strategia = tabella.from_board_to_hash(board, contatore)
    if strategia in tabella.strategie_viste.keys():
        lowerbound = tabella.get_lower(strategia)
        upperbound = tabella.get_upper(strategia)
        if lowerbound >= beta:
            return lowerbound
        if upperbound <= alpha:
            return upperbound
    else:
        tabella.add_hash(board, contatore)

    if flag:
        tabella.add_lower(strategia, risultato)
        tabella.add_upper(strategia, risultato)
        return risultato

    if contatore % 2 == 0:
        valore = - inf
        val_confronto = valore
        for rotta in check_rotte_possibili(board, 'X'):
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_lupo(rotta)
            valore = max(valore, valore_mossa(guess_move, tabella,
                                              banco_prova, contatore + 1, deep - 1, alpha, beta))
            if guess_move.check_start_memory(deep) and (val_confronto < valore or valore == - inf) and (guess_move.segno == 'X'):
                guess_move.add_move(rotta, board)
                val_confronto = valore
            del banco_prova
            alpha = max(alpha, valore)
            if beta <= alpha:
                break
    else:
        valore = inf
        val_confronto = valore
        for mossa in check_rotte_possibili(board, 'O'):
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_cacciatore(mossa[0], mossa[1])
            valore = min(valore, valore_mossa(guess_move, tabella,
                                              banco_prova, contatore + 1, deep - 1, alpha, beta))
            if guess_move.check_start_memory(deep) and (val_confronto > valore or valore == inf) and (guess_move.segno == 'O'):
                guess_move.add_move(mossa, board)
                val_confronto = valore
            del banco_prova
            beta = min(beta, valore)
            if beta <= alpha:
                break

    if valore < beta:
        tabella.add_lower(strategia, valore)
    if valore > alpha:
        tabella.add_upper(strategia, valore)

    return valore


# AIUTO SUPPLEMENTARE AL DEBUGGER ----------
def debug_value(valore, contatore, rotta, coordinata=0):
    if True:
        if contatore % 2 == 0:
            print(str(rotta) + ':-------->' + str(valore))
        else:
            print('[' + str(coordinata) + ',' + str(rotta) +
                  ']:-------->' + str(valore))


def scegli_mossa_ai(guess_move, board, contatore, deep):
    # Inizializzo la transposition table
    tabella = transposition_table()
    # Devo scegliere la mossa come se fossi il lupo
    # Il lupo vuole massimizzare
    if contatore % 2 == 0:
        if deep % 2 == 0:
            deep -= 1
        guess_move.initial_deep = deep
        if index_to_coo(board.find('X'))[1] > 2 + max({index_to_coo(hunter)[1] for hunter in board.find('O')}):
            deep = 7
        valore = - inf
        possibili_rotte_lupo = check_rotte_possibili(board, 'X', guess_move)
        if len(possibili_rotte_lupo) == 1:
            return possibili_rotte_lupo[0]
        for rotta in possibili_rotte_lupo:
            if valore == - inf:
                mossa_futura = rotta
            start = timer()
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_lupo(rotta)
            move_power = valore_mossa(guess_move, tabella,
                                      banco_prova, contatore + 1, deep - 1, valore, inf)
            debug_value(move_power, contatore, rotta)
            if valore < move_power:
                mossa_futura = rotta
                valore = move_power
            end = timer()
            print(end - start)
            print()
            if valore == inf:
                break
            del banco_prova
    # Devo scegliere quale cacciatore muovere e come muoverlo
    # I cacciatori vogliono minimizzare
    else:
        if deep % 2 == 1:
            deep -= 1
        guess_move.initial_deep = deep
        valore = inf
        for mossa in check_rotte_possibili(board, 'O', guess_move):
            if valore == inf:
                mossa_futura = mossa
            start = timer()
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_cacciatore(mossa[0], mossa[1])
            move_power = valore_mossa(guess_move, tabella,
                                      banco_prova, contatore + 1, deep - 1, - inf, valore)
            debug_value(move_power, contatore, mossa[1], mossa[0])
            if valore > move_power:
                mossa_futura = mossa
                valore = move_power
            end = timer()
            print(end - start)
            print()
            if valore == - inf:
                break
            del banco_prova
    del tabella
    return mossa_futura
