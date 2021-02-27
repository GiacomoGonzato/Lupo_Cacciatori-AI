from utils.plancia_lupo_cacciatori import plancia
from math import *


def check_rotte_possibili(board, simbolo, coordinata_cacciatore=(0, 0)):
    rotte_possibili = set()
    if simbolo == 'X':
        for rotta in {'SO', 'SE', 'NE', 'NO'}:
            if not board.check_movimento_lupo(rotta):
                rotte_possibili.add(rotta)
    elif simbolo == 'O':
        for rotta in {'NE', 'NO'}:
            if not board.check_movimento_cacciatore(coordinata_cacciatore, rotta):
                rotte_possibili.add(rotta)
    return rotte_possibili


def distanza_posizioni(coo1, coo2):
    return abs(coo1[0] - coo2[0]) + abs(coo1[1] - coo2[1])

# True ---> i cacciatori hanno lasciato dei buchi tra di loro
# False --> non l'hanno fatto


def check_cacciatori_holes(board):
    posti_cacciatori = board.find('O')
    for cacciatore in posti_cacciatori:
        compagni = {posto for posto in posti_cacciatori if posto != cacciatore}
        flag_lontano = True
        for compagno in compagni:
            if distanza_posizioni(cacciatore, compagno) <= 3:
                flag_lontano = False
                break
        if flag_lontano:
            return True
    return False


def valore_mossa(board, contatore, deep, alpha=- inf, beta=inf):
    check_win = board.check_vittoria()
    if check_win == 1:
        return - inf
    elif check_win == -1:
        return inf
    elif deep == 0:
        return board.find('X')[0]

    if contatore % 2 == 0:
        valore = - inf
        for rotta in check_rotte_possibili(board, 'X'):
            banco_prova = plancia()
            banco_prova.plancia = [[board.plancia[i][j]
                                    for j in range(8)] for i in range(8)]
            banco_prova.posiziona_lupo(rotta)
            valore = max(valore, valore_mossa(
                banco_prova, contatore + 1, deep - 1, alpha, beta))
            if check_cacciatori_holes(banco_prova):
                valore = valore + 2
            del banco_prova
            alpha = max(alpha, valore)
            if beta <= alpha:
                break
        return valore
    else:
        valore = inf
        for coordinata in board.find('O'):
            for rotta in check_rotte_possibili(board, 'O', coordinata):
                banco_prova = plancia()
                banco_prova.plancia = [[board.plancia[i][j]
                                        for j in range(8)] for i in range(8)]
                banco_prova.posiziona_cacciatore(coordinata, rotta)
                valore = min(valore, valore_mossa(
                    banco_prova, contatore + 1, deep - 1, alpha, beta))
                if check_cacciatori_holes(banco_prova):
                    valore = valore + 2
                del banco_prova
                beta = min(beta, valore)
                if beta <= alpha:
                    break
            if beta <= alpha:
                break
        return valore


def scegli_mossa_ai(board, contatore, deep):
    # Devo scegliere la mossa come se fossi il lupo
    # Il lupo vuole massimizzare
    if contatore % 2 == 0:
        valore = - inf
        for rotta in check_rotte_possibili(board, 'X'):
            banco_prova = plancia()
            banco_prova.plancia = [[board.plancia[i][j]
                                    for j in range(8)] for i in range(8)]
            banco_prova.posiziona_lupo(rotta)
            move_power = valore_mossa(banco_prova, contatore + 1, deep)
            if valore <= move_power:
                rotta_futura = rotta
                valore = move_power
            del banco_prova
        return rotta_futura
    # Devo scegliere quale cacciatore muovere e come muoverlo
    # I cacciatori vogliono minimizzare
    else:
        valore = inf
        for coordinata in board.find('O'):
            for rotta in check_rotte_possibili(board, 'O', coordinata):
                banco_prova = plancia()
                banco_prova.plancia = [[board.plancia[i][j]
                                        for j in range(8)] for i in range(8)]
                banco_prova.posiziona_cacciatore(coordinata, rotta)
                move_power = valore_mossa(banco_prova, contatore + 1, deep)
                if valore >= move_power:
                    mossa_futura = (coordinata, rotta)
                    valore = move_power
                del banco_prova
        return mossa_futura
