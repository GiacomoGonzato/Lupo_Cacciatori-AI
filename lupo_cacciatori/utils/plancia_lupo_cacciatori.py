def ordine():
    scacchiera = ['' for i in range(64)]
    for i in range(1, 8, 2):
        scacchiera[i] = 'O'
    scacchiera[60] = 'X'
    return scacchiera


def posizioni_proibite():
    proibito = {x for x in range(64) if ((x//8) % 2 == 0) and (x % 2 == 0)}
    proibito |= {x for x in range(64) if ((x//8) % 2 == 1) and (x % 2 == 1)}
    return proibito


# Coordinata del tipo (X,Y)
def index_to_coo(index):
    return (index % 8 + 1, index // 8 + 1)


def termini_noti_rette(lista):
    banco_prova = plancia()
    banco_prova.plancia = lista
    coo_cacciatori = {index_to_coo(n) for n in banco_prova.find('O')}
    del banco_prova
    left = min({cacciatore[1] + cacciatore[0]
                for cacciatore in coo_cacciatori})
    right = min({cacciatore[1] - cacciatore[0]
                 for cacciatore in coo_cacciatori})
    return (left, right)


def luogo_futuro(posto_attuale, rotta):
    if rotta == 'NE':
        posto_futuro = posto_attuale + 9
    elif rotta == 'NO':
        posto_futuro = posto_attuale + 7
    elif rotta == 'SE':
        posto_futuro = posto_attuale - 7
    elif rotta == 'SO':
        posto_futuro = posto_attuale - 9
    return posto_futuro


class plancia():
    def __init__(self, lato=3):
        self.lato = lato*2
        # CACCIATORI ---> 'O'
        # LUPO ---------> 'X'
        self.plancia = ordine()
        self.proibiti = posizioni_proibite()

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

        def lista_to_matrice():
            matrice = [['' if ((i % 2 == 0) and (j % 2 == 0)) or (
                (i % 2 == 1) and (j % 2 == 1)) else '#' for i in range(8)] for j in range(8)]
            lupo = self.find('X')
            cacciatori = self.find('O')
            matrice[7 - lupo//8][lupo % 8] = 'X'
            for cacciatore in cacciatori:
                matrice[7 - cacciatore // 8][cacciatore % 8] = 'O'
            return matrice

        matrice = lista_to_matrice()
        for linea in matrice:
            stampa_riga(linea)
        print('-'*self.lato*16 + '-'*9)

    def find(self, simb=''):
        if simb == 'X':
            return self.plancia.index('X')
        elif simb == 'O':
            posti = set()
            for i in range(64):
                if self.plancia[i] == 'O':
                    posti.add(i)
                if len(posti) == 4:
                    break
            return posti
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

        self.plancia[posto_attuale] = ''
        self.plancia[posto_futuro] = 'X'

    def posiziona_cacciatore(self, posto_attuale, rotta):
        # CACCIATORI -------------> 'O'
        # Possibili rotte --------> 'NE' 'NO'
        posto_futuro = luogo_futuro(posto_attuale, rotta)

        self.plancia[posto_attuale] = ''
        self.plancia[posto_futuro] = 'O'

    # Controlla che il movimento che vogliamo fare alla pedina del Lupo sia un movimento legale e che la plancia sia OK
    # True ---> NON OK
    # False --> OK
    def check_movimento_lupo(self, rotta):
        # Controllo che sia sensato
        if rotta not in {'NE', 'NO', 'SE', 'SO'}:
            return True

        posto_lupo = self.find('X')
        posti_cacciatori = self.find('O')

        # Controllo che il movimento non sia in conflitto con la Plancia di gioco o con le altre pedine
        posto_lupo_futuro = luogo_futuro(posto_lupo, rotta)
        if (posto_lupo_futuro not in range(64)) or (posto_lupo_futuro in posti_cacciatori) or (posto_lupo_futuro in self.proibiti):
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
        posti_cacciatori = self.find('O')
        if posto_cacciatore not in posti_cacciatori:
            return True
        # Controllo che la rotta del Cacciatore che voglio muovere sia compatibile con la Plancia e le pedine

        posti_cacciatori.discard(posto_cacciatore)
        posti_occupati = {x for x in posti_cacciatori}
        posti_occupati.add(self.find('X'))

        posto_cacciatore_futuro = luogo_futuro(posto_cacciatore, rotta)
        if (posto_cacciatore_futuro not in range(64)) or (posto_cacciatore_futuro in posti_occupati) or (posto_cacciatore_futuro in self.proibiti):
            return True
        else:
            return False

    # Controlla se le pedina sulla plancia sono o meno in una posizione di vittoria o sconfitta
    # Vince Cacciatori (O) ----->  1
    # Vince Lupo (X) -----------> -1
    # In corso ----------------->  0
    def check_vittoria(self):
        posti_cacciatori = self.find('O')
        posto_lupo = self.find('X')

        # Se il lupo è a fianco del cacciatore più in basso allora il lupo ha certamente vinto
        if posto_lupo // 8 <= min({x // 8 for x in posti_cacciatori}):
            return -1
        # Controllo quando il lupo ha matematicamente vinto
        coo_posto_lupo = index_to_coo(posto_lupo)
        termine_noto = termini_noti_rette(self.plancia)
        if (coo_posto_lupo[1] + coo_posto_lupo[0] < termine_noto[0]) or (coo_posto_lupo[1] - coo_posto_lupo[0] < termine_noto[1]):
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
            if not flag_cacciatori:
                break

        if flag_lupo:
            return 1
        elif flag_cacciatori:
            return -1
        else:
            return 0
