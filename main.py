from Engine3D import Engine3D

Engine: Engine3D = Engine3D(1000 , Angel=45)

Engine.scene.add_file("utah_teapot","utah_teapot.engine3D")
Engine.scene.assetSet["utah_teapot"].rotate('x', 90)


with Engine.painter as canvas:
    while True:
        points = Engine.scene.returnTriangles()
        for x, y, z in points:
            x0, y0 = Engine.cam.line_plane_intersection(x)
            x1, y1 = Engine.cam.line_plane_intersection(y)
            x2, y2 = Engine.cam.line_plane_intersection(z)
            if all([x0, y0, x1, y1, x2, y2]):
                Engine.painter.DrawTriangle(x0, y0, x1, y1, x2, y2)
                
                
        Engine.scene.assetSet["utah_teapot"].rotate('z', 5)

        Engine.painter.updateFrame()
        Engine.painter.clearFrame()
