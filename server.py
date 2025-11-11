from fastapi import FastAPI
from graph import Graph
app = FastAPI()

from wierzcholki_drog import przetworz_plik, indeks_przestrzenny, najblizszy_wierzcholek
wierzcholki, krawedzie, lista_sasiedztwa = przetworz_plik('warmia_skjz.shp')
drzewo, indeks_wierzcholka = indeks_przestrzenny(wierzcholki)
g = Graph(wierzcholki, krawedzie, lista_sasiedztwa)

@app.get("/djikstratarget/{start_x}/{start_y}/{target_x}/{target_y}")
def djikstratarget(start_x, start_y, target_x, target_y):

    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_x), float(start_y))
    target, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(target_x), float(target_y))
    d, p, e = g.djikstra(start, target)

    return {'cost': d,
        'edges': e}

@app.get("/a_star/{start_x}/{start_y}/{target_x}/{target_y}")
def djikstratarget(start_x, start_y, target_x, target_y):

    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_x), float(start_y))
    target, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(target_x), float(target_y))
    p, d = g.a_star(start, target, True)
    return {'cost': d, 'path': p}


@app.get("/djikstra/{start_x}/{start_y}/{max_cost}")
def djikstratarget(start_x, start_y, max_cost):

    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_x), float(start_y))
    d, p, e = g.djikstra(start, None, float(max_cost))

    return {'costs': d, 'edges': e}