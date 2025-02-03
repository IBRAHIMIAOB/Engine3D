import numpy as np
import math
from typing import List, Tuple, Optional, Dict, Any

class Triangle:
    """
    Represents a triangle in 3D space defined by three points.

    Attributes:
      p1 (np.ndarray): First vertex of the triangle.
      p2 (np.ndarray): Second vertex of the triangle.
      p3 (np.ndarray): Third vertex of the triangle.
    """
    def __init__(self, p1: Tuple[float, float, float], p2: Tuple[float, float, float], p3: Tuple[float, float, float]) -> None:
        """
        Initialize the Triangle object.

        Parameters:
          p1 (tuple): The first vertex of the triangle.
          p2 (tuple): The second vertex of the triangle.
          p3 (tuple): The third vertex of the triangle.
        """
        self.p1: np.ndarray = np.array(p1)
        self.p2: np.ndarray = np.array(p2)
        self.p3: np.ndarray = np.array(p3)


class Object3D:
    """
    Represents a 3D object composed of triangles and a position.

    Attributes:
      Object_position (np.ndarray): The pivot position of the object.
      TriangleSet (List[Triangle]): A list of Triangle objects relative to the pivot.
    """
    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Initialize the Object3D.

        Parameters:
          x (float): X coordinate of the object's position.
          y (float): Y coordinate of the object's position.
          z (float): Z coordinate of the object's position.
        """
        self.Object_position: np.ndarray = np.array((x, y, z))
        self.TriangleSet: List[Triangle] = []

    def addTriangle(self, triangle: Triangle) -> None:
        """
        Add a triangle to the object's triangle set.

        Parameters:
          triangle (Triangle): The triangle to add.
        """
        self.TriangleSet.append(triangle)

    def returnTriangles(self) -> List[Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Get the absolute coordinates of all triangles in the object.

        Returns:
          list: A list of tuples, each containing three np.ndarray points representing a triangle.
        """
        trianglePoints: List[Tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for tri in self.TriangleSet:
            trianglePoints.append((tri.p1 + self.Object_position, 
                                     tri.p2 + self.Object_position, 
                                     tri.p3 + self.Object_position))
        return trianglePoints

    def shift(self, x: float, y: float, z: float) -> None:
        """
        Shift the object's position.

        Parameters:
          x (float): Shift along the x-axis.
          y (float): Shift along the y-axis.
          z (float): Shift along the z-axis.
        """
        shiftValue: np.ndarray = np.array((x, y, z))
        self.Object_position += shiftValue

    def scale(self, factor: float) -> None:
        """
        Scale the object relative to its pivot.

        Parameters:
          factor (float): Scaling factor to apply.
        """
        for tri in self.TriangleSet:
            tri.p1 = self.Object_position + (tri.p1 - self.Object_position) * factor
            tri.p2 = self.Object_position + (tri.p2 - self.Object_position) * factor
            tri.p3 = self.Object_position + (tri.p3 - self.Object_position) * factor

    def rotate(self, axis: str, angle: float) -> None:
        """
        Rotate the object around its pivot.

        Parameters:
          axis (str): Axis to rotate around ('x', 'y', or 'z').
          angle (float): Rotation angle in degrees.

        Raises:
          ValueError: If an invalid axis is provided.
        """
        angle_rad: float = math.radians(angle)
        cos_a: float = math.cos(angle_rad)
        sin_a: float = math.sin(angle_rad)
        if axis == 'x':
            rotation_matrix: np.ndarray = np.array([
                [1, 0, 0],
                [0, cos_a, -sin_a],
                [0, sin_a, cos_a]
            ])
        elif axis == 'y':
            rotation_matrix = np.array([
                [cos_a, 0, sin_a],
                [0, 1, 0],
                [-sin_a, 0, cos_a]
            ])
        elif axis == 'z':
            rotation_matrix = np.array([
                [cos_a, -sin_a, 0],
                [sin_a, cos_a, 0],
                [0, 0, 1]
            ])
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        for tri in self.TriangleSet:
            tri.p1 = np.dot(rotation_matrix, tri.p1 - self.Object_position) + self.Object_position
            tri.p2 = np.dot(rotation_matrix, tri.p2 - self.Object_position) + self.Object_position
            tri.p3 = np.dot(rotation_matrix, tri.p3 - self.Object_position) + self.Object_position


def create_cube(x: float, y: float, z: float, size: float = 1) -> "Object3D":
    """
    Create a cube 3D object composed of triangles.

    Parameters:
      x (float): X coordinate of the cube's position.
      y (float): Y coordinate of the cube's position.
      z (float): Z coordinate of the cube's position.
      size (float, optional): Length of the cube's edge. Default is 1.

    Returns:
      Object3D: A 3D object representing a cube constructed from triangles.
    """
    obj: Object3D = Object3D(x, y, z)
    s: float = size / 2
    vertices: List[Tuple[float, float, float]] = [
        (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),
        (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)
    ]
    faces: List[Tuple[int, int, int]] = [(0, 1, 2), (2, 3, 0), (4, 5, 6), (6, 7, 4),
                                          (0, 1, 5), (5, 4, 0), (2, 3, 7), (7, 6, 2),
                                          (0, 3, 7), (7, 4, 0), (1, 2, 6), (6, 5, 1)]
    for f in faces:
        obj.addTriangle(Triangle(vertices[f[0]], vertices[f[1]], vertices[f[2]]))
    return obj

def create_pyramid(x: float, y: float, z: float, size: float = 1) -> "Object3D":
    """
    Create a pyramid 3D object with a square base and four triangular faces.

    Parameters:
      x (float): X coordinate of the pyramid's position.
      y (float): Y coordinate of the pyramid's position.
      z (float): Z coordinate of the pyramid's position.
      size (float, optional): Size parameter for the base. Default is 1.

    Returns:
      Object3D: A 3D object representing a pyramid constructed from triangles.
    """
    obj: Object3D = Object3D(x, y, z)
    s: float = size / 2
    base: List[Tuple[float, float, float]] = [(-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s)]
    top: Tuple[float, float, float] = (0, 0, s)
    obj.addTriangle(Triangle(base[0], base[1], base[2]))
    obj.addTriangle(Triangle(base[2], base[3], base[0]))
    for i in range(4):
        obj.addTriangle(Triangle(base[i], base[(i+1) % 4], top))
    return obj

def create_sphere(x: float, y: float, z: float, radius: float = 1, resolution: int = 10) -> "Object3D":
    """
    Create a sphere 3D object approximated by triangles.

    Parameters:
      x (float): X coordinate of the sphere's center.
      y (float): Y coordinate of the sphere's center.
      z (float): Z coordinate of the sphere's center.
      radius (float, optional): Radius of the sphere. Default is 1.
      resolution (int, optional): Number of segments for approximation. Default is 10.

    Returns:
      Object3D: A 3D object representing a sphere constructed from triangles.
    """
    obj: Object3D = Object3D(x, y, z)
    for i in range(resolution):
        theta1: float = (i / resolution) * np.pi
        theta2: float = ((i + 1) / resolution) * np.pi
        for j in range(resolution * 2):
            phi1: float = (j / (resolution * 2)) * 2 * np.pi
            phi2: float = ((j + 1) / (resolution * 2)) * 2 * np.pi
            p1: np.ndarray = np.array([radius * np.sin(theta1) * np.cos(phi1),
                                       radius * np.sin(theta1) * np.sin(phi1),
                                       radius * np.cos(theta1)])
            p2: np.ndarray = np.array([radius * np.sin(theta1) * np.cos(phi2),
                                       radius * np.sin(theta1) * np.sin(phi2),
                                       radius * np.cos(theta1)])
            p3: np.ndarray = np.array([radius * np.sin(theta2) * np.cos(phi1),
                                       radius * np.sin(theta2) * np.sin(phi1),
                                       radius * np.cos(theta2)])
            p4: np.ndarray = np.array([radius * np.sin(theta2) * np.cos(phi2),
                                       radius * np.sin(theta2) * np.sin(phi2),
                                       radius * np.cos(theta2)])
            obj.addTriangle(Triangle(p1, p2, p3))
            obj.addTriangle(Triangle(p2, p3, p4))
    return obj
    