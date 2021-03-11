from utils.plancia_lupo_cacciatori import plancia
from utils.remember_reorder_moves import next_moves
from utils.ai_lupo_cacciatori import scegli_mossa_ai


def str_to_index(stringa):
    num = list()
    for i in stringa:
        if ord(i) >= 49 and ord(i) <= 56:
            num.append(int(i) - 1)
    if len(num) != 2:
        return 0
    else:
        return 8 * num[0] + num[1]


class lupo_cacciatori():
    def __init__(self, lato=2):
        self.plancia = plancia(lato)

    def reset_plancia(self):
        self.plancia.reset()

    def opzioni_gioco(self):
        flag = True
        giocatore = ''
        while flag:
            print('-'*35)
            print('GIOCO DELLA VOLPE E DEI CACCIATORI')
            print('1) Persona Vs Persona')
            print('2) Persona Vs PC')
            print('3) PC Vs PC')
            print('-'*35)
            print()
            tipo_partita = input(
                'Seleziona il tipo di partita che vuoi fare: ')
            if tipo_partita.isnumeric():
                tipo_partita = int(tipo_partita)
                if tipo_partita in {1, 2, 3}:
                    flag = False
        if tipo_partita == 2:
            flag = True
            while flag:
                giocatore = input(
                    'Con che fazione vuoi giocare? (Volpe "X", Cacciatori "O"): ').upper()
                if giocatore in {'O', 'X'}:
                    flag = False
        return (tipo_partita, giocatore)

    # Logica di gioco
    def play(self, deep=4):
        # Capisco il tipo di partita che voglio fare
        opzioni = self.opzioni_gioco()
        contatore = 0

        # Persona Vs Persona
        if opzioni[0] == 1:
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
                        posto_cacciatore = str_to_index(posto_cacciatore)
                    rotta_cacciatore = 'Entrare nel loop'
                    # Controllo che la rotte che quel cacciatore deve seguire sia sensata
                    while self.plancia.check_movimento_cacciatore(posto_cacciatore, rotta_cacciatore):
                        rotta_cacciatore = input(
                            'Inserisci la ROTTA (NE, NO) che deve seguire il cacciatore: ')
                        rotta_cacciatore = rotta_cacciatore.upper()
                    self.plancia.posiziona_cacciatore(
                        posto_cacciatore, rotta_cacciatore)
                contatore += 1
                check_win = self.plancia.check_vittoria()

        # Computer Vs Persona
        elif opzioni[0] == 2:
            # Inizializzo la memoria per la scelta delle mosse future della AI
            guess_move = next_moves(deep)
            # Il computer fa il LUPO
            if opzioni[1] == 'O':
                check_win = 0
                while check_win == 0:
                    self.plancia.stampa_plancia()
                    # Muove per primo il Lupo
                    if contatore % 2 == 0:
                        guess_move.segno = 'X'
                        rotta_lupo = scegli_mossa_ai(guess_move,
                                                     self.plancia, contatore, deep)
                        self.plancia.posiziona_lupo(rotta_lupo)
                    # Muove il Cacciatore
                    else:
                        posto_cacciatore = 'Entrare nel loop'
                        # Controllo che la posizione del Cacciatore che vogliamo muovere è sensata
                        while self.plancia.check_movimento_cacciatore(posto_cacciatore, 'NE') and self.plancia.check_movimento_cacciatore(posto_cacciatore, 'NO'):
                            posto_cacciatore = input(
                                'Inserisci la coordinata (riga,colonna) del cacciatore che vuoi spostare: ')
                            posto_cacciatore = str_to_index(
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
                    check_win = self.plancia.check_vittoria()

            # Il computer fa i CACCIATORI
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
                        guess_move.segno = 'O'
                        mossa_cacciatore = scegli_mossa_ai(guess_move,
                                                           self.plancia, contatore, deep)
                        self.plancia.posiziona_cacciatore(
                            mossa_cacciatore[0], mossa_cacciatore[1])
                    contatore += 1
                    check_win = self.plancia.check_vittoria()

        # Computer Vs Computer
        else:
            guess_move_lupo = next_moves(deep)
            guess_move_cacciatore = next_moves(deep)
            check_win = 0
            while check_win == 0:
                self.plancia.stampa_plancia()
                # Muove per primo il Lupo
                if contatore % 2 == 0:
                    guess_move_lupo.segno = 'X'
                    rotta_lupo = scegli_mossa_ai(guess_move_lupo,
                                                 self.plancia, contatore, deep)
                    self.plancia.posiziona_lupo(rotta_lupo)
                # Muove il Cacciatore
                else:
                    guess_move_cacciatore.segno = 'O'
                    mossa_cacciatore = scegli_mossa_ai(guess_move_cacciatore,
                                                       self.plancia, contatore, deep)
                    self.plancia.posiziona_cacciatore(
                        mossa_cacciatore[0], mossa_cacciatore[1])
                contatore += 1
                check_win = self.plancia.check_vittoria()

        self.plancia.stampa_plancia()
        if check_win == 1:
            print('HANNO VINTO I CACCIATORI')
        else:
            print('HA VINTO IL LUPO')
