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
