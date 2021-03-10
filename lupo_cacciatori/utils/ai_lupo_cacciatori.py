from utils.plancia_lupo_cacciatori import plancia, index_to_coo
from utils.transposition_table import transposition_table
from math import *
from timeit import default_timer as timer


def check_rotte_possibili(board, simbolo, posto_cacciatore=0):
    rotte_possibili = list()
    if simbolo == 'X':
        for rotta in ['SO', 'SE', 'NE', 'NO']:
            if not board.check_movimento_lupo(rotta):
                rotte_possibili.append(rotta)
    elif simbolo == 'O':
        for rotta in ['NE', 'NO']:
            if not board.check_movimento_cacciatore(posto_cacciatore, rotta):
                rotte_possibili.append(rotta)
    return rotte_possibili


# I cacciatori vogliono minimizzare il valore (mandare il lupo verso l'alto)
# Il lupo vuole massimizzarlo (andare verso il basso)
# Vince Cacciatori (O) ----->  1
# Vince Lupo (X) -----------> -1
# In corso ----------------->  0
def valore_mossa(tabella, board, contatore, deep, alpha=- inf, beta=inf):
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
        for rotta in check_rotte_possibili(board, 'X'):
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_lupo(rotta)
            valore = max(valore, valore_mossa(tabella,
                                              banco_prova, contatore + 1, deep - 1, alpha, beta))
            del banco_prova
            alpha = max(alpha, valore)
            if beta <= alpha:
                break
    else:
        valore = inf
        for coordinata in board.find('O'):
            for rotta in check_rotte_possibili(board, 'O', coordinata):
                banco_prova = plancia()
                banco_prova.plancia = [x for x in board.plancia]
                banco_prova.posiziona_cacciatore(coordinata, rotta)
                valore = min(valore, valore_mossa(tabella,
                                                  banco_prova, contatore + 1, deep - 1, alpha, beta))
                del banco_prova
                beta = min(beta, valore)
                if beta <= alpha:
                    break
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


def scegli_mossa_ai(board, contatore, deep):
    # Inizializzo la transposition table
    tabella = transposition_table()
    # Devo scegliere la mossa come se fossi il lupo
    # Il lupo vuole massimizzare
    if contatore % 2 == 0:
        if deep % 2 == 0:
            deep -= 1
        if index_to_coo(board.find('X'))[1] > 2 + max({index_to_coo(hunter)[1] for hunter in board.find('O')}):
            deep = 7
        valore = - inf
        for rotta in check_rotte_possibili(board, 'X'):
            if valore == - inf:
                mossa_futura = rotta
            start = timer()
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_lupo(rotta)
            move_power = valore_mossa(tabella,
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
        valore = inf
        pool_mosse = list()
        for coordinata in board.find('O'):
            pool_mosse.extend([(coordinata, rotta)
                               for rotta in check_rotte_possibili(board, 'O', coordinata)])
        for mossa in pool_mosse:
            if valore == inf:
                mossa_futura = mossa
            start = timer()
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_cacciatore(mossa[0], mossa[1])
            move_power = valore_mossa(tabella,
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
