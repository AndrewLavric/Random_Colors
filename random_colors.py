bl_info={
    "name":"Random colors",
    "author":"Andrew Lavric",
    "version":(0,4),
    "blender":(2,6,6),
    "location":"View3D > Object Tools",
    "description":"Random object (face,vertex) colors",
    "category":"Object",
    "wiki_url":"https://github.com/AndrewLavric/Random_Colors",
    "tracker_url":"https://github.com/AndrewLavric/Random_Colors"}

import bpy
import random

bpy.types.Scene.random_color_r=bpy.props.FloatProperty(name='R',description='Red',min=0,max=1,subtype='FACTOR')
bpy.types.Scene.random_color_g=bpy.props.FloatProperty(name='G',description='Green',min=0,max=1,subtype='FACTOR')
bpy.types.Scene.random_color_b=bpy.props.FloatProperty(name='B',description='Blue',min=0,max=1,subtype='FACTOR')
bpy.types.Scene.random_static_color_r=bpy.props.BoolProperty(name='Static',description='Static Red')
bpy.types.Scene.random_static_color_g=bpy.props.BoolProperty(name='Static',description='Static Green')
bpy.types.Scene.random_static_color_b=bpy.props.BoolProperty(name='Static',description='Static Blue')
bpy.types.Scene.random_invert_color_r=bpy.props.BoolProperty(name='Invert',description='Invert Red')
bpy.types.Scene.random_invert_color_g=bpy.props.BoolProperty(name='Invert',description='Invert Green')
bpy.types.Scene.random_invert_color_b=bpy.props.BoolProperty(name='Invert',description='Invert Blue')
bpy.types.Scene.random_count_colors=bpy.props.IntProperty(name='Count',description='Count Colors',min=0,default=0)
bpy.types.Scene.random_gray=bpy.props.BoolProperty(name='Gray',description='Gray Colors')

class random_colors_panel(bpy.types.Panel):
    bl_idname="random_colors_panel"
    bl_label="Random Object Colors"
    bl_space_type='VIEW_3D'
    bl_region_type='TOOLS'
    def draw(self,context):
        layout=self.layout
        layout.prop(bpy.context.scene,'random_count_colors')
        box=layout.box()
        boxrow=box.row()
        box.prop(bpy.context.scene,'random_color_r')
        boxrow.prop(bpy.context.scene,'random_static_color_r')
        boxrow.prop(bpy.context.scene,'random_invert_color_r')
        box=layout.box()
        boxrow=box.row()
        box.prop(bpy.context.scene,'random_color_g')
        boxrow.prop(bpy.context.scene,'random_static_color_g')
        boxrow.prop(bpy.context.scene,'random_invert_color_g')
        box=layout.box()
        boxrow=box.row()
        box.prop(bpy.context.scene,'random_color_b')
        boxrow.prop(bpy.context.scene,'random_static_color_b')
        boxrow.prop(bpy.context.scene,'random_invert_color_b')
        box=layout.box()
        box.prop(bpy.context.scene,'random_gray')
        layout.operator("random.random_colors")

def rand_colors():
    C=bpy.context.scene
    if(C.random_gray):
        gray=random.random()
        return (gray,gray,gray)
    else:
        red=green=blue=0
        if(C.random_static_color_r):
            red=C.random_color_r
        else:
            if(C.random_invert_color_r):
                red=random.uniform(0,C.random_color_r)
            else:
                red=random.uniform(C.random_color_r,1.0)
        if(C.random_static_color_g):
            green=C.random_color_g
        else:
            if(C.random_invert_color_g):
                green=random.uniform(0,C.random_color_g)
            else:
                green=random.uniform(C.random_color_g,1.0)
        if(C.random_static_color_b):
            blue=C.random_color_b
        else:
            if(C.random_invert_color_b):
                blue=random.uniform(0,C.random_color_b)
            else:
                blue=random.uniform(C.random_color_b,1.0)
        return (red,green,blue)

class mat_assigner(bpy.types.Operator):
    bl_idname="random.random_colors"
    bl_label="Random colors"
    bl_description="Use this to random object colors"
    bl_optin={'REGISTER','UNDO'}
    def execute(self,context):
        C=bpy.context
        if((bpy.context.mode=='EDIT_MESH')|(bpy.context.mode=='PAINT_VERTEX')):
            bpy.ops.object.mode_set(mode='VERTEX_PAINT')
            vertex_colors=None
            if(C.active_object.data.vertex_colors.active==None):
                vertex_colors=C.active_object.data.vertex_colors.new()
            else:
                vertex_colors=C.active_object.data.vertex_colors.active
            if(C.scene.random_count_colors==0):
                for poly in C.active_object.data.polygons:
                    if(poly.select):
                        rgb=rand_colors()
                        for index in poly.loop_indices:
                            vertex_colors.data[index].color=rgb
            else:
                list_colors=[]
                for count in range(C.scene.random_count_colors):
                    list_colors.append(rand_colors())
                for poly in C.active_object.data.polygons:
                    if(poly.select):
                        rgb=random.choice(list_colors)
                        for index in poly.loop_indices:
                            vertex_colors.data[index].color=rgb
        if(bpy.context.mode=='OBJECT'):
            material=None
            if(C.scene.random_count_colors==0):
                for ob in C.selected_objects:
                    rgb=rand_colors()
                    ob.color=rgb+(1.0,)
                    if(ob.active_material==None):
                        if(material==None):
                            material=bpy.data.materials.new('mat')
                            material.use_object_color=True
                        ob.active_material=material
            else:
                list_colors=[]
                for count in range(C.scene.random_count_colors):
                    list_colors.append(rand_colors())
                for ob in C.selected_objects:
                    ob.color=random.choice(list_colors)+(1.0,)
                    if(ob.active_material==None):
                        if(material==None):
                            material=bpy.data.materials.new('mat')
                            material.use_object_color=True
                        ob.active_material=material
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__": 
    register()
