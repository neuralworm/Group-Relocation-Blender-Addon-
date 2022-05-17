# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy

bl_info = {
    "name" : "placeatcoords",
    "author" : "j",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}
# Properties
class COORDINATE_PROPERTIES(bpy.types.PropertyGroup):
    x: bpy.props.FloatProperty(name="X", default= 0)
    y: bpy.props.FloatProperty(name="Y", default= 0)
    z: bpy.props.FloatProperty(name="Z", default= 0)

  


class COORDINATE_PANEL_PT_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Object Coordinates"
    bl_context = "objectmode"
    bl_idname = "COORDINATE_PANEL_PT_panel"
    @classmethod
    def poll(self, context):
        return len(context.selected_objects) != 0

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        coordinates = scene.object_coordinates
        row = layout.row()
        row.operator(RESET_COORD_OPERATOR.bl_idname, icon="OUTLINER_OB_EMPTY")

        layout.prop(coordinates, "x")
        layout.prop(coordinates, "y")
        layout.prop(coordinates, "z")

        row = layout.row()
        row.operator(COORDINATE_PLACEMENT_OPERATOR.bl_idname, icon="OUTLINER_OB_EMPTY")
       
class COORDINATE_PLACEMENT_OPERATOR(bpy.types.Operator):
    bl_idname = "object.place_at_coords"
    bl_label = "Place at Coordinates"
    bl_description = "Enter object location manually."

    @classmethod
    def poll(self, context):
        return context.object is not None
    def execute(self, context):
        scene = context.scene
        coordinates = scene.object_coordinates
        object = context.object
        object.location.x = coordinates.x
        object.location.y = coordinates.y
        object.location.z = coordinates.z
        return {"FINISHED"}

class RESET_COORD_OPERATOR(bpy.types.Operator):
    bl_idname = "object.reset_coordinates"
    bl_label = "Zero out vector"
    bl_description = "Zero out vector"
    
    @classmethod
    def poll(self, context):
        return context.object is not None
    def execute(self, context):
        scene = context.scene
        coordinates = scene.object_coordinates
        coordinates.x = 0.0
        coordinates.y = 0.0
        coordinates.z = 0.0
        return {"FINISHED"}


toRegister = [
    COORDINATE_PROPERTIES,
    COORDINATE_PLACEMENT_OPERATOR,
    COORDINATE_PANEL_PT_panel,
    RESET_COORD_OPERATOR
]
def register():
    for i in toRegister:
        bpy.utils.register_class(i)
    bpy.types.Scene.object_coordinates = bpy.props.PointerProperty(type = COORDINATE_PROPERTIES)

def unregister():
    for i in toRegister:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.object_coordinates


if __name__ == "__main__":
    register()