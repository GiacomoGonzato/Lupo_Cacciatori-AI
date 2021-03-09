from utils.plancia_lupo_cacciatori import plancia, index_to_coo
from utils.transposition_table import scelta_casuale, transposition_table
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


# True ---> i cacciatori hanno lasciato dei buchi tra di loro
# False --> non l'hanno fatto
# Se non sono in formazione penalizzo
def check_cacciatori_formazione(board):
    posti_cacciatori = board.find('O')
    copia_posti = [x for x in posti_cacciatori]
    copia_posti.sort()
    righe_cacciatori = {x//8 for x in posti_cacciatori}
    if len(righe_cacciatori) >= 3:
        return True
    elif len(righe_cacciatori) <= 1:
        return False
    else:
        for i in range(3):
            if (min(posti_cacciatori)//8) % 2 == 0:
                if ((copia_posti[i+1] - copia_posti[i]) not in {2, 9}):
                    return True
            else:
                if ((copia_posti[i+1] - copia_posti[i]) not in {2, 3}):
                    return True
    return False


def middle_value(valori):
    return (sum(valori) / len(valori))


def deviazione_standard(valori):
    media = middle_value(valori)
    valori_quadri_centrati = [(i - media)**2 for i in valori]
    return sqrt(middle_value(valori_quadri_centrati))


def deviazione_from_index(valori):
    punti = {index_to_coo(x) for x in valori}
    return deviazione_from_coo(punti)


def deviazione_from_coo(punti):
    valori_x = [i[0] for i in punti]
    valori_y = [i[1] for i in punti]
    return (deviazione_standard(valori_x), deviazione_standard(valori_y))


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


def conteggio_extra_inizio_lupo(banco):
    totale = 0
    (deviazione_x, deviazione_y) = deviazione_from_index(banco.find('O'))
    totale += deviazione_y
    return totale


def conteggio_extra_inizio_cacciatori(banco):
    totale = 0
    if check_cacciatori_formazione(banco):
        totale += 20
    (deviazione_x, deviazione_y) = deviazione_from_index(banco.find('O'))
    totale += deviazione_y
    return totale


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
        valore = - inf
        for rotta in check_rotte_possibili(board, 'X'):
            banco_prova = plancia()
            banco_prova.plancia = [x for x in board.plancia]
            banco_prova.posiziona_lupo(rotta)
            move_power = conteggio_extra_inizio_lupo(banco_prova)
            move_power += valore_mossa(tabella,
                                       banco_prova, contatore + 1, deep - 1, valore, inf)
            debug_value(move_power, contatore, rotta)
            if valore <= move_power:
                mossa_futura = rotta
                valore = move_power
            if valore == inf:
                break
            del banco_prova
    # Devo scegliere quale cacciatore muovere e come muoverlo
    # I cacciatori vogliono minimizzare
    else:
        valore = inf
        for coordinata in board.find('O'):
            for rotta in check_rotte_possibili(board, 'O', coordinata):
                start = timer()
                banco_prova = plancia()
                banco_prova.plancia = [x for x in board.plancia]
                banco_prova.posiziona_cacciatore(coordinata, rotta)
                move_power = conteggio_extra_inizio_cacciatori(banco_prova)
                move_power += valore_mossa(tabella,
                                           banco_prova, contatore + 1, deep - 1, - inf, valore)
                debug_value(move_power, contatore, rotta, coordinata)
                if valore >= move_power:
                    mossa_futura = (coordinata, rotta)
                    valore = move_power
                if valore == - inf:
                    break
                del banco_prova
                end = timer()
                print(end - start)
                print()
            if valore == - inf:
                break
    del tabella
    return mossa_futura
