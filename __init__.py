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

class CoordinatePanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Place at Coordinates"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text = "x")
        row.prop(CoordinateOperator.bl_idname, text="Test Place")
        row = layout.row()
        row.label(text = "y")
        row.operator(CoordinateOperator.bl_idname, text="Test Place")
        row = layout.row()
        row.label(text = "z")
        row.operator(CoordinateOperator.bl_idname, text="Test Place")

class CoordinateOperator(bpy.types.Operator):
    bl_idname = "object.place_at_coords"
    bl_label = "Place at Coordinates"
    bl_description = "Enter object location manually."
    bl_options = {'REGISTER', 'UNDO'}

    x: bpy.props.FloatProperty(name="X")
    y = 0
    z = 0
    @classmethod
    def poll(self, context):
        if context.active_object:
            self.x = context.active_object.location.x
            self.y = context.active_object.location.y
            self.z = context.active_object.location.z
        print(self.x + " " + self.y + " " + self.z)
        return {"FINISHED"}
    def execute(self, context):
        print("Run")
        return {"FINISHED"}

toRegister = [
    CoordinateOperator,
    CoordinatePanel
]
def register():
    for i in toRegister:
        bpy.utils.register_class(i)
def unregister():
    for i in toRegister:
        bpy.utils.unregister_class(i)

if __name__ == "__main__":
    register()