import time
import datetime
import bpy, bmesh
from scipy.constants import physical_constants
import scipy.special as sp
import numpy as np
# from numpy import interp 
from bpy.types import Operator
from bpy.props import (StringProperty,IntProperty,FloatProperty,BoolProperty)
from itertools import chain
import math
import colorsys
# import mcubes
from skimage import measure

def asSpherical(x,y,z,eps):
    #takes list xyz (single coord)
    r       =  np.sqrt(x*x + y*y + z*z)
    theta   =  np.arccos(z/(r + eps))
    phi     =  np.arctan2(y,x)
    return [r,theta,phi]

# Normalized radial function Rnl(r)
def radial_function(n, l, r, a0):
    """ Compute the normalized radial part of the wavefunction using
    Laguerre polynomials and an exponential decay factor.

    Args:
        n (int): principal quantum number
        l (int): azimuthal quantum number
        r (numpy.ndarray): radial coordinate
        a0 (float): scaled Bohr radius
    Returns:
        numpy.ndarray: wavefunction radial component
    """

    # Laguerre polynomials describe how the electron density
    # changes as the distance from the nucleus increases
    laguerre = sp.genlaguerre(n - l - 1, 2 * l + 1)

    # Normalized radial distance from the nucleus
    p = 2 * r / (n * a0)

    # This factor ensures the radial wavefunction is normalized
    constant_factor = np.sqrt(
        ((2 / n * a0) ** 3 * (sp.factorial(n - l - 1))) /
        (2 * n * (sp.factorial(n + l)))
    )

    # The radial part of the wavefunction is constructed by the product of:
    # - Constant factor:
    #   Normalizes the radial wavefunction

    # - Exponential decay factor: np.exp(-p / 2)
    #   Reflects the decrease in probability of finding an
    #   electron as it moves away from the nucleus

    # - Power-law dependence on radial distance: p ** l
    #   Introduces a dependency based on the azimuthal quantum number 'l',
    #   indicating different radial behaviors for different orbitals

    # - Laguerre polynomial: laguerre(p)
    #   Captures oscillations in the electron density
    #   as a function of radial distance
    return constant_factor * np.exp(-p / 2) * (p ** l) * laguerre(p)


# Normalized angular function Ylm(θ,φ)
def angular_function(m, l, theta, phi):
    """ Compute the normalized angular part of the wavefunction using
    Legendre polynomials and a phase-shifting exponential factor.

    Args:
        m (int): magnetic quantum number
        l (int): azimuthal quantum number
        theta (numpy.ndarray): polar angle
        phi (int): azimuthal angle
    Returns:
        numpy.ndarray: wavefunction angular component
    """

    # Legendre polynomials describe the spatial arrangement and directional
    # characteristics of electron probability densities
    legendre = sp.lpmv(m, l, np.cos(theta))

    # This factor ensures that the angular wavefunction is normalized
    constant_factor = ((-1) ** m) * np.sqrt(
        ((2 * l + 1) * sp.factorial(l - np.abs(m))) /
        (4 * np.pi * sp.factorial(l + np.abs(m)))
    )

    # The angular part of the wavefunction is constructed by the product of:
    # - Constant factor:
    #   Normalizes the angular wavefunction

    # - Legendre polynomial:
    #   Describes the angular dependence of the wavefunction based on the quantum numbers.
    #   Providing insight into the orientation and shape of electron orbitals
    #   around the nucleus for given quantum numbers

    # - Exponential factor: np.real(np.exp(1.j * m * phi))
    #   Introduces a phase shift dependent on the magnetic quantum
    #   number 'm' and the azimuthal angle 'phi'
    return constant_factor * legendre * np.real(np.exp(1.j * m * phi))


# Normalized wavefunction Ψnlm(r,θ,φ) as a product of Rnl(r).Ylm(θ,φ)
def compute_wavefunction(n, l, m, a0_scale_factor,grid_extent,grid_resolution):
    """ Compute the normalized wavefunction as a product
    of its radial and angular components.

    Args:
        n (int): principal quantum number
        l (int): azimuthal quantum number
        m (int): magnetic quantum number
        a0_scale_factor (float): Bohr radius scale factor
    Returns:
        numpy.ndarray: wavefunction
    """

    # The Bohr radius sets the scale of the wavefunction and determines the size of the atom.
    # By scaling it, we adapt the wavefunction's spatial extent for effective visualization
    global a0
    a0 = a0_scale_factor * physical_constants['Bohr radius'][0] * 1e+12

    # Establish a grid in the z-x plane, allowing the wavefunction to assign a probability
    # value to each point. This grid aids in visualizing the electron's spatial distribution
    # grid_extent = 480
    # grid_resolution = 100
    z = x = y = np.linspace(-grid_extent, grid_extent, grid_resolution)
    z, x, y= np.meshgrid(z, x, y)

    # Using an epsilon value to prevent division by zero during the calculation of angles
    eps = np.finfo(float).eps

    # Compute the wavefunction by multiplying the radial and angular parts.
    # The radial part considers the distance from the nucleus, whereas the angular part
    # looks into the spatial orientation. Together, they define the electron's behavior
    # in the atom's vicinity
    r,theta,phi = asSpherical(x,y,z,eps)

    psi = radial_function(n, l, r, a0) * angular_function(m, l, theta, phi)

    # Return the computed wavefunction, which encapsulates the quantum state
    # of an electron in a hydrogen atom. The wavefunction contains complex amplitudes
    # that provide information about the quantum state's magnitude and phase
    return psi


# Probability density |Ψ|^2
def compute_probability_density(psi):
    """ Compute the probability density of a given wavefunction.
    Args:
        psi (numpy.ndarray): wavefunction
    Returns:
        numpy.ndarray: wavefunction probability density
    """

    # Return the computed probability density, which gives the likelihood of finding
    # the electron at a specific point in space for the given quantum state. The
    # values represent the square magnitude of the wavefunction, encapsulating the
    # probability of the electron's presence in different regions of the atom
    return np.abs(psi) ** 2

def create_mesh_for(objname,verts,faces):
    me = bpy.data.meshes.new(objname)  # create a new mesh
    me.from_pydata(verts,[],faces)
    me.update()      # update the mesh with the new data


    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
    bm.to_mesh(me)

    ob = bpy.data.objects.new(objname,me) # create a new object
    ob.data = me          # link the mesh data to the object
    return ob
   
def make_object_in_scene(object_name,verts,faces):

    block=create_mesh_for(object_name,verts,faces)

    bpy.context.collection.objects.link(block)
    selectobj(block)
    
    #recalculate normals to outside
    # block.select_set(state=True)
    # bpy.context.view_layer.objects.active = block    # go edit mode
    # bpy.ops.object.mode_set(mode='EDIT')
    # # select al faces
    # bpy.ops.mesh.select_all(action='SELECT')
    # # recalculate outside normals 
    # bpy.ops.mesh.normals_make_consistent(inside=False)
    # # go object mode again
    # bpy.ops.object.editmode_toggle()
    
    return block

def selectobj(obj):
    for o2 in bpy.context.scene.objects:
        if o2==obj: 
            o2.select_set(state=True)

def create_material(obj,name,color_value,alpha_value):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat_nodes = mat.node_tree.nodes
    mat_links = mat.node_tree.links
    # a new material node tree already has a diffuse and material output node
    #output = mat_nodes['Material Output']
    diffuse = mat_nodes['Principled BSDF']

    # obj = bpy.context.active_object
    #add new material to object
    obj.data.materials.append(mat)
    #added material will be last in material slots
    #so make last slot active
    obj.active_material_index = len(obj.data.materials) - 1 

    # add new Color Ramp and set location
    ramp = mat_nodes.new("ShaderNodeValToRGB")
    ramp.location=(-300,170)
    # add new Value node and set location
    value = mat_nodes.new("ShaderNodeValue")
    value.location=(-500,95)
    # add Math node
    math = mat_nodes.new("ShaderNodeMath")
    math.location=(-250,-50)
    math.operation="MULTIPLY"

    # link Color Ramp to Principled BSDF
    mat_links.new(diffuse.inputs[0], ramp.outputs[0])
    # link Value node to Color Ramp
    mat_links.new(ramp.inputs[0], value.outputs[0])
    # link Math node to Principled BSDF Emission Strenght 
    mat_links.new(diffuse.inputs[28], math.outputs[0])
    # link Value node to Math node
    mat_links.new(math.inputs[0], value.outputs[0])
    # link Color Ranp node to Principled BSDF Emission Color
    mat_links.new(diffuse.inputs[27], ramp.outputs[0])

    # set Value node value
    value.outputs["Value"].default_value=color_value
    # set math node multiply value
    math.inputs[1].default_value=10

    ramp.color_ramp.elements[0].color=[1,0,0,1]
    ramp.color_ramp.elements[1].color=[1,1,0,1]

    diffuse.inputs.get("Metallic").default_value=0
    diffuse.inputs.get("Alpha").default_value=alpha_value

def plot_wf_probability_density(n, l, m, a0_scale_factor,grid_extent,grid_resolution):
    """ Plot the probability density of the hydrogen
    atom's wavefunction for a given quantum state (n,l,m).

    Args:
        n (int): principal quantum number, determines the energy level and size of the orbital
        l (int): azimuthal quantum number, defines the shape of the orbital
        m (int): magnetic quantum number, defines the orientation of the orbital
        a0_scale_factor (float): Bohr radius scale factor
    """

    # Quantum numbers validation
    if not isinstance(n, int) or n < 1:
        raise ValueError('n should be an integer satisfying the condition: n >= 1')
    if not isinstance(l, int) or not (0 <= l < n):
        raise ValueError('l should be an integer satisfying the condition: 0 <= l < n')
    if not isinstance(m, int) or not (-l <= m <= l):
        raise ValueError('m should be an integer satisfying the condition: -l <= m <= l')

    psi = compute_wavefunction(n, l, m, a0_scale_factor,grid_extent,grid_resolution)
    # print("psi shape: ",psi.shape)

    return psi

def collection_add(col_name,obj):

    try:
        collection = bpy.data.collections[col_name]
    except:
        collection = bpy.data.collections.new(name=col_name)

    # retrieve the scene collection
    scene_collection = bpy.context.scene.collection

    # link the new collection into the scene
    scene_collection.children.link(collection)

    # add the object into the collection 
    collection.objects.link(obj)

    ##################################################################################################
# Define UI and execute

class Electron_orbitals_input(Operator):
    bl_idname = "mesh.generate_electron_orbitals"
    bl_label = "generate electron orbitals"
    bl_description = ("Generate electron orbitals based combinations of n, l & m \n"
                      "+ number of contours + mesh resolution.")
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}

    n: IntProperty(
                name="Principal n    (>= 1, <= 10)",
                description="The principal quantum number (n) "
                            "describes the size of the orbital.",
                min=1,
                max=10,
                default=3
                )
    l: IntProperty(
                name="Angular l    (>= 0, <= n-1)",
                description="The angular quantum number (l) "
                            "describes the shape of the orbital.",
                min=0,
                max=9,
                default=1
                )
    m: IntProperty(
                name="Magnetic m    (>= -l, <= l)",
                description="Magnetic quantum number (m), "
                            "to describe the orientation in "
                            "space of a particular orbital.",
                min=-9,
                max=9,
                default=1
                )

    grid_extent: IntProperty(
                name="Grid extent >= 1",
                description="The extent of the grid in the x, y and z direction"
                            "allowing the wavefunction to assign a probability "
                            "value to each point. This grid aids in visualizing " 
                            "the electron's spatial distribution",
                min=1,
                default=480
                )
    
    grid_resolution: IntProperty(
                name="Grid resolution >= 1",
                description="The resolution of the grid",
                min=1,
                default=400
                )
    
    levels: IntProperty(
                name="Number of iso levels <= 30, >=1",
                description="Number of isosurfaces to generate",
                min=1,
                default=1,
                max=30
                )

    sf: FloatProperty(
                name="Bohr radius scale Factor <= 3, >= 0",
                description="The Bohr radius sets the scale of the wavefunction "
                "and determines the size of the atom. By scaling it, we adapt "
                "the wavefunction's spatial extent for effective visualization",
                min=0.0,
                max=3.0,
                default=0.4
                )

    delete_orbs : BoolProperty(
            name="Delete all generated iso surfaces objects?",
            default=True,
            description="Here you can specify if you want all"
            "generated iso surface meshes to be deleted"
            )

    ok : BoolProperty(
            name="Generate electron orbitals mesh",
            default=False,
            description="Generate meshes visualizing electron orbtals"
            )

    # Display the options
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.operator_defaults")
        # layout.operator_context = 'INVOKE_REGION_WIN'

        box = layout.box()
        #box.label(text="Input")
        col = box.column(align=True)
        col.prop(self, "n")
        col.prop(self, "l")
        col.prop(self, "m")
        col.prop(self, "grid_extent")
        col.prop(self, "grid_resolution")
        col.prop(self, "levels")
        col.prop(self, "sf")
        col.prop(self, "delete_orbs")
        box = layout.box()
        box.prop(self, "ok", toggle=True)

    def invoke(self,context,event):
        return self.execute(context)
        # return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):

        #start time recording
        if self.ok==True:
            start_time = time.time()

        if bpy.context.mode!='OBJECT': # if not in OBJECT mode, set OBJECT mode
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
        
        #unhide all hidden objects
        for obj in bpy.data.objects:
            obj.hide_set(False)
            obj.hide_viewport=False

        #delete all objects from previous run if applicable 
        if self.delete_orbs:
            #Delete previous generated Blender MESH objects
            bpy.ops.object.select_all(action='DESELECT')
            for ob in bpy.context.scene.objects:
                if ob.type == 'MESH' and ob.name.startswith("orb_"):
                    #Select the object
                    ob.select_set(state=True)
            #Delete all objects selected above 
            bpy.ops.object.delete()
 
        # remove unsused blocks
        for block in bpy.data.meshes:
            if block.users == 0:
                bpy.data.meshes.remove(block)
        for block in bpy.data.texts:
            if block.users == 0:
                bpy.data.texts.remove(block)
        for block in bpy.data.node_groups:
            if block.users == 0:
                bpy.data.node_groups.remove(block)
        for block in bpy.data.actions:
            if block.users == 0:
                bpy.data.actions.remove(block)
        for block in bpy.data.curves:
            if block.users == 0:
                bpy.data.curves.remove(block)
        for block in bpy.data.cameras:
            if block.users == 0:
                bpy.data.cameras.remove(block)
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)
        
        bpy.context.scene.cursor.location = (0,0,0) #put curser in world center
        bpy.context.scene.cursor.rotation_euler = (0,0,0) #put curser in world center

        if self.ok==False:
            return {'FINISHED'}  #return to operator screen if execute button is not pressed

        psi = plot_wf_probability_density(self.n,self.l, self.m, self.sf, self.grid_extent,self.grid_resolution)
        prob_density = compute_probability_density(psi)
        min = prob_density.min()
        max = prob_density.max()

        if self.levels < 10:
            nivos=10
        else:
            nivos=self.levels

        isostep = 0
        width=(max-min)/nivos
        old_min=min+(width/10)
        old_max=max-(width/10)

        print("min=",min," max=",max)
        print("old_min=",old_min," old_max=",old_max)
        print("a0=",a0)

        col_name="orb_" + str(self.n) + "_" + str(self.l) + "_" + str(self.m) + "_" + str(round(self.sf,2)) + "_" + str(self.grid_extent) + "_" + str(self.grid_resolution)
        try:
            collection = bpy.data.collections[col_name]
        except:
            collection = bpy.data.collections.new(name=col_name)

            # retrieve the scene collection
            scene_collection = bpy.context.scene.collection

            # link the new collection into the scene
            try:
                scene_collection.children.link(collection)
            except:
                bla=1

            bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[collection.name]

        for iso in np.geomspace(max-(width/10),min+(width/20),nivos,endpoint=False):

            isostep = isostep + 1

            # if self.levels less than 10 -> only create the number of iso mesh levels equal as specified in self.levels  
            if nivos != self.levels:
                if (10 - self.levels) >= isostep:
                    continue 
            
            obj_name="orb_" + str(self.n) + "_" + str(self.l) + "_" + str(self.m) + "_" + str(round(self.sf,2)) + "_" + str(self.grid_extent) + "_" + str(self.grid_resolution) +"_" + str(isostep)

            verts, faces, normals, values = measure.marching_cubes(prob_density,iso,gradient_direction="ascent")

            obj = make_object_in_scene(obj_name,verts,faces)

            print(obj_name + " created")
            
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

            obj.location = [0,0,0]

            color_value = (( (iso - old_min) / (old_max - old_min) ))
            
            #if last loop make alpha value a fixed value for better visualization
            if isostep == nivos: 
                alpha_value=0.174
            else:
                alpha_value=color_value

            print("alpha_value: ", alpha_value)
            print("color_value: ", color_value)
            create_material(obj,"mat_iso_" + str(isostep),color_value,alpha_value)


        #Frame Viewport to Object 
        area_type = 'VIEW_3D'
        areas  = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        with bpy.context.temp_override(
            window=bpy.context.window,
            area=areas[0],
            region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
            screen=bpy.context.window.screen):
            bpy.ops.view3d.view_selected()

        bpy.ops.object.select_all(action='DESELECT')

        elapsed = time.time()-start_time
        elapsed =round(elapsed)
        conversion = datetime.timedelta(seconds=elapsed)
        converted_time = str(conversion)
        print("Elapsed Time %r"%converted_time)  
        
        self.ok=False
        
        return {'FINISHED'}
        
        
      
