from fastapi import FastAPI, Response
from graph import Graph
import pickle, shapely, geopandas, pandas
from nearest_node import indeks_przestrzenny, najblizszy_wierzcholek
print("loading...")
app = FastAPI()
with open('lista_sasiedztwa.pickle', 'rb') as f:
    lista_sasiedztwa = pickle.load(f)
with open('wierzcholki.pickle', 'rb') as f:
    wierzcholki = pickle.load(f)
drzewo, indeks_wierzcholka = indeks_przestrzenny(wierzcholki)
g = Graph(wierzcholki, lista_sasiedztwa)
roadnetwork = pandas.read_pickle('drogi.pickle')
print("loaded")
bins = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100, 5400, 5700, 6000, 6300, 6600, 6900, 7200]
@app.get("/djikstratarget/{start_y}/{start_x}/{target_y}/{target_x}")
def djikstratarget(start_y, start_x, target_y, target_x):
    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_y), float(start_x))
    target, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(target_y), float(target_x))
    d, p, l, e = g.djikstra(start, target)
    if d <= 0 or p is None:
        return Response(status_code=204)
    s = geopandas.GeoDataFrame({"cost": [d], "distance": [l], 'geometry': shapely.unary_union([roadnetwork[edge] for edge in e])}, crs="EPSG:2180")
    return Response(content=s.to_json(), media_type="application/json")
@app.get("/a_star/{start_y}/{start_x}/{target_y}/{target_x}")
def a_star(start_y, start_x, target_y, target_x):
    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_y), float(start_x))
    target, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(target_y), float(target_x))
    p, d, l = g.a_star(start, target, True)
    if d <= 0 or p is None:
        return Response(status_code=204)
    s = geopandas.GeoDataFrame({"cost": [d], "distance": [l], 'geometry': shapely.unary_union([roadnetwork[edge] for edge in e])}, crs="EPSG:2180")
    return Response(content=s.to_json(), media_type="application/json")
@ app.get("/djikstrarange/{start_y}/{start_x}/{max_cost}/{buffer}/{step}/{simplified}")
def djikstrarange(start_y, start_x, max_cost, buffer, step, simplified):
    maxbuffer = int(buffer)
    step = int(step)
    start, _ = najblizszy_wierzcholek(drzewo, indeks_wierzcholka, float(start_y), float(start_x))
    d, p, e = g.djikstra(start, None, float(max_cost))
    geom = []
    try:
        if simplified == 'false':
            for i, path in enumerate(p):
                if path is not None and len(path) > 1:
                    cost = d[i]
                    buffer = max(0, maxbuffer - (step * (cost // 300)))
                    line = shapely.LineString([wierzcholki[node][:2] for node in path])
                    simplified_line = line.simplify(tolerance=5)
                    geom.append({'cost': cost, 'geometry': simplified_line.buffer(buffer)})
        else:
            for i, path in enumerate(p):
                if path is not None and len(path) > 1:
                    cost = d[i]
                    buffer = max(0, maxbuffer - (step * (cost // 300)))
                    geom.append({'cost': cost, 'geometry': shapely.LineString([wierzcholki[node][:2] for node in path]).buffer(buffer)})
    except Exception:
        return Response(status_code=204)
    s = geopandas.GeoDataFrame(geom, crs="EPSG:2180")
    s['grupy'] = pandas.cut(s['cost'], bins=bins).astype(str)
    s = s.dissolve(by='grupy', aggfunc={'cost': 'max'})
    return Response(content=s.to_json(), media_type="application/json")
