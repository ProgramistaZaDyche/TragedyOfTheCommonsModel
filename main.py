# glowny plik modelu
import funkcje
import wartosci

if __name__ == "__main__":
    zadowolenie_populusu = []
    zadowolenie_gracza = []
    flota_autobusow = []
    n = wartosci.liczba_uczestnikow - 1  # liczba pasazerow do poczatkowego rozsadzenia po autobusach

    # rozsadzenie graczy po autobusach
    for i in range(wartosci.liczba_autobusow):
        pojemnosc_autobus = wartosci.pojemnosc_autobus  # optymalizacja
        if n >= pojemnosc_autobus:
            flota_autobusow.append(pojemnosc_autobus)
            n -= pojemnosc_autobus
        else:
            flota_autobusow.append(n)
            n = 0
    flota_autobusow.sort()  # pasazerowie wchodza do najbardziej zapelnionego (ale niepelnego) autobusu)
    # logika jest w tym taka, ze autobus ktory jest w czesci zapelniony nadjechal troszeczke szybciej od pustego

    # przypisywanie zadowolenia
    ostatnia_iteracja = wartosci.liczba_uczestnikow - n - 1  # zeby nie wywolywac dodatkowego len() co obrot petli
    autobus_do_oproznienia = 0
    autobus_do_odwiedzenia = -1  # autobus do ktorego wsiadzie wylosowany gracz
    for i in range(wartosci.liczba_uczestnikow - n):
        ilosc_pasazerow = 0
        for iterator, autobus in enumerate(flota_autobusow):
            if not autobus:  # autobus jest pusty, rowny zero
                continue
            if autobus == wartosci.pojemnosc_autobus:  # jesli pierwszy niepusty autobus jest pelny
                ilosc_pasazerow = 0
                autobus_do_odwiedzenia = iterator - 1
            else:
                ilosc_pasazerow = autobus
                autobus_do_odwiedzenia = iterator
            autobus_do_oproznienia = iterator  # sprawdzamy, z ktorego autobusu nalezy usunac pasazera
            break  # usuwamy tylko jednego pasazera z tylko najmniej zapelnionego (niepustego) busa

        if autobus_do_odwiedzenia == -1:
            zadowolenie_gracza.append((funkcje.zadowolenieSamochod(n + i + 1),wartosci.INT_MIN))
        else:
            zadowolenie_gracza.append((funkcje.zadowolenieSamochod(n+i+1),
                                   funkcje.zadowolenieAutobus(n+i, ilosc_pasazerow)))

        # przypisywanie wartosci zadowolenia populusu
        if not i == ostatnia_iteracja:
            laczne_zadowolenie_autobusow = 0
            for iterator, autobus in enumerate(flota_autobusow):
                if not autobus:
                    continue
                # zadowolenie autobusa_do_odwiedzenia mozna obliczyc dopiero przy decyzji wylosowanego gracza
                if not iterator == autobus_do_odwiedzenia:
                    laczne_zadowolenie_autobusow += autobus * funkcje.zadowolenieAutobus(n + i, autobus-1)

            zadowolenie_populusu.append((laczne_zadowolenie_autobusow + (flota_autobusow[autobus_do_odwiedzenia] * funkcje.zadowolenieAutobus(n + i + 1, flota_autobusow[autobus_do_odwiedzenia]-1)) + (n+i+1) * funkcje.zadowolenieSamochod(n+i+1),
                                         laczne_zadowolenie_autobusow + ((flota_autobusow[autobus_do_odwiedzenia]+1) * funkcje.zadowolenieAutobus(n + i, flota_autobusow[autobus_do_odwiedzenia])) + (n+i) * funkcje.zadowolenieSamochod(n+i)))

        flota_autobusow[autobus_do_oproznienia] -= 1  # odjecie pasazera do nastepnej strategii
    # zadowolenie populusu dla ostatniej strategii - tylko wylosowany gracz wchodzi do autobusu
    zadowolenie_populusu.append((wartosci.liczba_uczestnikow * zadowolenie_gracza[-1][0],
                                 (wartosci.liczba_uczestnikow - 1) * zadowolenie_gracza[-2][0] + zadowolenie_gracza[-1][1]))


    print("Zadowolenie gracza i populusu w zaleznosci od sytuacji na drodze (strategii kolumny):")
    for i, s in enumerate(zadowolenie_gracza):
        print(f"{i+1}: ({round(s[0], 3)}, {round(s[1], 3)})\t({round(zadowolenie_populusu[i][0], 3)})({round(zadowolenie_populusu[i][1], 3)})")


    # tworzenie macierzy wyplat
    macierz_wyplat = [[], [], []]
    for i, s in enumerate(zadowolenie_gracza):
        macierz_wyplat[0].append((float(s[0]), float(zadowolenie_populusu[i][0])))
        macierz_wyplat[1].append((float(s[1]), float(zadowolenie_populusu[i][1])))
        macierz_wyplat[2].append(i+1)

    # usuwanie strategii zdominowanych
    maks_index = len(macierz_wyplat[0])
    i = 0
    while i < maks_index:
        j = i + 1
        while j < maks_index:
            if (macierz_wyplat[0][i][0] >= macierz_wyplat[0][j][0] and macierz_wyplat[0][i][1] >= macierz_wyplat[0][j][1]) and (macierz_wyplat[1][i][0] >= macierz_wyplat[1][j][0] and macierz_wyplat[1][i][1] >= macierz_wyplat[1][j][1]):
                del(macierz_wyplat[0][j])
                del(macierz_wyplat[1][j])
                del(macierz_wyplat[2][j])
                j -= 1
                maks_index -= 1
            elif (macierz_wyplat[0][i][0] <= macierz_wyplat[0][j][0] and macierz_wyplat[0][i][1] <= macierz_wyplat[0][j][1]) and (macierz_wyplat[1][i][0] <= macierz_wyplat[1][j][0] and macierz_wyplat[1][i][1] <= macierz_wyplat[1][j][1]):
                del (macierz_wyplat[0][i])
                del (macierz_wyplat[1][i])
                del (macierz_wyplat[2][i])
                maks_index -= 1
                j -= 1
            j += 1
        i += 1

    #zaokraglona macierz dla czytelnosci wynikow
    zaokraglona_macierz = [[(round(wyplata[0], 3), round(wyplata[1], 3)) for wyplata in macierz_wyplat[0]],
                           [(round(wyplata[0], 3), round(wyplata[1], 3)) for wyplata in macierz_wyplat[1]]]

    print("\nMacierz wyplat po redukcji zdominowanych strategii kolumny")
    print("Pierwszy wiersz przedstawia numery strategii kolumny z poczatkowej macierzy wyplat")
    print(macierz_wyplat[2])
    for wiersz in zaokraglona_macierz:
        print(wiersz)

    # obliczenie stosunkow zadowolen uzytkownikow samochodow do zadowolen populusu
    stosunki_zadowolen = []
    for indeks, wyplata in enumerate(macierz_wyplat[0]):
        stosunki_zadowolen.append(abs((wyplata[0] * (macierz_wyplat[2][indeks]-1 + n)) / (abs(wyplata[1]) + abs(wyplata[0])*(macierz_wyplat[2][indeks]-1))))
    stosunki_zadowolen = [round(stosunek, 3) for stosunek in stosunki_zadowolen]
    print("\nWartosci stosunkow zadowolen uzytkownikow samochodow do zadowolen populusu")
    print(stosunki_zadowolen)

    print("\nindeks: wyplata -- stosunek")
    for i in range(len(stosunki_zadowolen)):
        print(f"{macierz_wyplat[2][i]}:\t{zaokraglona_macierz[0][i]}\t--\t{stosunki_zadowolen[i]}")

    # indeksy
    najwyzsze_zadowolenie_ogolu = macierz_wyplat[0].index(max(macierz_wyplat[0], key=lambda x: x[1]))
    lista_najwyzszych = []
    for wyplata in macierz_wyplat[0]:
        if wyplata[1] == macierz_wyplat[0][najwyzsze_zadowolenie_ogolu][1]:
            lista_najwyzszych.append(macierz_wyplat[0].index(wyplata))
    max_zadowolenie_min_stosunek = stosunki_zadowolen.index(min([stosunki_zadowolen[x] for x in lista_najwyzszych]))
    print(f"\nOptymalna strategia jest strategia numer: {macierz_wyplat[2][max_zadowolenie_min_stosunek]}.")