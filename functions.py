import arcpy

# Read data
arcpy.env.workspace = './test/cut_torun.shp'
cursor = arcpy.SearchCursor('cut_torun', 'FID < 10')
for row in cursor:
    #print(row.FID, row.Shape.firstPoint.X, row.Shape.firstPoint.Y)
    print(row.FID, row.Shape)