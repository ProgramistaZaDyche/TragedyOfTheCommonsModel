# folder z wykorzystywanymi funkcjami
import wartosci


def przepelnienieDrogi(liczba_samochodow):
    autobusy = wartosci.liczba_autobusow * wartosci.autobus_samochod
    przepelnienie_drogi = (liczba_samochodow + autobusy) - wartosci.przepustowosc
    if przepelnienie_drogi < 0:
        przepelnienie_drogi = 0
    return przepelnienie_drogi


def zadowolenieAutobus(liczba_samochodow, liczba_wspolpasazerow):
    przepelnienie_drogi = przepelnienieDrogi(liczba_samochodow)

    wplyw_wspolpasazerow = liczba_wspolpasazerow * wartosci.zadowolenie_wspolpasazerowie
    wplyw_czas = przepelnienie_drogi * wartosci.zmiana_czasu * wartosci.zadowolenie_czas
    return wartosci.zadowolenie_autobus - wplyw_czas - wplyw_wspolpasazerow


def zadowolenieSamochod(liczba_samochodow):
    przepelnienie_drogi = przepelnienieDrogi(liczba_samochodow)

    wplyw_czas = przepelnienie_drogi * wartosci.zmiana_czasu * wartosci.zadowolenie_czas
    return wartosci.zadowolenie_samochod - wplyw_czas
