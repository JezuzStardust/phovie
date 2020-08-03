import bpy
from mathutils import Vector
import math
from importlib import resources, reload
import os
import phovie # Only to get path to background image
from phovie import generate_text
reload(generate_text)

# This should probably just be a set of functions.
# Hmmm... or perhaps each Clip should be a separate 
# scene to render. 
# However, many of the functions are general purpose and 
# can be moved elsewhere. 

class Clip():
    
    def __init__(self,name='Collection'):
        self.clear_collections()
        self.collection = self.make_new_collection(name)
        self.name = self.collection.name
        self.camera = self.make_camera()
        self.set_background()
        # Set lights
        # Set objects
        
        # Set units
        #bpy.context.scene.unit_settings.scale_lengt = 0.01
    
    def clear_collections(self):
        # Delete all the objects in a collection. 
        objs = bpy.data.objects
        for obj in objs:
            objs.remove(obj, do_unlink=True)
        
        # Delete all collections. 
        for coll in bpy.data.collections:
            bpy.data.collections.remove(coll)

    def make_new_collection(self, name):
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
        return col
        
    def make_camera(self):
        cam = bpy.data.cameras.new('Camera')
        camera_obj = bpy.data.objects.new('Camera', cam)
        self.collection.objects.link(camera_obj)
        #camera = bpy.data.objects['Camera']
        cam.lens = 50
        camera_obj.location = Vector((0,0,10))
        return camera_obj

    def set_background(self):
        module_path = os.path.abspath(jens.__file__)

        background = jens.__path__[0] + '/images/studio_light_small.hdr'

        # The get method returns the worlds['World'] if it exists
        # otherwise it creates a new one. 
        wor = bpy.data.worlds.get('World', bpy.data.worlds.new('World'))


        wor.use_nodes = True
        node = wor.node_tree.nodes.new('ShaderNodeTexImage')
        node.location = (-400,300) 
        bg_node = bpy.data.worlds['World'].node_tree.nodes['Background']
        wor.node_tree.links.new(bg_node.inputs['Color'], node.outputs['Color'])
        im = bpy.data.images.load(background)
        node.image = im

        generate_text.generate_text_collection(r'$\sqrt{3+2}$')


if __name__ == '__main__':
    c = Clip()
    
