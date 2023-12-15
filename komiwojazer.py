import random
import copy

def generator_macierzy(liczba, gestosc):
    generowana = [[0]*liczba for x in range(liczba)]
    for i in range(liczba):
        for j in range(liczba):
            if(i == j):
                continue
            losowo = random.randint(0,100)/100
            if(losowo < gestosc and generowana[i][j] == 0):
                generowana[i][j] = 1
                generowana[j][i] = 1
    wierzcholki = [0]*liczba
    for i in range(liczba):
        wierzcholki[i] = random.randint(-6,6)
    test = copy.deepcopy(generowana)
    if(czy_hamilton(test, [0], True)):
        return generowana, wierzcholki
    generator_macierzy(liczba, gestosc)

def generator_wag(liczba, graf):
    graf_wagi = copy.deepcopy(graf)
    for i in range(liczba):
        for j in range(i+1,liczba):
            if(graf[i][j] == 1):
                waga = random.randint(-5,5)
                graf_wagi[i][j] = waga
                graf_wagi[j][i] = waga
    return graf_wagi

def bound(graf, cykl):
    zredukowany_graf = copy.deepcopy(graf)
    n = len(graf)
    for w in cykl:
        for i in range(n):
            zredukowany_graf[w][i] = 0
            zredukowany_graf[i][w] = 0
    for i in range(n):
        licznik = 0
        for j in range(n):
            if(zredukowany_graf[i][j] > 0):
                licznik += 1
        if((licznik < 2)
                and (not i in cykl)
                and ((licznik != 1) or ((graf[cykl[-1]][i] == 0) and (graf[i][cykl[0]]==0)))
                and ((len(cykl) < n-1) or (licznik != 0) or (graf[cykl[-1]][i]==0) or (graf[i][cykl[0]] == 0))):
            return False
    odleglosci = [-1]*n
    zoptymalizowane = [False]*n
    for w in cykl:
        odleglosci[w] = -2
    pierwszy_lepszy = -1
    for i in range(n):
        if(odleglosci[i] == -1):
            pierwszy_lepszy = i
            odleglosci[i] = 0
            break
    for i in range(n):
        najmniejszy = -1
        for j in range(n):
            if((odleglosci[j] >= 0) and (zoptymalizowane[j] == False)):
                if((najmniejszy == -1) or (odleglosci[najmniejszy] > odleglosci[j])):
                    najmniejszy = j
        if(najmniejszy < 0):
            break
        zoptymalizowane[najmniejszy] = True
        for j in range(n):
            if(zredukowany_graf[najmniejszy][j] == 0):
                continue
            if((odleglosci[j] < 0) or (odleglosci[najmniejszy]+1 < odleglosci[j])):
                odleglosci[j] = odleglosci[najmniejszy]+1
    for i in range(n):
        if(odleglosci[i] == -1):
            return False
    return True

cykle = []

def czy_hamilton(graf, cykl, one_enough):
    global cykle
    if(len(cykl) == 1):
        cykle = []
    if(len(cykl) == len(graf)):
        if(graf[cykl[0]][cykl[-1]] > 0):
            cykle.append(cykl.copy())
    else:
        if(bound(graf, cykl)):
            biezacy = cykl[-1]
            for i in range(len(graf)):
                if(graf[biezacy][i] == 0):
                    continue
                if(not i in cykl):
                    cykl.append(i)
                    czy_hamilton(graf, cykl, one_enough)
                    if(one_enough and len(cykle) > 0):
                         return
                    cykl.pop(-1)

def heurystyka(graf, wierzcholki):
    global cykle
    wynik = {'cykl':None, 'budzet':0}
    wybrany = None
    wartosc = 1000000
    kopia = wierzcholki
    for i in range(len(kopia)):
        if(kopia[i] > wartosc):
            wartosc = kopia[i]
            wybrany = i
    for cykl in cykle:
        piwot = 0
        for j in range(len(cykl)):
            if(cykl[j] == wybrany):
                piwot = j
        nowy_cykl = copy.deepcopy(cykl)
        nowy_cykl = nowy_cykl[piwot:len(cykl)]+nowy_cykl[0:piwot]
        current = (-1)*kopia[wybrany]
        for j in range(len(nowy_cykl)-1):
            current += graf[nowy_cykl[j]][nowy_cykl[j+1]]
            if(current < najmniejsza):
                najmniejsza = current
            current -= kopia[nowy_cykl[j+1]]
            if(current < najmniejsza):
                najmniejsza = current
        current += graf[nowy_cykl[0]][nowy_cykl[-1]]
        if(current < wartosc):
            wartosc = current
            wynik = {'cykl':nowy_cykl, 'budzet':wartosc}

def dokladne(graf, cykl, wierzcholki, budzet):
    global cykle
    if(len(cykl) == 1):
        cykle = []
    if(len(cykl) == len(graf)):
        if(graf[cykl[0]][cykl[-1]] > 0):
            cykle.append(cykl.copy())
    else:
        if(bound(graf, cykl)):
            biezacy = cykl[-1]
            for i in range(len(graf)):
                if(graf[biezacy][i] == 0):
                    continue
                if(not i in cykl):
                    cykl.append(i)
                    czy_hamilton(graf, cykl, one_enough)
                    if(one_enough and len(cykle) > 0):
                         return
                    cykl.pop(-1)

gestosc = random.randint(5, 10)/10
ilosc = 10

macierz, wierzcholki = generator_macierzy(ilosc, gestosc)
graf = copy.deepcopy(macierz)
wagi = copy.deepcopy(wierzcholki)
graf_final = generator_wag(ilosc, graf)
graf = copy.deepcopy(graf_final)
wynik_heur = heurystyka(graf, wagi)
wynik_dokl = dokladne(graf, wagi)
print(f'wynik_heur: {wynik_heur}')
print(f'wynik_dokl: {wynik_dokl}')