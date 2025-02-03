from typing import Dict , Tuple ,List , Optional , Callable
from assets import Object3D
import numpy as np
from assets import create_cube  , create_pyramid , create_sphere
from assets import Object3D ,Triangle


class Scene:
    """
    Represents a scene containing multiple 3D objects.

    Attributes:
      assetSet (Dict[str, Object3D]): Dictionary mapping asset names to Object3D instances.
    """
    def __init__(self) -> None:
        """
        Initialize an empty Scene.
        """
        self.assetSet: Dict[str, Object3D] = {}
        
    

    def add_object(self, name: str, obj: Object3D) -> None:
        """
        Add a 3D object to the scene.

        Parameters:
          name (str): Identifier for the asset.
          obj (Object3D): The 3D object to add.
          """
        
        self.assetSet[name] = obj
        
        
    def add_cube(self, name: str, x: float, y: float, z: float, size: float = 1) -> None:
        """
        Create and add a cube to the scene.

        Parameters:
          name (str): Identifier for the cube.
          x (float): X coordinate of the cube's position.
          y (float): Y coordinate of the cube's position.
          z (float): Z coordinate of the cube's position.
          size (float, optional): Length of the cube's edge. Default is 1.
        """
        cube :Object3D  =  create_cube(x, y, z, size)
        self.add_object(name, cube)

    def add_pyramid(self, name: str, x: float, y: float, z: float, size: float = 1) -> None:
        """
        Create and add a pyramid to the scene.

        Parameters:
          name (str): Identifier for the pyramid.
          x (float): X coordinate of the pyramid's position.
          y (float): Y coordinate of the pyramid's position.
          z (float): Z coordinate of the pyramid's position.
          size (float, optional): Size parameter for the base. Default is 1.
        """
        pyramid :Object3D  = create_pyramid(x, y, z, size)
        self.add_object(name, pyramid)

    def add_sphere(self, name: str, x: float, y: float, z: float, radius: float = 1, resolution: int = 10) -> None:
        """
        Create and add a sphere to the scene.

        Parameters:
          name (str): Identifier for the sphere.
          x (float): X coordinate of the sphere's center.
          y (float): Y coordinate of the sphere's center.
          z (float): Z coordinate of the sphere's center.
          radius (float, optional): Radius of the sphere. Default is 1.
          resolution (int, optional): Number of segments for approximation. Default is 10.
        """
        sphere:Object3D = create_sphere(x, y, z, radius, resolution)
        self.add_object(name, sphere)
    def add_file(self, name :str , filename: str, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """
        Parses a file containing 3D triangle data and returns an Object3D instance.

        The file is expected to contain lines of vertex coordinates. Each triangle is defined by three consecutive
        lines, each containing three floating-point numbers representing a vertex in 3D space.

        Parameters:
          filename (str): The path to the file containing the 3D triangle data.
          x (float): X coordinate of the object's position. Default is 0.0.
          y (float): Y coordinate of the object's position. Default is 0.0.
          z (float): Z coordinate of the object's position. Default is 0.0.

        Returns:
          Object3D: An instance of Object3D containing the parsed triangles.
        """
        obj = Object3D(x, y, z)
        
        with open(filename , "r") as file :
          points = file.readlines()
          triList = []
          for point in points :
            if point == '\n':
              continue
            else :
              x, y , z = tuple(point.replace("\n" , "").split())
              x, y , z = float(x) , float(y) , float(z)
              triList.append((x, y , z))
              if len(triList) == 3 :
                tri = Triangle(triList[0] ,triList[1] , triList[2])
                obj.addTriangle(tri)
                triList = []
        self.add_object(name , obj)
              

        
    def returnTriangles(self) -> List[Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Aggregate triangles from all objects in the scene.

        Returns:
          list: A list of triangles from all scene assets.
        """
        pointsToRender: List[Tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for obj in self.assetSet.values():
            pointsToRender.extend(obj.returnTriangles())
        return pointsToRender
    