def ordine():
    scacchiera = [['O' if ((i+j) % 2 == 0 and j == 7)
                   else '' for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            if (i+j) % 2 == 1:
                scacchiera[i][j] = '#'
    scacchiera[0][4] = 'X'
    return scacchiera


def luogo_futuro(posto_attuale, rotta):
    if rotta == 'NE':
        posto_futuro = (posto_attuale[0]-1, posto_attuale[1]+1)
    elif rotta == 'NO':
        posto_futuro = (posto_attuale[0]-1, posto_attuale[1]-1)
    elif rotta == 'SE':
        posto_futuro = (posto_attuale[0]+1, posto_attuale[1]+1)
    elif rotta == 'SO':
        posto_futuro = (posto_attuale[0]+1, posto_attuale[1]-1)
    return posto_futuro


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
        if simb == 'X':
            for i in range(8):
                riga = self.plancia[i]
                if riga.count('X') != 0:
                    return (i, riga.index('X'))
        elif simb == 'O':
            posti_cacciatori = []
            for i in range(8):
                riga = self.plancia[i]
                if riga.count('O') == 1:
                    posti_cacciatori.append((i, riga.index('O')))
                elif riga.count('O') >= 2:
                    for j in range(8):
                        if riga[j] == 'O':
                            posti_cacciatori.append((i, j))
            return posti_cacciatori
        else:
            posti = dict()
            posti['X'] = self.find('X')
            posti['O'] = self.find('O')
            return posti

    def posiziona_lupo(self, rotta):
        # LUPO -------------------> 'X'
        # Possibili rotte --------> 'NE' 'NO' 'SE' 'SO'

        posto_attuale = self.find('X')
        posto_futuro = luogo_futuro(posto_attuale, rotta)

        self.plancia[posto_attuale[0]][posto_attuale[1]] = ''
        self.plancia[posto_futuro[0]][posto_futuro[1]] = 'X'

    def posiziona_cacciatore(self, coo_attuale, rotta):
        # CACCIATORI -------------> 'O'
        # Possibili rotte --------> 'NE' 'NO'
        posto_futuro = luogo_futuro(coo_attuale, rotta)

        self.plancia[coo_attuale[0]][coo_attuale[1]] = ''
        self.plancia[posto_futuro[0]][posto_futuro[1]] = 'O'

    # Controlla che il movimento che vogliamo fare alla pedina del Lupo sia un movimento legale e che la plancia sia OK
    # True ---> NON OK
    # False --> OK
    def check_movimento_lupo(self, rotta):
        # Controllo che sia sensato
        if rotta not in {'NE', 'NO', 'SE', 'SO'}:
            return True

        posto_lupo = self.find('X')
        posti_cacciatori = []
        posti_cacciatori.extend(self.find('O'))

        # Controllo che il movimento non sia in conflitto con la Plancia di gioco o con le altre pedine
        posto_lupo_futuro = luogo_futuro(posto_lupo, rotta)
        if (posto_lupo_futuro[0] not in range(8)) or (posto_lupo_futuro[1] not in range(8)) or (posto_lupo_futuro in posti_cacciatori):
            return True
        else:
            return False

    # Controlla che il movimento che vogliamo fare alla pedina del Cacciatore sia un movimento legale e che la plancia sia OK
    # True ---> NON OK
    # False --> OK
    def check_movimento_cacciatore(self, posto_cacciatore, rotta):
        # Controllo che la rotta abbia senso
        if rotta not in {'NE', 'NO'}:
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

        posto_cacciatore_futuro = luogo_futuro(posto_cacciatore, rotta)
        if (posto_cacciatore_futuro[0] not in range(8)) or (posto_cacciatore_futuro[1] not in range(8)) or (posto_cacciatore_futuro in posti_occupati):
            return True
        else:
            return False

    # Controlla se le pedina sulla plancia sono o meno in una posizione di vittoria o sconfitta
    # Vince Cacciatori (O) ----->  1
    # Vince Lupo (X) -----------> -1
    # In corso ----------------->  0
    def check_vittoria(self):
        posti_cacciatori = []
        posti_cacciatori.extend(self.find('O'))
        posto_lupo = self.find('X')

        # Se il lupo è a fianco del cacciatore più in basso allora il lupo ha certamente vinto
        if posto_lupo[0] >= max([hunter[0] for hunter in posti_cacciatori]):
            return -1
        
        # flag_lupo ---> True se il lupo non si può muovere
        #           ---> False altrimenti
        flag_lupo = True
        for rotta in {'NE', 'NO', 'SE', 'SO'}:
            if not self.check_movimento_lupo(rotta):
                flag_lupo = False
                break

        # flag_cacciatori ---> True se i cacciatori non si possono muovere
        #                 ---> False altrimenti
        flag_cacciatori = True
        for rotta in {'NE', 'NO'}:
            for posto_cacciatore in posti_cacciatori:
                if not self.check_movimento_cacciatore(posto_cacciatore, rotta):
                    flag_cacciatori = False
                    break
            if flag_cacciatori == False:
                break

        if flag_lupo:
            return 1
        elif flag_cacciatori and not flag_lupo:
            return -1
        else:
            return 0
