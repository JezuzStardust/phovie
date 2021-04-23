import bpy
import math
import numpy as np


def get_grease_pencil(gpencil_obj_name="Grease Pencil"):
    """
    Return the grease-pencil object with the given name.
    Initialize one if not already present.
    :param gpencil_obj_name: name/key of the grease pencil object in the scene
    """

    # If not present already, create grease pencil object
    if gpencil_obj_name not in bpy.context.scene.objects:
        bpy.ops.object.gpencil_add(location=(0, 0, 0), type="EMPTY")
        # rename grease pencil
        bpy.context.scene.objects[-1].name = gpencil_obj_name

    # Get grease pencil object
    gpencil = bpy.context.scene.objects[gpencil_obj_name]

    return gpencil


def get_grease_pencil_layer(gpencil, gpencil_layer_name="GP_Layer", clear_layer=False):
    """
    Return the grease-pencil layer with the given name.
    Create one if not already present.

    Paramters:
        gpencil: grease-pencil object for the layer
        gpencil_layer_name: name of the greace pencil layer
        clear_layer: if the layer should be cleared or not
    """

    # Get grease pencil layer or create one if none exists
    if gpencil.data.layers and gpencil_layer_name in gpencil.data.layers:
        gpencil_layer = gpencil.data.layers[gpencil_layer_name]
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)

    if clear_layer:
        gpencil_layer.clear()  # clear all previous layer data

    # bpy.ops.gpencil.paintmode_toggle()  # need to trigger otherwise there is no frame

    return gpencil_layer


# Util for default behavior merging previous two methods
def init_grease_pencil(
    gpencil_obj_name="GPencil", gpencil_layer_name="GP_Layer", clear_layer=True
):
    gpencil = get_grease_pencil(gpencil_obj_name)
    gpencil_layer = get_grease_pencil_layer(
        gpencil, gpencil_layer_name, clear_layer=clear_layer
    )
    return gpencil_layer


# Default primitives: line, longitudal_circle, latitudal_circle
# These should probably be classes right?
# These classes can wrap convenience methods for changing materials etc.
# Perhaps I am redoing a lot of work that already exists in Blender....
def draw_line(gp_frame, p0: tuple, p1: tuple):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = "3DSPACE"  # allows for editing

    # Define stroke geometry
    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = p0
    gp_stroke.points[1].co = p1
    return gp_stroke


def draw_circle(gp_frame, center, radius, num_segments):
    # Init new stroke
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = "3DSPACE"  # allows for editing
    gp_stroke.draw_cyclic = True  # closes the stroke

    # Define stroke geometry
    angle = 2 * math.pi / num_segments  # angle in radians
    gp_stroke.points.add(count=num_segments + 1)
    for i in range(num_segments + 1):
        x = center[0] + radius * math.cos(angle * i)
        y = center[1] + radius * math.sin(angle * i)
        z = center[2]
        gp_stroke.points[i].co = (x, y, z)

    return gp_stroke


def rotate_stroke(stroke, angle, axis="z"):
    # Define rotation matrix based on axis
    if axis.lower() == "x":
        transform_matrix = np.array(
            [
                [1, 0, 0],
                [0, math.cos(angle), -math.sin(angle)],
                [0, math.sin(angle), math.cos(angle)],
            ]
        )
    elif axis.lower() == "y":
        transform_matrix = np.array(
            [
                [math.cos(angle), 0, -math.sin(angle)],
                [0, 1, 0],
                [math.sin(angle), 0, math.cos(angle)],
            ]
        )
    # default on z
    else:
        transform_matrix = np.array(
            [
                [math.cos(angle), -math.sin(angle), 0],
                [math.sin(angle), math.cos(angle), 0],
                [0, 0, 1],
            ]
        )

    # Apply rotation matrix to each point
    for i, p in enumerate(stroke.points):
        p.co = transform_matrix @ np.array(p.co).reshape(3, 1)


def draw_sphere(gp_frame, radius, num_segments=64, num_circles=12):
    angle = math.pi / num_circles
    for i in range(num_circles):
        circle = draw_circle(gp_frame, (0, 0, 0), radius, num_segments)
        rotate_stroke(circle, angle * i, "x")


# gp_layer = init_grease_pencil(clear_layer=True)
# gp_frame = gp_layer.frames.new(0)
# draw_line(gp_frame, (0, 0, 0), (1, 1, 0))
# draw_sphere(gp_frame, 1.1)
