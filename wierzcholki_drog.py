import arcpy
import numpy as np

arcpy.env.workspace = r"./torun_cut"
cursor = arcpy.SearchCursor('cut_torun.shp')
wierzcholki = {}
krawedzie = {}
for row in cursor:
    if len(wierzcholki) == 0:
        wierzcholki[0] = (row.Shape.firstPoint.X, row.Shape.firstPoint.Y, row.x_kod)
        wierzcholki[1] = (row.Shape.firstPoint.X, row.Shape.firstPoint.Y, row.x_kod)

        krawedzie[row.FID] = [0, 1, 0]
    else:
        znaleziono = False
        for w in list(wierzcholki):
            nowe_id = len(wierzcholki)
            if (row.Shape.firstPoint.X == wierzcholki[w][0]) and (row.Shape.firstPoint.Y == wierzcholki[w][1]):
                wierzcholki[nowe_id] = (row.Shape.lastPoint.X, row.Shape.lastPoint.Y, row.x_kod)
                krawedzie[row.FID] = [w, nowe_id, 0]
                znaleziono = True
                break
            elif (row.Shape.lastPoint.X == wierzcholki[w][0]) and (row.Shape.lastPoint.Y == wierzcholki[w][1]):
                wierzcholki[nowe_id] = (row.Shape.firstPoint.X, row.Shape.firstPoint.Y, row.x_kod)
                krawedzie[row.FID] = [nowe_id, w, 0]
                znaleziono = True
                break
        if not znaleziono:
            nowe_id = len(wierzcholki)
            wierzcholki[nowe_id] = (row.Shape.firstPoint.X, row.Shape.firstPoint.Y, row.x_kod)
            wierzcholki[nowe_id + 1] = (row.Shape.lastPoint.X, row.Shape.lastPoint.Y, row.x_kod)
            krawedzie[row.FID] = [nowe_id, nowe_id + 1, 0]

    for fid, (id_pocz, id_kon, _) in krawedzie.items():
        p1 = wierzcholki[id_pocz]
        p2 = wierzcholki[id_kon]
        wektor = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        krawedzie[fid][2] = np.linalg.norm(wektor)
print(wierzcholki)
print(krawedzie)

