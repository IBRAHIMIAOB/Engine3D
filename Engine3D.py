from painter2D import Painter2D 
from mathCam import MathCam
from Scene import Scene


class Engine3D:
    """
    3D Engine that integrates the painter, camera, and scene to render 3D objects onto a 2D canvas.

    Attributes:
      painter (Painter2D): The 2D drawing interface.
      cam (MathCam): The camera used for projection.
      scene (Scene): The scene containing 3D assets.
    """
    def __init__(self, resolution: int , FPS :int = 60 ,Angel = 90 , x= -10 , y=0 , z =0 , Distance = 5 ) -> None:
        """
        Initialize the 3D engine.

        Parameters:
          resolution (int): The resolution for the Painter2D canvas.
        """
        self.painter: Painter2D = Painter2D(resolution , FPS=FPS)
        self.cam: MathCam = MathCam(x, y, z, Distance , max_value=resolution , Angle=Angel )
        self.scene: Scene = Scene()