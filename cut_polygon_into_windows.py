def cut_polygon_into_windows(p, window_height, window_width):

    crs = p.crs().toWkt()
    extent = p.extent()
    (xmin, xmax, ymin, ymax) = (extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum())

    # Create the grid layer
    vector_grid = QgsVectorLayer('Polygon?crs='+ crs, 'vector_grid' , 'memory')
    prov = vector_grid.dataProvider()

    # Create the grid layer
    output = QgsVectorLayer('Polygon?crs='+ crs, 'output' , 'memory')
    outprov = output.dataProvider()

    # Add ids and coordinates fields
    fields = QgsFields()
    fields.append(QgsField('ID', QVariant.Int, '', 10, 0))
    outprov.addAttributes(fields)

    # Generate the features for the vector grid
    id = 0
    y = ymax
    while y >= ymin:
        x = xmin
        while x <= xmax:
            point1 = QgsPointXY(x, y)
            point2 = QgsPoint(x + window_width, y)
            point3 = QgsPointXY(x + window_width, y - window_height)
            point4 = QgsPoint(x, y - window_height)
            vertices = [point1, point2, point3, point4] # Vertices of the polygon for the current id
            inAttr = [id]
            feat = QgsFeature()
            #feat.setGeometry(QgsGeometry().fromPolygon([vertices])) # Set geometry for the current id
            rectangle = QgsRectangle(point1,point3)
            feat.setGeometry(QgsGeometry().fromRect(rectangle)) # Set geometry for the current id
            feat.setAttributes(inAttr) # Set attributes for the current id
            prov.addFeatures([feat])
            x = x + window_width
            id += 1
        y = y - window_height

    index = QgsSpatialIndex() # Spatial index
    for ft in vector_grid.getFeatures():
        index.insertFeature(ft)

    for feat in p.getFeatures():
        geom = feat.geometry()
        idsList = index.intersects(geom.boundingBox())
        for gridfeat in vector_grid.getFeatures(QgsFeatureRequest().setFilterFids(idsList)):
            tmp_geom = QgsGeometry(gridfeat.geometry())
            tmp_attrs = gridfeat.attributes()
            if geom.intersects(tmp_geom):
                int = QgsGeometry(geom.intersection(tmp_geom))
                outfeat = QgsFeature()
                outfeat.setGeometry(int)
                outfeat.setAttributes(tmp_attrs)
                outprov.addFeatures([outfeat])

    output.updateFields()

    return output