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

# This addon allows the easy relocation via x,y,z coordinates of both individual objects and groups of objects.

import bpy

bl_info = {
    "name" : "Object to Coordinates",
    "author" : "neuralworm",
    "description" : "Easy widget to take a single or group of objects and place them at designated coordinates.",
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
class MULTI_SELECT_PROPERTIES(bpy.types.PropertyGroup):
    move_by_type: bpy.props.EnumProperty(name = "Move...", description="Move all objects to coordinate, or move group average location to coordinate.", items=[("All to Coordinate", "All to Coordinate", "All to Coordinate"), ("Average to Coordinate", "Average to Coordinate", "Average to Coordinate")])
  


class COORDINATE_PANEL_PT_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
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
        # IF MULTIPLE OBJECTS SELECTED
        if len(context.selected_objects) > 1:
            row = layout.row()
            row.label(text= "Multiple selected")
            layout.prop(scene.multi_select_props, "move_by_type")
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
        # Determine if solo or group
        if len(context.selected_objects) > 1:
            self.moveGroup(context)
        else:
            self.moveOne(context)
        
        return {"FINISHED"}
    def moveOne(self, context):
        scene = context.scene
        coordinates = scene.object_coordinates
        object = context.object
        object.location.x = coordinates.x
        object.location.y = coordinates.y
        object.location.z = coordinates.z
    def moveGroup(self, context):
        group = context.selected_objects
        scene = context.scene
        coordinates = scene.object_coordinates
        if(scene.multi_select_props.move_by_type == "All to Coordinate"):
            for i in group:
                i.location.x = coordinates.x
                i.location.y = coordinates.y
                i.location.z = coordinates.z
        if(scene.multi_select_props.move_by_type == "Average to Coordinate"):
            mean = self.getGroupMean(group)
            translation = self.getGroupTranslation(mean, [coordinates.x, coordinates.y, coordinates.z])
            # finish this
            for i in group:
                i.location.x -= translation[0]
                i.location.y -= translation[1]
                i.location.z -= translation[2]

    def getGroupMean(self, objects):
        vector = [0,0,0]
        for i in objects:
            vector[0] += i.location.x
            vector[1] += i.location.y
            vector[2] += i.location.z
        length = len(objects)
        # divide total x,y,z coord by length of objects
        for indx, i in enumerate(vector):
            vector[indx] = i / length 
        return vector
    def getGroupTranslation(self, meanVector, desiredVector):
        return [meanVector[0] - desiredVector[0], meanVector[1] - desiredVector[1], meanVector[2] - desiredVector[2]]
    def getObjectTranslation(self, object, translationVector):
        return [translationVector[0] - object.location.x, translationVector[1] - object.location.y, translationVector[2] - object.location.z]


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
    RESET_COORD_OPERATOR,
    MULTI_SELECT_PROPERTIES
]
def register():
    for i in toRegister:
        bpy.utils.register_class(i)
    bpy.types.Scene.object_coordinates = bpy.props.PointerProperty(type = COORDINATE_PROPERTIES)
    bpy.types.Scene.multi_select_props = bpy.props.PointerProperty(type = MULTI_SELECT_PROPERTIES)
def unregister():
    for i in toRegister:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.object_coordinates
    del bpy.types.Scene.multi_select_props



if __name__ == "__main__":
    register()