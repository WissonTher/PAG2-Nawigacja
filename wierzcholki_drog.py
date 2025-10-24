import arcpy
import numpy as np

arcpy.env.workspace = r"./torun_cut"

def przetworz_plik(shapefile):
    cursor = arcpy.SearchCursor('cut_torun.shp')
    wierzcholki = {}
    krawedzie = {}

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
        kod = row.x_kod

        id1 = znajdz_lub_dodaj(wierzcholki, cache_xy, p1[0], p1[1], kod)
        id2 = znajdz_lub_dodaj(wierzcholki, cache_xy, p2[0], p2[1], kod)

        wektor = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        dlugosc = np.linalg.norm(wektor)
        krawedzie[row.FID] = [id1, id2, dlugosc]

    return wierzcholki, krawedzie

wierzcholki, krawedzie = przetworz_plik('./torun_cut.shp')

print(wierzcholki)
print(krawedzie)

