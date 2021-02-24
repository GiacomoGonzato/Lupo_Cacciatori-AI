from plancia_lupo_cacciatori import plancia


class lupo_cacciatori():
    def __init__(self, lato=2):
        self.plancia = plancia(lato)
        print('INIZIO DEL GIOCO\n')

    # Controlla che il numero delle pedine sulla plancia sia corretto e che siano posizionate sulle caselle corrette
    def check_plancia(self):
        # True ---> NON OK
        # False --> OK
        pedine_dict = self.plancia.find()
        if len(pedine_dict['O']) != 4 or len(pedine_dict['X']) != 1:
            return True
        else:
            for pedina in pedine_dict.keys():
                for coordinata in pedine_dict[pedina]:
                    if (coordinata[0] + coordinata[1]) % 2 == 1:
                        return True
            return False

    # Controlla che il movimento che vogliamo fare alla pedina del Lupo sia un movimento legale e che la plancia sia OK
    # True ---> NON OK
    # False --> OK
    def check_movimento_lupo(self, rotta):
        # Controllo che sia sensato
        if rotta not in {'NE', 'NO', 'SE', 'SO'}:
            return True

        # Controllo che la Plancia sia OK
        if self.check_plancia():
            return True

        posto_lupo = self.plancia.find('X')
        posti_cacciatori = []
        posti_cacciatori.extend(self.plancia.find('O'))

        # Controllo che il movimento non sia in conflitto con la Plancia di gioco o con le altre pedine
        if (posto_lupo[0] == 0 and rotta in {'NO', 'NE'}) or (posto_lupo[0] == 0 and posto_lupo[1] == 7 and rotta in {'NE', 'NO', 'SE'}):
            return True
        elif (posto_lupo[1] == 0 and rotta in {'SO', 'NO'}) or (posto_lupo[1] == 0 and posto_lupo[0] == 7 and rotta in {'SO', 'NO', 'SE'}):
            return True
        elif posto_lupo[1] == 7 and rotta in {'SE', 'NE'}:
            return True
        elif posto_lupo[0] == 7 and rotta in {'SE', 'SO'}:
            return True
        elif posto_lupo[0] != 0 and posto_lupo[1] != 7 and rotta == 'NE':
            if (posto_lupo[0] - 1, posto_lupo[1] + 1) in posti_cacciatori:
                return True
        elif posto_lupo[0] != 0 and posto_lupo[1] != 0 and rotta == 'NO':
            if (posto_lupo[0] - 1, posto_lupo[1] - 1) in posti_cacciatori:
                return True
        elif posto_lupo[0] != 7 and posto_lupo[1] != 7 and rotta == 'SE':
            if (posto_lupo[0] + 1, posto_lupo[1] + 1) in posti_cacciatori:
                return True
        elif posto_lupo[0] != 7 and posto_lupo[1] != 0 and rotta == 'SO':
            if (posto_lupo[0] + 1, posto_lupo[1] - 1) in posti_cacciatori:
                return True

        return False

    # Controlla che il movimento che vogliamo fare alla pedina del Cacciatore sia un movimento legale e che la plancia sia OK
    # True ---> NON OK
    # False --> OK
    def check_movimento_cacciatore(self, posto_cacciatore, rotta):
        # Controllo che la rotta abbia senso
        if rotta not in {'NE', 'NO'}:
            return True

        # Controllo che la Plancia sia OK
        if self.check_plancia():
            return True

        # Controllo che la selezione del Cacciatore che voglio far spostare sia corretta
        posti_cacciatori = []
        posti_cacciatori.extend(self.plancia.find('O'))
        if posto_cacciatore not in posti_cacciatori:
            return True
        else:
            posti_cacciatori.remove(posto_cacciatore)

        # Controllo che la rotta del Cacciatore che voglio muovere sia compatibile con la Plancia e le pedine
        posti_cacciatori.append(self.plancia.find('X'))
        posti_occupati = posti_cacciatori

        if posto_cacciatore[1] == 0 and rotta == 'NO':
            return True
        elif posto_cacciatore[1] == 7 and rotta == 'NE':
            return True
        elif posto_cacciatore[0] == 0:
            return True
        elif posto_cacciatore[1] != 7 and posto_cacciatore[0] != 0 and rotta == 'NE':
            if ((posto_cacciatore[0] - 1, posto_cacciatore[1] + 1) in posti_occupati):
                return True
        elif posto_cacciatore[1] != 0 and posto_cacciatore[0] != 0 and rotta == 'NO':
            if ((posto_cacciatore[0] - 1, posto_cacciatore[1] - 1) in posti_occupati):
                return True

        return False

    # Controlla se le pedina sulla plancia sono o meno in una posizione di vittoria o sconfitta
    # Vince Cacciatori (O) ----->  1
    # Vince Lupo (X) -----------> -1
    # In corso ----------------->  0
    def check_vittoria(self):
        posti_cacciatori = []
        posti_cacciatori.extend(self.plancia.find('O'))
        posto_lupo = self.plancia.find('X')

        if posto_lupo[0] >= max([hunter[0] for hunter in posti_cacciatori]):
            return -1

        flag_lupo = True
        for rotta in {'NE', 'NO', 'SE', 'SO'}:
            if not self.check_movimento_lupo(rotta):
                flag_lupo = False

        flag_cacciatori = True
        for rotta in {'NE', 'NO'}:
            for posto_cacciatore in posti_cacciatori:
                if not self.check_movimento_cacciatore(posto_cacciatore, rotta):
                    flag_cacciatori = False

        if flag_lupo:
            return 1
        elif flag_cacciatori and not flag_lupo:
            return -1
        else:
            return 0

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
        while self.check_vittoria() == 0:
            self.plancia.stampa_plancia()
            # Muove per primo il Lupo
            if contatore % 2 == 0:
                rotta_lupo = 'Entrare nel loop'
                # Controllo che lo spostamento richiesto per il lupo sia possibile e sensato
                while self.check_movimento_lupo(rotta_lupo):
                    rotta_lupo = input(
                        'Inserisci la ROTTA (NE, NO, SE, SO) che deve seguire il Lupo: ')
                    rotta_lupo = rotta_lupo.upper()
                self.plancia.posiziona_lupo(rotta_lupo)
            # Muove il Cacciatore
            else:
                posto_cacciatore = 'Entrare nel loop'
                # Controllo che la posizione del Cacciatore che vogliamo muovere è sensata
                while self.check_movimento_cacciatore(posto_cacciatore, 'NE') and self.check_movimento_cacciatore(posto_cacciatore, 'NO'):
                    posto_cacciatore = input(
                        'Inserisci la coordinata (riga,colonna) del cacciatore che vuoi spostare: ')
                    posto_cacciatore = str_to_tupla_coo(posto_cacciatore)
                rotta_cacciatore = 'Entrare nel loop'
                # Controllo che la rotte che quel cacciatore deve seguire sia sensata
                while self.check_movimento_cacciatore(posto_cacciatore, rotta_cacciatore):
                    rotta_cacciatore = input(
                        'Inserisci la ROTTA (NE, NO) che deve seguire il cacciatore: ')
                    rotta_cacciatore = rotta_cacciatore.upper()
                self.plancia.posiziona_cacciatore(
                    posto_cacciatore, rotta_cacciatore)
            contatore += 1

        if self.check_vittoria() == 1:
            print('HANNO VINTO I CACCIATORI')
        else:
            print('HA VINTO IL LUPO')
