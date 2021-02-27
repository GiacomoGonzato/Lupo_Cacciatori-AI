from utils.plancia_lupo_cacciatori import plancia
from utils.ai_lupo_cacciatori import scegli_mossa_ai


class lupo_cacciatori():
    def __init__(self, lato=2):
        self.plancia = plancia(lato)
        print('INIZIO DEL GIOCO\n')

    def reset_plancia(self):
        self.plancia.reset()

    # Logica di gioco
    def play(self):
        def str_to_tupla_coo(stringa):
            num = list()
            for i in stringa:
                if ord(i) >= 49 and ord(i) <= 56:
                    num.append(int(i) - 1)
            if len(num) != 2:
                return (9, 9)
            else:
                return tuple(num)

        contatore = 0
        while self.plancia.check_vittoria() == 0:
            self.plancia.stampa_plancia()
            # Muove per primo il Lupo
            if contatore % 2 == 0:
                rotta_lupo = 'Entrare nel loop'
                # Controllo che lo spostamento richiesto per il lupo sia possibile e sensato
                while self.plancia.check_movimento_lupo(rotta_lupo):
                    rotta_lupo = input(
                        'Inserisci la ROTTA (NE, NO, SE, SO) che deve seguire il Lupo: ')
                    # rotta_lupo = scegli_mossa_ai(self.plancia, contatore, 64)
                    rotta_lupo = rotta_lupo.upper()
                self.plancia.posiziona_lupo(rotta_lupo)
            # Muove il Cacciatore
            else:
                #                posto_cacciatore = 'Entrare nel loop'
                # Controllo che la posizione del Cacciatore che vogliamo muovere è sensata
                #                while self.plancia.check_movimento_cacciatore(posto_cacciatore, 'NE') and self.plancia.check_movimento_cacciatore(posto_cacciatore, 'NO'):
                #                    posto_cacciatore = input(
                #                        'Inserisci la coordinata (riga,colonna) del cacciatore che vuoi spostare: ')
                #                    posto_cacciatore = str_to_tupla_coo(posto_cacciatore)
                #                rotta_cacciatore = 'Entrare nel loop'
                # Controllo che la rotte che quel cacciatore deve seguire sia sensata
                #                while self.plancia.check_movimento_cacciatore(posto_cacciatore, rotta_cacciatore):
                #                    rotta_cacciatore = input(
                #                        'Inserisci la ROTTA (NE, NO) che deve seguire il cacciatore: ')
                #                    rotta_cacciatore = rotta_cacciatore.upper()
                #                self.plancia.posiziona_cacciatore(
                #                    posto_cacciatore, rotta_cacciatore)
                mossa_cacciatore = scegli_mossa_ai(self.plancia, contatore, 6)
                self.plancia.posiziona_cacciatore(
                    mossa_cacciatore[0], mossa_cacciatore[1])
            contatore += 1

        if self.plancia.check_vittoria() == 1:
            print('HANNO VINTO I CACCIATORI')
        else:
            print('HA VINTO IL LUPO')
