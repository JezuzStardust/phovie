"""help_functions defines utility functions used by other modules. 

Functions:
    clear_scene(): Clear all Blender data. 
    reload_modules(print_to_console=False): Reloads all modules in the package. 
"""

import bpy
import sys # sys.modules 
import importlib # importlib.reload


def clear_scene():
    """Clears all Blender data in the Blender scene."""

    for data_list in (
        bpy.data.cameras,
        bpy.data.collections,
        bpy.data.curves,
        bpy.data.lights,
        bpy.data.materials,
        bpy.data.meshes,
        bpy.data.objects,
        bpy.data.particles,
        bpy.data.worlds):
        for data in data_list:
            data_list.remove(data)

def reload_modules(print_to_console=False):
    """Reloads all custom modules (modules that starts with 'jens').
    
    Blender does not do this automatically when a script is rerun, so instead of 
    constantly reloading each updated module it is easier to just run this 
    function. 
    Probably not needed after developement. 
    Perhaps it is possible to change this to make it easier to change the
    name of the package later. 
    
    Args: 
        print_to_console: An optional boolean that determines wether or not 
            to print information to console. Defaults to false.
    """
    if print_to_console:
        print("Reloading all custom modules.")
        
    module_names = [module for module in sys.modules.keys() if module.startswith('phovie')]
    for module_name in module_names:
        if print_to_console:
            print('Reloading ' + module_name)
        importlib.reload(sys.modules[module_name])

if __name__ == '__main__':
    clear_scene() 
    reload_modules(True)
