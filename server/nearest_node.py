from scipy.spatial import KDTree
from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "EPSG:2180", always_xy=True)

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
    nowe_x, nowe_y = transformer.transform(x_klik, y_klik)

    punkt_wybrany = (nowe_x, nowe_y)
    dystans, indeks = drzewo.query(punkt_wybrany)
    oryginalne_id = indeks_wierzcholka[indeks]

    return oryginalne_id, dystans