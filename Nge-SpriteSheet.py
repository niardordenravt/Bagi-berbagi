bl_info = {
    "name": "Nge-SpriteSheet",
    "author": "Run-D",
    "version": (1, 1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Nge-SpriteSheet",
    "description": "Build sprite sheets with auto or custom grid",
    "category": "Import-Export",
}

import bpy
import os
import math

# =================================================
# PROPERTIES
# =================================================
class SpriteSheetProps(bpy.types.PropertyGroup):
    directory: bpy.props.StringProperty(
        name="Directory",
        subtype='DIR_PATH'
    )

    files: bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup
    )

    quadratic: bpy.props.BoolProperty(
        name="Quadratic",
        description="Auto grid using square root of image count",
        default=True
    )

    rows: bpy.props.IntProperty(
        name="Rows",
        min=1,
        default=4
    )

    columns: bpy.props.IntProperty(
        name="Columns",
        min=1,
        default=4
    )


# =================================================
# PICK IMAGE SEQUENCE
# =================================================
class SPRITESHEET_OT_pick(bpy.types.Operator):
    bl_idname = "spritesheet.pick"
    bl_label = "Pick Image Sequence"

    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        props = context.scene.sprite_sheet_props
        props.files.clear()
        props.directory = self.directory

        for f in self.files:
            item = props.files.add()
            item.name = f.name

        self.report({'INFO'}, f"{len(self.files)} images selected")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# =================================================
# BUILD SPRITESHEET
# =================================================
class SPRITESHEET_OT_build(bpy.types.Operator):
    bl_idname = "spritesheet.build"
    bl_label = "Build Sprite Sheet"

    def execute(self, context):
        props = context.scene.sprite_sheet_props

        if not props.files:
            self.report({'ERROR'}, "No images selected")
            return {'CANCELLED'}

        paths = [os.path.join(props.directory, f.name) for f in props.files]
        paths.sort()

        count = len(paths)

        # === GRID LOGIC ===
        if props.quadratic:
            grid = int(math.sqrt(count))
            if grid * grid != count:
                self.report({'ERROR'}, "Quadratic mode requires perfect square image count")
                return {'CANCELLED'}
            rows = columns = grid
        else:
            rows = props.rows
            columns = props.columns
            if rows * columns != count:
                self.report({'ERROR'}, "Rows × Columns must equal image count")
                return {'CANCELLED'}

        images = [bpy.data.images.load(p, check_existing=True) for p in paths]
        w, h = images[0].size

        sheet = bpy.data.images.new(
            name="SpriteSheet",
            width=w * columns,
            height=h * rows,
            alpha=True
        )

        sheet_pixels = [0.0] * (sheet.size[0] * sheet.size[1] * 4)

        for i, img in enumerate(images):
            col = i % columns
            row = rows - 1 - (i // columns)

            src = list(img.pixels)

            for y in range(h):
                for x in range(w):
                    si = (y * w + x) * 4
                    di = (
                        ((row * h + y) * sheet.size[0] + (col * w + x)) * 4
                    )
                    sheet_pixels[di:di+4] = src[si:si+4]

        sheet.pixels = sheet_pixels

        # === OUTPUT NAME ===
        folder_name = os.path.basename(os.path.normpath(props.directory))
        out_path = os.path.join(
            props.directory,
            f"{folder_name}_Spritesheet.png"
        )

        sheet.filepath_raw = out_path
        sheet.file_format = 'PNG'
        sheet.save()

        self.report({'INFO'}, f"Saved: {out_path}")
        return {'FINISHED'}


# =================================================
# UI PANEL
# =================================================
class SPRITESHEET_PT_panel(bpy.types.Panel):
    bl_label = "Nge-SpriteSheet"
    bl_idname = "SPRITESHEET_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Nge-SpriteSheet"

    def draw(self, context):
        layout = self.layout
        props = context.scene.sprite_sheet_props

        layout.operator("spritesheet.pick", icon='FILE_FOLDER')

        layout.separator()
        layout.prop(props, "quadratic")

        if not props.quadratic:
            col = layout.column(align=True)
            col.prop(props, "rows")
            col.prop(props, "columns")

        layout.separator()
        layout.operator("spritesheet.build", icon='IMAGE_DATA')

        if props.files:
            layout.label(text=f"{len(props.files)} images selected")


# =================================================
# REGISTER
# =================================================
classes = (
    SpriteSheetProps,
    SPRITESHEET_OT_pick,
    SPRITESHEET_OT_build,
    SPRITESHEET_PT_panel
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.sprite_sheet_props = bpy.props.PointerProperty(
        type=SpriteSheetProps
    )

def unregister():
    del bpy.types.Scene.sprite_sheet_props
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
