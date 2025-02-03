import math 
import numpy as np 
from typing import List , Tuple ,Optional
class MathCam:
    """
    Mathematical camera that projects 3D points onto a 2D plane.

    Attributes:
      CenterPoint (np.ndarray): The 3D position of the camera.
      Distance (float): The distance from the camera to the view plane.
      Angle (float): The half-angle of the camera's field of view in radians.
      max_value (int): The maximum coordinate value for the projection.
      p1 (np.ndarray): First corner point of the view plane.
      p2 (np.ndarray): Second corner point of the view plane.
      p3 (np.ndarray): Third corner point of the view plane.
      p4 (np.ndarray): Fourth corner point of the view plane.
    """
    def __init__(self, x: float, y: float, z: float, Distance: float, Angle: float = 90, max_value: int = 500) -> None:
        """
        Initialize the MathCam object.

        Parameters:
          x (float): X coordinate of the camera's position.
          y (float): Y coordinate of the camera's position.
          z (float): Z coordinate of the camera's position.
          Distance (float): Distance from the camera to the view plane.
          Angle (float, optional): Full field of view angle in degrees. Default is 90.
          max_value (int, optional): Maximum projection coordinate value. Default is 500.
        """
        self.CenterPoint: np.ndarray = np.array([x, y, z])
        self.Distance: float = Distance
        self.Angle: float = math.radians(Angle) / 2
        self.max_value: int = max_value
        self.p1: np.ndarray = np.array([x + Distance, y + math.tan(self.Angle) * Distance, z + math.tan(self.Angle) * Distance])
        self.p2: np.ndarray = np.array([x + Distance, y + math.tan(self.Angle) * Distance, z - math.tan(self.Angle) * Distance])
        self.p3: np.ndarray = np.array([x + Distance, y - math.tan(self.Angle) * Distance, z + math.tan(self.Angle) * Distance])
        self.p4: np.ndarray = np.array([x + Distance, y - math.tan(self.Angle) * Distance, z - math.tan(self.Angle) * Distance])

    @staticmethod
    def normalize(v: np.ndarray) -> np.ndarray:
        """
        Normalize a vector.

        Parameters:
          v (np.ndarray): The vector to normalize.

        Returns:
          np.ndarray: The normalized vector.
        """
        norm: float = np.linalg.norm(v)
        return v if norm == 0 else v / norm

    def line_plane_intersection(self, P1: np.ndarray) -> Tuple[Optional[float], Optional[float]]:
        """
        Compute the intersection of a line (from camera center to point P1) with the view plane.

        Parameters:
          P1 (np.ndarray): A point in 3D space.

        Returns:
          tuple: A tuple (rel_x, rel_y) of 2D projection coordinates if intersection occurs;
                 (None, None) if there is no valid intersection.
        """
        P1, P2 = self.CenterPoint, np.array(P1)
        u: np.ndarray = self.p2 - self.p1
        v: np.ndarray = self.p3 - self.p1
        n: np.ndarray = np.cross(u, v)
        if np.linalg.norm(n) == 0:
            return (None, None)
        n = MathCam.normalize(n)
        d: float = np.dot(n, self.p1)
        denom: float = np.dot(n, P2 - P1)
        if np.isclose(denom, 0):
            return (None, None)
        t: float = (d - np.dot(n, P1)) / denom
        return (None, None) if t < 0 or t > 1 else self.relative_2D(P1 + t * (P2 - P1))

    def relative_2D(self, P: np.ndarray) -> Tuple[float, float]:
        """
        Convert a 3D point to relative 2D coordinates on the view plane.

        Parameters:
          P (np.ndarray): A 3D point.

        Returns:
          tuple: A tuple (rel_x, rel_y) representing 2D coordinates scaled to max_value.
        """
        P = np.array(P)
        u: np.ndarray = MathCam.normalize(self.p2 - self.p1)
        v: np.ndarray = MathCam.normalize(self.p3 - self.p1)
        rel_x: float = np.dot(P - self.p1, u)
        rel_y: float = np.dot(P - self.p1, v)
        max_x: float = np.dot(self.p2 - self.p1, u)
        max_y: float = np.dot(self.p3 - self.p1, v)
        rel_x = (rel_x / max_x) * self.max_value if max_x != 0 else 0
        rel_y = (rel_y / max_y) * self.max_value if max_y != 0 else 0
        return rel_x, rel_y