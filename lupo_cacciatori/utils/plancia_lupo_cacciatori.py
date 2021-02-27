def ordine():
    scacchiera = [['O' if ((i+j) % 2 == 0 and j == 7)
                   else '' for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            if (i+j) % 2 == 1:
                scacchiera[i][j] = '#'
    scacchiera[0][4] = 'X'
    return scacchiera


class plancia():
    def __init__(self, lato=3):
        self.lato = lato*2
        # CACCIATORI ---> 'O'
        # LUPO ---------> 'X'
        self.plancia = ordine()

    def reset(self):
        self.plancia = ordine()

    def stampa_plancia(self):
        def quadrato(simbolo=''):
            square = [['  ' for j in range(self.lato)]
                      for i in range(self.lato)]
            if simbolo == 'X' or simbolo == 'x':
                for i in range(self.lato):
                    square[i][i] = 'XX'
                    square[i][self.lato - 1 - i] = 'XX'
            elif simbolo == 'O' or simbolo == 'o' or simbolo == '0':
                for i in range(self.lato):
                    for j in range(self.lato):
                        if (i - (self.lato - 1)/2)**2 + (j - (self.lato - 1)/2)**2 <= (self.lato // 2-1)**2:
                            square[i][j] = 'OO'

            elif simbolo == '#':
                for i in range(self.lato):
                    for j in range(self.lato):
                        square[i][j] = '::'
            return square

        def unire_matrici(mat1, mat2):
            for riga in range(len(mat2)):
                mat1[riga].extend(mat2[riga])

        def stampa_riga(lista):
            print('-'*self.lato*16 + '-'*9)
            riga = [['|'] for i in range(self.lato)]
            for simbolo in lista:
                unire_matrici(riga, quadrato(simbolo))
                unire_matrici(riga, [['|'] for i in range(self.lato)])
            for y in range(len(riga)):
                linea = ''
                for x in range(len(riga[0])):
                    linea += riga[y][x]
                print(linea)

        for linea in self.plancia:
            stampa_riga(linea)
        print('-'*self.lato*16 + '-'*9)

    def find(self, simb=''):
        posto = {'X': [], 'O': []}
        for i in range(8):
            for j in range(8):
                if self.plancia[i][j] == 'X':
                    posto['X'].append((i, j))
                elif self.plancia[i][j] == 'O':
                    posto['O'].append((i, j))
        if simb == 'X' and len(posto['X']) == 1:
            return posto['X'][0]
        elif simb == 'X' and len(posto['X']) != 1:
            return posto['X']
        elif simb == 'O':
            return tuple(posto['O'])
        else:
            return posto

    def posiziona_lupo(self, rotta):
        # LUPO -------------------> 'X'
        # Possibili rotte --------> 'NE' 'NO' 'SE' 'SO'

        if type(self.find('X')) == type(list()):
            print('Errore posiziona_lupo: self.find() ha ritornato una lista')
        else:
            posto_attuale = self.find('X')

        if rotta == 'NE':
            posto_futuro = (posto_attuale[0]-1, posto_attuale[1]+1)
        elif rotta == 'NO':
            posto_futuro = (posto_attuale[0]-1, posto_attuale[1]-1)
        elif rotta == 'SE':
            posto_futuro = (posto_attuale[0]+1, posto_attuale[1]+1)
        elif rotta == 'SO':
            posto_futuro = (posto_attuale[0]+1, posto_attuale[1]-1)
        else:
            print('Errore posiziona_lupo: Rotta definita male')

        self.plancia[posto_attuale[0]][posto_attuale[1]] = ''
        self.plancia[posto_futuro[0]][posto_futuro[1]] = 'X'

    def posiziona_cacciatore(self, coo_attuale, rotta):
        # CACCIATORI -------------> 'O'
        # Possibili rotte --------> 'NE' 'NO'
        if rotta == 'NE':
            posto_futuro = (coo_attuale[0]-1, coo_attuale[1]+1)
        elif rotta == 'NO':
            posto_futuro = (coo_attuale[0]-1, coo_attuale[1]-1)
        else:
            print('Errore posiziona_cacciatore: Rotta definita male')

        self.plancia[coo_attuale[0]][coo_attuale[1]] = ''
        self.plancia[posto_futuro[0]][posto_futuro[1]] = 'O'

    # Controlla che il numero delle pedine sulla plancia sia corretto e che siano posizionate sulle caselle corrette
    def check_plancia(self):
        # True ---> NON OK
        # False --> OK
        pedine_dict = self.find()
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

        posto_lupo = self.find('X')
        posti_cacciatori = []
        posti_cacciatori.extend(self.find('O'))

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
        posti_cacciatori.extend(self.find('O'))
        if posto_cacciatore not in posti_cacciatori:
            return True
        else:
            posti_cacciatori.remove(posto_cacciatore)

        # Controllo che la rotta del Cacciatore che voglio muovere sia compatibile con la Plancia e le pedine
        posti_cacciatori.append(self.find('X'))
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
        posti_cacciatori.extend(self.find('O'))
        posto_lupo = self.find('X')

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
