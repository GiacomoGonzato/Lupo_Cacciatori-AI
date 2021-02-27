from utils.plancia_lupo_cacciatori import plancia
from utils.ai_lupo_cacciatori import scegli_mossa_ai


def str_to_tupla_coo(stringa):
    num = list()
    for i in stringa:
        if ord(i) >= 49 and ord(i) <= 56:
            num.append(int(i) - 1)
    if len(num) != 2:
        return (9, 9)
    else:
        return tuple(num)


def distanza_posizioni(coo1, coo2):
    return abs(coo1[0] - coo2[0]) + abs(coo1[1] - coo2[1])


class lupo_cacciatori():
    def __init__(self, lato=2):
        self.plancia = plancia(lato)
        print('INIZIO DEL GIOCO\n')

    def reset_plancia(self):
        self.plancia.reset()

    # Logica di gioco
    def play(self, profondita=4):
        contatore = 0
        computer = 'entra nel loop'
        while computer not in {'y', 'n'}:
            computer = input('Vuoi giocare contro il computer? [Y/N] ').lower()
        if computer == 'y':
            cpwho = 'entra nel loop'
            while cpwho not in {'x', 'o'}:
                cpwho = input(
                    'Contro chi vuoi giocare? (X --> lupo, O --> cacciatori) ').lower()

            if cpwho == 'o':
                check_win = 0
                while check_win == 0:
                    self.plancia.stampa_plancia()
                    # Muove per primo il Lupo
                    flag_contatto = False
                    for cacciatore in self.plancia.find('O'):
                        if distanza_posizioni(self.plancia.find('X'), cacciatore) <= 2:
                            flag_contatto = True
                            break
                    if flag_contatto:
                        deep = profondita + 2
                    else:
                        deep = profondita
                    if contatore % 2 == 0:
                        rotta_lupo = 'Entrare nel loop'
                        # Controllo che lo spostamento richiesto per il lupo sia possibile e sensato
                        while self.plancia.check_movimento_lupo(rotta_lupo):
                            rotta_lupo = input(
                                'Inserisci la ROTTA (NE, NO, SE, SO) che deve seguire il Lupo: ')
                            rotta_lupo = rotta_lupo.upper()
                        self.plancia.posiziona_lupo(rotta_lupo)
                    # Muove il Cacciatore
                    else:
                        mossa_cacciatore = scegli_mossa_ai(
                            self.plancia, contatore, deep)
                        self.plancia.posiziona_cacciatore(
                            mossa_cacciatore[0], mossa_cacciatore[1])
                    contatore += 1
                    if contatore >= 10:
                        check_win = self.plancia.check_vittoria()
            else:
                check_win = 0
                while check_win == 0:
                    self.plancia.stampa_plancia()
                    # Muove per primo il Lupo
                    flag_contatto = False
                    for cacciatore in self.plancia.find('O'):
                        if distanza_posizioni(self.plancia.find('X'), cacciatore) <= 2:
                            flag_contatto = True
                            break
                    if flag_contatto:
                        deep = profondita + 2
                    else:
                        deep = profondita
                    if contatore % 2 == 0:
                        rotta_lupo = scegli_mossa_ai(
                            self.plancia, contatore, deep)
                        self.plancia.posiziona_lupo(rotta_lupo)
                    # Muove il Cacciatore
                    else:
                        posto_cacciatore = 'Entrare nel loop'
                        # Controllo che la posizione del Cacciatore che vogliamo muovere è sensata
                        while self.plancia.check_movimento_cacciatore(posto_cacciatore, 'NE') and self.plancia.check_movimento_cacciatore(posto_cacciatore, 'NO'):
                            posto_cacciatore = input(
                                'Inserisci la coordinata (riga,colonna) del cacciatore che vuoi spostare: ')
                            posto_cacciatore = str_to_tupla_coo(
                                posto_cacciatore)
                        rotta_cacciatore = 'Entrare nel loop'
                        # Controllo che la rotte che quel cacciatore deve seguire sia sensata
                        while self.plancia.check_movimento_cacciatore(posto_cacciatore, rotta_cacciatore):
                            rotta_cacciatore = input(
                                'Inserisci la ROTTA (NE, NO) che deve seguire il cacciatore: ')
                            rotta_cacciatore = rotta_cacciatore.upper()
                        self.plancia.posiziona_cacciatore(
                            posto_cacciatore, rotta_cacciatore)
                    contatore += 1
                    if contatore >= 10:
                        check_win = self.plancia.check_vittoria()
        else:
            check_win = 0
            while check_win == 0:
                self.plancia.stampa_plancia()
                # Muove per primo il Lupo
                if contatore % 2 == 0:
                    rotta_lupo = 'Entrare nel loop'
                    # Controllo che lo spostamento richiesto per il lupo sia possibile e sensato
                    while self.plancia.check_movimento_lupo(rotta_lupo):
                        rotta_lupo = input(
                            'Inserisci la ROTTA (NE, NO, SE, SO) che deve seguire il Lupo: ')
                        rotta_lupo = rotta_lupo.upper()
                    self.plancia.posiziona_lupo(rotta_lupo)
                # Muove il Cacciatore
                else:
                    posto_cacciatore = 'Entrare nel loop'
                    # Controllo che la posizione del Cacciatore che vogliamo muovere è sensata
                    while posto_cacciatore not in self.plancia.find('O'):
                        posto_cacciatore = input(
                            'Inserisci la coordinata (riga,colonna) del cacciatore che vuoi spostare: ')
                        posto_cacciatore = str_to_tupla_coo(posto_cacciatore)
                    rotta_cacciatore = 'Entrare nel loop'
                    # Controllo che la rotte che quel cacciatore deve seguire sia sensata
                    while self.plancia.check_movimento_cacciatore(posto_cacciatore, rotta_cacciatore):
                        rotta_cacciatore = input(
                            'Inserisci la ROTTA (NE, NO) che deve seguire il cacciatore: ')
                        rotta_cacciatore = rotta_cacciatore.upper()
                    self.plancia.posiziona_cacciatore(
                        posto_cacciatore, rotta_cacciatore)
                contatore += 1
                if contatore >= 10:
                    check_win = self.plancia.check_vittoria()

        if check_win == 1:
            print('HANNO VINTO I CACCIATORI')
        else:
            print('HA VINTO IL LUPO')
