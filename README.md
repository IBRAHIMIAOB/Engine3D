# 3D Engine Project

This project is a simple 3D rendering engine implemented in Python. It allows you to create and manipulate 3D objects, project them onto a 2D plane, and render them using a 2D painter. The engine supports basic 3D objects like cubes, pyramids, and spheres, as well as custom objects loaded from files.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Examples](#examples)

## Introduction

The 3D Engine project is designed to provide a basic framework for rendering 3D objects in a 2D space. It includes modules for handling 3D objects, camera projection, and 2D rendering. The engine is built using Python and leverages libraries like NumPy and Matplotlib for mathematical operations and rendering.

## Features

- **3D Object Creation**: Create basic 3D objects like cubes, pyramids, and spheres.
- **Custom Object Loading**: Load custom 3D objects from files.
- **Camera Projection**: Project 3D points onto a 2D plane using a mathematical camera.
- **2D Rendering**: Render the projected 2D points using a 2D painter.
- **Object Manipulation**: Rotate, scale, and shift 3D objects in the scene.

## Installation

To use this project, you need to have Python installed on your system. You can install the required dependencies using pip:

```bash
pip install numpy matplotlib
```

## Usage

To use the 3D engine, you can start by creating a scene and adding objects to it. Here is an example of how to create a scene with a rotating Utah teapot:

```python
from Engine3D import Engine3D

# Initialize the engine with a resolution of 1000 and a field of view of 45 degrees
Engine: Engine3D = Engine3D(1000, Angel=45)

# Load the Utah teapot object from a file
Engine.scene.add_file("utah_teapot", "utah_teapot.engine3D")

# Rotate the teapot 90 degrees around the x-axis
Engine.scene.assetSet["utah_teapot"].rotate('x', 90)

# Render the scene
with Engine.painter as canvas:
    while True:
        points = Engine.scene.returnTriangles()
        for x, y, z in points:
            x0, y0 = Engine.cam.line_plane_intersection(x)
            x1, y1 = Engine.cam.line_plane_intersection(y)
            x2, y2 = Engine.cam.line_plane_intersection(z)
            if all([x0, y0, x1, y1, x2, y2]):
                Engine.painter.DrawTriangle(x0, y0, x1, y1, x2, y2)
                
        # Rotate the teapot 5 degrees around the z-axis
        Engine.scene.assetSet["utah_teapot"].rotate('z', 5)

        # Update the frame and clear the canvas for the next frame
        Engine.painter.updateFrame()
        Engine.painter.clearFrame()
```

## Code Structure

The project is organized into several modules:

- **main.py**: The main script that initializes the engine and runs the rendering loop.
- **Engine3D.py**: The core engine module that integrates the painter, camera, and scene.
- **assets.py**: Contains classes and functions for creating and manipulating 3D objects.
- **mathCam.py**: Implements the mathematical camera for projecting 3D points onto a 2D plane.
- **painter2D.py**: Provides a 2D painter for rendering the projected points.
- **Scene.py**: Manages the scene and the objects within it.

## Examples

### Creating a Cube

```python
from Engine3D import Engine3D

Engine: Engine3D = Engine3D(1000, Angel=45)

# Add a cube to the scene
Engine.scene.add_cube("my_cube", 0, 0, 0, size=2)

with Engine.painter as canvas:
    while True:
        points = Engine.scene.returnTriangles()
        for x, y, z in points:
            x0, y0 = Engine.cam.line_plane_intersection(x)
            x1, y1 = Engine.cam.line_plane_intersection(y)
            x2, y2 = Engine.cam.line_plane_intersection(z)
            if all([x0, y0, x1, y1, x2, y2]):
                Engine.painter.DrawTriangle(x0, y0, x1, y1, x2, y2)
                
        Engine.scene.assetSet["my_cube"].rotate('z', 5)
        Engine.painter.updateFrame()
        Engine.painter.clearFrame()
```

### Creating a Sphere

```python
from Engine3D import Engine3D

Engine: Engine3D = Engine3D(1000, Angel=45)

# Add a sphere to the scene
Engine.scene.add_sphere("my_sphere", 0, 0, 0, radius=2, resolution=20)

with Engine.painter as canvas:
    while True:
        points = Engine.scene.returnTriangles()
        for x, y, z in points:
            x0, y0 = Engine.cam.line_plane_intersection(x)
            x1, y1 = Engine.cam.line_plane_intersection(y)
            x2, y2 = Engine.cam.line_plane_intersection(z)
            if all([x0, y0, x1, y1, x2, y2]):
                Engine.painter.DrawTriangle(x0, y0, x1, y1, x2, y2)
                
        Engine.scene.assetSet["my_sphere"].rotate('z', 5)
        Engine.painter.updateFrame()
        Engine.painter.clearFrame()
```




Feel free to explore the code and modify it to suit your needs. If you have any questions or suggestions, please open an issue or submit a pull request. Happy coding!
