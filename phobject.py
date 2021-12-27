# Define basic classes for handling things that should be added to Blender.
import mathutils
import .constants
import .generate_text

class Phobject:
    """Class to handle general Blender object.
    Most of this will probably be a wrapper to real Blender's object class.
    """

    def __init__(self):
        pass

    def add_to_Blender(self):
        """Implemented by the specific class."""
        pass

class Text(Phobject): 
    """LaTeX text object. 
    """
    def __init__(self, 
                 position = mathutils.Vector((0,0,0))
                 anchor = "MC"
                 text = "Text",
                 )

        self.text = text
        super().__init__(self)
        generate_text(text) 




class Square:
    """Square with rounded corners.
    """
    def __init__(self, x, y, rx=0, ry=0, color=None, fillcolor=None, rotation=None):
        pass
