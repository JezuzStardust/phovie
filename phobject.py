# Define basic classes for handling things that should be added to Blender.


class Phobject:
    """Class to handle general Blender object.
    Most of this will probably be a wrapper to real Blender's object class.
    """

    def __init__(self, bl_data):
        pass

    # Type - E.g. CURVE, MESH, etc.
    # Reference - Name of Blender object within Blender.
    # Position - Coordinate of the object.
    # Rotation - Rotation in e.g. Euler.
    # Origin - Origin position relative to the object. E.g. UL, UR, etc.
