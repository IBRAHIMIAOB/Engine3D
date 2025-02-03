import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple,Any




class Painter2D:
    """
    2D Painter class for drawing on a pixel matrix using matplotlib.

    Attributes:
      W (int): Width (and height) resolution of the drawing canvas.
      H (int): Height resolution of the drawing canvas.
      FPS (int): Frames per second for updating the canvas.
      matrix (np.ndarray): 2D array representing pixel intensities.
      fig (plt.Figure): The matplotlib figure object.
      ax (plt.Axes): The matplotlib axes object.
      img (Any): The image object for displaying the matrix.
    """
    def __init__(self, Resolution: int, FPS: int = 60) -> None:
        """
        Initialize the Painter2D object.

        Parameters:
          Resolution (int): The resolution (width and height) of the canvas.
          FPS (int, optional): Frames per second for canvas update. Default is 60.
        """
        self.W: int = Resolution
        self.H: int = Resolution
        self.FPS: int = FPS
        self.matrix: np.ndarray = np.zeros((Resolution, Resolution))
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(self.matrix, cmap='gray', vmin=0, vmax=255)

    def __enter__(self) -> "Painter2D":
        """
        Enter the runtime context for Painter2D.

        Returns:
          Painter2D: The current instance.
        """
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """
        Exit the runtime context, turning off interactive mode and closing the figure.

        Parameters:
          exc_type: Exception type.
          exc_value: Exception value.
          traceback: Traceback object.
        """
        plt.ioff()
        plt.close(self.fig)

    def DrawLine(self, x0: int, y0: int, x1: int, y1: int, color: int = 255) -> List[Tuple[int, int]]:
        """
        Draw a line on the canvas using Bresenham's algorithm.

        Parameters:
          x0 (int): Starting x coordinate.
          y0 (int): Starting y coordinate.
          x1 (int): Ending x coordinate.
          y1 (int): Ending y coordinate.
          color (int, optional): Color intensity value. Default is 255.

        Returns:
          list: A list of coordinate tuples that were colored.
        """
        X_Y_colored: List[Tuple[int, int]] = []
        dx: int = abs(x1 - x0)
        dy: int = abs(y1 - y0)
        sx: int = 1 if x0 < x1 else -1
        sy: int = 1 if y0 < y1 else -1
        steep: bool = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dx, dy = dy, dx
        p: int = 2 * dy - dx
        y: int = y0
        for x in range(x0, x1 + sx, sx):
            if steep:
                if 0 <= x < self.matrix.shape[1] and 0 <= y < self.matrix.shape[0]:
                    self.matrix[y, x] = color
                    X_Y_colored.append((y, x))
            else:
                if 0 <= x < self.matrix.shape[0] and 0 <= y < self.matrix.shape[1]:
                    self.matrix[x, y] = color
                    X_Y_colored.append((x, y))
            if p >= 0:
                y += sy
                p -= 2 * dx
            p += 2 * dy
        return X_Y_colored

    def DrawTriangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, color: int = 255) -> None:
        """
        Draw a triangle on the canvas by drawing its three edges.

        Parameters:
          x0 (int): X coordinate of the first vertex.
          y0 (int): Y coordinate of the first vertex.
          x1 (int): X coordinate of the second vertex.
          y1 (int): Y coordinate of the second vertex.
          x2 (int): X coordinate of the third vertex.
          y2 (int): Y coordinate of the third vertex.
          color (int, optional): Color intensity value. Default is 255.
        """
        x0, y0, x1, y1, x2, y2 = int(x0), int(y0), int(x1), int(y1), int(x2), int(y2)
        if None in [x0, y0, x1, y1, x2, y2]:
            return
        self.DrawLine(x0, y0, x1, y1, color)
        self.DrawLine(x1, y1, x2, y2, color)
        self.DrawLine(x2, y2, x0, y0, color)

    def updateFrame(self) -> None:
        """
        Update the canvas display with the current matrix data.
        """
        self.img.set_data(self.matrix)
        plt.draw()
        plt.pause(0.5)

    def clearFrame(self) -> None:
        """
        Clear the canvas by resetting the pixel matrix to zeros.
        """
        self.matrix = np.zeros((self.W, self.H))






