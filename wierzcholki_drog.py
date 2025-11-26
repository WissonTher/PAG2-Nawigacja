import arcpy
import numpy as np
import time
from scipy.spatial import KDTree
import pickle

start = time.perf_counter()
arcpy.env.workspace = r"./test"
file = 'warmia_skjz.shp'

def indeks_przestrzenny(wierzcholki):
    wspolrzedne_lista = []
    indeks_wierzcholka = []

    for id_wierzcholka, dane in wierzcholki.items():
        x, y, _ = dane
        wspolrzedne_lista.append((x,y))
        indeks_wierzcholka.append(id_wierzcholka)

    drzewo = KDTree(wspolrzedne_lista)

    return drzewo, indeks_wierzcholka

def najblizszy_wierzcholek(drzewo, indeks_wierzcholka, x_klik, y_klik):
    uklad_zrodlowy = arcpy.SpatialReference(4326)
    uklad_docelowy = arcpy.SpatialReference(2180)
    punkt = arcpy.Point(x_klik, y_klik)

    geom = arcpy.PointGeometry(punkt, uklad_zrodlowy)
    geom_proj = geom.projectAs(uklad_docelowy)

    nowe_x = geom_proj.firstPoint.X
    nowe_y = geom_proj.firstPoint.Y

    punkt_wybrany = (nowe_x, nowe_y)
    dystans, indeks = drzewo.query(punkt_wybrany)
    oryginalne_id = indeks_wierzcholka[indeks]

    return oryginalne_id, dystans
def przetworz_plik(shapefile):
    cursor = arcpy.SearchCursor(shapefile)
    wierzcholki = {}
    lista_sasiedztwa = {}
    #0 - główna, 1 - lokalna, 2 - zbiorcza, 3 - wewnętrzna, 4 - dojazdowa
    predkosci = {0: 100, 1: 60, 2: 80, 3: 30, 4: 40}

    def znajdz_lub_dodaj(wierzcholki, cache, x, y, kod, prec = 4):
        wspolrzedne = (round(x, prec), round(y, prec))
        if wspolrzedne in cache:
            return cache[wspolrzedne]
        nowe_id = len(wierzcholki)
        wierzcholki[nowe_id] = (x, y, kod)
        cache[wspolrzedne] = nowe_id
        return nowe_id

    cache_xy = {}
    for row in cursor:
        p1 = [row.Shape.firstPoint.X, row.Shape.firstPoint.Y]
        p2 = [row.Shape.lastPoint.X, row.Shape.lastPoint.Y]
        kod = row.LOKALNYID
        klasa_drogi = row.KLASA_DROG

        id1 = znajdz_lub_dodaj(wierzcholki, cache_xy, p1[0], p1[1], kod)
        id2 = znajdz_lub_dodaj(wierzcholki, cache_xy, p2[0], p2[1], kod)

        wektor = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        dlugosc = np.linalg.norm(wektor)

        predkosc_kmh = predkosci.get(klasa_drogi, 20)
        predkosc_mps = predkosc_kmh/3.6

        czas_s = dlugosc/predkosc_mps

        lista_sasiedztwa.setdefault(id1, []).append([id2, dlugosc, czas_s])
        lista_sasiedztwa.setdefault(id2, []).append([id1, dlugosc, czas_s])

    return wierzcholki, lista_sasiedztwa

wierzcholki, lista_sasiedztwa = przetworz_plik(file)

with open('lista_sasiedztwa.pickle', 'wb') as f:
    pickle.dump(lista_sasiedztwa, f)

with open('wierzcholki.pickle', 'wb') as f:
    pickle.dump(wierzcholki, f)

