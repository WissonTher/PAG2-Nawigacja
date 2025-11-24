from fastapi import FastAPI, Response
from graph import Graph
import pickle, shapely, geopandas
from nearest_node import indeks_przestrzenny, najblizszy_wierzcholek

app = FastAPI()
print("loading...")
with open('lista_sasiedztwa.pickle', 'rb') as f:
    lista_sasiedztwa = pickle.load(f)
with open('wierzcholki.pickle', 'rb') as f:
    wierzcholki = pickle.load(f)
drzewo, indeks_wierzcholka = indeks_przestrzenny(wierzcholki)
g = Graph(wierzcholki, lista_sasiedztwa)
print("loaded")
@app.get("/djikstratarget/{start_y}/{start_x}/{target_y}/{target_x}")
def djikstratarget(start_y, start_x, target_y, target_x):

    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_y), float(start_x))
    target, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(target_y), float(target_x))
    d, p, e = g.djikstra(start, target)

    s = geopandas.GeoDataFrame({"cost": [d]}, geometry=[shapely.LineString([wierzcholki[node][:2] for node in p])], crs="EPSG:2180")
    return Response(content=s.to_json(), media_type="application/json")

@app.get("/a_star/{start_y}/{start_x}/{target_y}/{target_x}")
def a_star(start_y, start_x, target_y, target_x):

    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_y), float(start_x))
    target, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(target_y), float(target_x))
    p, d = g.a_star(start, target, True)

    s = geopandas.GeoDataFrame({"cost": [d]}, geometry=[shapely.LineString([wierzcholki[node][:2] for node in p])], crs="EPSG:2180")
    return Response(content=s.to_json(), media_type="application/json")

@app.get("/djikstrarange/{start_y}/{start_x}/{max_cost}")
def djikstrarange(start_y, start_x, max_cost):

    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_y), float(start_x))
    d, p, e = g.djikstra(start, None, float(max_cost))
    s = geopandas.GeoDataFrame({'cost': d, 'geometry': [shapely.buffer(shapely.LineString([wierzcholki[node][:2] for node in path]), 10) for path in p if path is not None and len(path) > 1]}, crs="EPSG:2180")
    return Response(content=s.to_json(), media_type="application/json")