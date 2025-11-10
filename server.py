from fastapi import FastAPI
from graph import Graph

app = FastAPI()

from wierzcholki_drog import przetworz_plik
wierzcholki, krawedzie = przetworz_plik('cut_torun.shp')
g = Graph(wierzcholki, krawedzie)

@app.get("/djikstratarget/{start}/{target}")
def djikstratarget(start, target):

    d, p, e = g.djikstra(int(start), int(target))

    return {'edges': e}

@app.get("/a_star/{start}/{target}")
def djikstratarget(start, target):

    p, d = g.a_star(int(start), int(target), True)
    return {'path': p}


@app.get("/djikstra/{start}")
def djikstratarget(start):

    d, p, e = g.djikstra(int(start))

    return {'edges': e}