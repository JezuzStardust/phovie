# TODO: Add copyright. 

"""This module creates a collection with curve objects that are generated from
output of a LaTeX-command or text. 

Typical usage: 
    tex_code = r'\frac{a}{b} \int_0^\infty dx f(x)'
    generate_text_collection(tex_code)
    
Results: 
    Produces a collection with the curve objects. 
"""

from importlib import resources
import hashlib
import os
import re
import subprocess

import bpy

from phovie import templates
import svgparser.svgparser

pattern = r"(depth=([+-]?(\d+(\.\d*)?|[+-]?(\.\d+))([eE][+-]?\d+)?)pt)"
re_pattern = re.compile(pattern)

blender_file_path = bpy.path.abspath("//")
latex_directory = blender_file_path + "latex-file/"  # TODO: Make name a constant.

def generate_text_collection(texcode, collection_to_move_to=None):
    """Generates a new collection with curve object from a string with LaTeX-commands or text.
    Args:
        texcode: A string containing valid LaTeX code. Use r to make the string raw if it contains, e.g., backslash.
        collection_to_move_to: A collection where all objects are moved.
    """
    if not os.path.exists(latex_directory):
        make_directory(latex_directory)

    # TODO: If another instance is already imported the actual name will be different (added .001, etc).
    name = gen_hash(texcode)
    file_path = latex_directory + name

    gen_latex_source(texcode, latex_directory, name)
    gen_dvi(texcode, latex_directory, name)
    depth = str(gen_svg(file_path))

    # TODO: String this together better.
    # Each generation should return the path of the new file.
    # Each generation should take the previous path as input.
    # Then we can use e.g. os.path.split etc to convert
    # filenames and endings when needed.

    # bpy.ops.import_curve.svg(filepath=file_path + '.svg')
    coll_name = name + ".svg"
    parser = svgparser.svgparser.SVGLoader(
        bpy.context, file_path + ".svg", origin="PC", depth=depth,
    )
    # TODO: Rethink this. Perhaps the parsers job is simply to get the data. 
    # the actual creation of the curves could be done externally.
    parser.parse()
    parser.create_blender_splines()

    # Scales each curve.
    # TODO: Scale should perhaps be a parameter.
    for object in bpy.data.collections[coll_name].objects:
        object.name = name
        object.scale = (100, 100, 100)
    return bpy.data.collections[coll_name].objects

def make_directory(latex_directory):
    """Creates the directory to store the output files.
    These files can in general be discarded afterwards."""
    print("Creating directory: " + latex_directory)
    os.system("mkdir -p " + '"' + latex_directory + '"')

def gen_hash(expression):  # , template_tex_file_body):
    """Generates a hash based on the expression.
    This is used to give a unique name."""
    # TODO: Consider moving this to a general utility module.
    # TODO: Consider also involving the tex_template (if needed).

    id_str = str(expression)  # + template_tex_file_body)
    hasher = hashlib.sha256()
    hasher.update(id_str.encode())
    # Truncating at 16 bytes for cleanliness
    return hasher.hexdigest()[:8]

def gen_latex_source(texcode, directory, name):
    """Generates the LaTeX source file. 
    Use the input and the template to create the .tex file. 
    The output is stored in the directory."""
    # TODO: Make the name of the tex_template a constant.
    template = resources.read_text(templates, "tex_template.tex")
    filedata = template.replace("YOURTEXTHERE", texcode)
    file_path = directory + name + ".tex"
    with open(file_path, "w") as file:
        file.write(filedata)

    return file_path

def gen_dvi(texcode, latex_directory, name):
    """Generates a dvi from the LaTeX source. 
    The result is stored in latex_directory as name.dvi."""
    latex_command = " ".join(
        [
            "latex",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory",
            '"' + latex_directory + '"',
            '"' + latex_directory + name + ".tex" + '"',
            #+ ' > /dev/null' # Send output to null if not needed.
        ]
    )

    os.system(latex_command)
    # TODO: Add check and output logfile for latex in case it fails.
    # See manimlib/utils/tex_file_writing.py line 66-72.

def gen_svg(file_path):
    """Generates the svg file from the dvi file.
    Returns the text depth variable (distance below text baseline where the 
    output ends. If it does not exist, the output is zero."""
    # Remember to set "export LIBGS=/usr/local/lib/libgs.dylib"
    # in the .zshrc and source it! 
    #If this dylib is missing install ghostscript using Homebrew.
    print("----------Generating svg-file----------")
    svg_command = " ".join(
        [
            "dvisvgm",
            "-n",  # No fonts!
            "--bbox=preview",
            # '--libgs=/usr/local/lib/libgs.dylib', # Not needed if $LIBGS is set.
            "--output=" + '"' + file_path + ".svg" + '"',
            '"' + file_path + ".dvi" '"',
        ]
    ) 
    process = subprocess.run([svg_command], capture_output=True, shell=True)
    depth_re = re.compile(r'(?<=depth=)\d+.\d+pt')
    # Note that the diagnostic output ends up in stderr, in accordance with POSIX.
    print(process.stderr.decode("UTF-8"))
    depth = re.search(depth_re, process.stderr.decode("UTF-8"))
    if depth: 
        return depth[0]
    else:
        return 0

    # proc = subprocess.Popen([svg_command], stdout=subprocess.PIPE, shell=True)
    # (out, err) = proc.communicate()
    # print('hej', out) 
    # print('mej', err) 
    # print("start")
    # for p in re_pattern.findall(str(out)):
    #     print("hej", p)
    # print("end")
    # print(out)  # Use this to parse baseline???

"""
    1. Create directory if needed (perhaps move somewhere else, e.g., where scene is created). 
    2. Generate hash for name. 
    3. Create LaTeX-file frome template and string. 
    4. Run LaTe to create a dvi-file. 
    5. Use dvisvgm to reate svg-file. 
    6. Import the svg-file to Blender. 
    
    Probably I should write a custom parser for 6. 
    
    Overall function
    latex_output_path = init_directory()
    dvi_file = gen_dvi(name, latex_output_path) (should gen latex_source and then the dvi-file)
    svg_file = gen_svg(dvi_file) (should gen the svg-file from the dvi)
    import_svg(svg_file)
     
    """

# TODO: Consider generating a single object in Blender instead of a new collection.


""" To get TikZ to work we should do the following:
    - Use latex to produce .dvi file (not pdf!)
    - Use dvisvgm -n file.dvi --libgs=/usr/local/lib/libgs.dylib 
    to create .svg file. 
    - Use inkscape to make all the strokes into paths. 
    inkscape --actions="select-all;object-to-path;FileSave;FileClose" --batch-process file.svg" 
    Note: There is a problem to solve here. If the LaTeX contains both 
    math and tikz there might be lines that are problematics in the tikz figure. 
    These are created as lines with thick strokes and they yield only a thin
    line when imported to Blender. 
    In the gui we can choose all objects that have an undefined stroke and then choose object-to-path in the object menu. 
    Then we can choose all objects which have a defined color (black) and then choose stroke-to-path. 
    I need to figure out how to do this from the command line. 
"""
