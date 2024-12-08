from . import electron_orbitals_new_3D
import bpy
from bpy.types import Menu

class VIEW_MT_electron_orbitals_menu_add(Menu):
    # Define the "Electron Orbitals" menu
    bl_idname = "V_MT_Electron_Orbitals"
    bl_label = "Simulation"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.generate_electron_orbitals",text="Generate Electron Orbitals")

# Register all operators and panels

# Define "Extras" menu
def menu_func(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.separator()
    layout.operator("mesh.generate_electron_orbitals",
                    text="Generate Electron Orbitals", icon="PACKAGE")

# Register
classes = [VIEW_MT_electron_orbitals_menu_add,electron_orbitals_new_3D.Electron_orbitals_input]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    # Add "Extras" menu to the "Add Mesh" menu 
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    # Remove "Extras" menu from the "Add Mesh" menu 
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
    