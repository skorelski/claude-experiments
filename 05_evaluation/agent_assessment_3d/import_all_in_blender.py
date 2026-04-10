"""
AI Agent Assessment Kit — Blender Import Script
================================================
Paste this into Blender's Scripting tab and click Run.
It imports all 15 STL files into the scene, assigns
colour materials, and arranges everything in a neat grid.

How to use:
  1. Open Blender
  2. Go to the Scripting workspace (top tab)
  3. Click New → paste this script
  4. Set STL_DIR below to the folder where your STL files are
  5. Click Run Script (▶)

After running you can:
  - View all pieces in the 3D viewport
  - Render a preview image
  - Fine-tune any piece and re-export as STL via
      File > Export > Stl  (with  Apply Modifiers ✓)
"""

import bpy
import os
import math

# ── CONFIGURE THIS ────────────────────────────────────────────────────────────
STL_DIR = r"C:\Users\YourName\Documents\agent_assessment_3d"
# On Mac/Linux:  STL_DIR = "/Users/yourname/Documents/agent_assessment_3d"
# ──────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────
# Colour palette (name → RGBA linear)
# ─────────────────────────────────────────────────────────
COLOURS = {
    # Hex tiles
    "tile_01_purpose":    (0.05, 0.18, 0.60, 1.0),   # deep blue
    "tile_02_tasks":      (0.05, 0.55, 0.50, 1.0),   # teal
    "tile_03_context":    (0.40, 0.10, 0.55, 1.0),   # purple
    "tile_04_data":       (0.55, 0.05, 0.08, 1.0),   # dark red
    "tile_05_oversight":  (0.80, 0.35, 0.02, 1.0),   # orange
    "tile_06_errors":     (0.05, 0.15, 0.40, 1.0),   # navy
    "tile_07_scope":      (0.40, 0.40, 0.42, 1.0),   # grey
    "tile_08_finops":     (0.75, 0.55, 0.05, 1.0),   # gold
    # Chips
    "chip_scoring":       (0.85, 0.85, 0.85, 1.0),   # light grey (placeholder)
    # Toppers
    "topper_green_go":    (0.10, 0.70, 0.20, 1.0),
    "topper_amber_review":(0.90, 0.55, 0.02, 1.0),
    "topper_red_halt":    (0.80, 0.08, 0.08, 1.0),
    # Dial
    "dial_base":          (0.90, 0.90, 0.88, 1.0),   # off-white
    "dial_arrow":         (0.05, 0.05, 0.05, 1.0),   # black
    # Flag
    "flag_attention":     (1.00, 0.85, 0.00, 1.0),   # bright yellow
}

# Layout grid positions (x, y) in Blender units (metres → mm scale)
# Each mm = 0.001 Blender units
MM = 0.001

LAYOUT = {
    # Tiles: row 1
    "tile_01_purpose":     ( 0 * MM * 100,   0 * MM * 100),
    "tile_02_tasks":       ( 1 * MM * 100,   0 * MM * 100),
    "tile_03_context":     ( 2 * MM * 100,   0 * MM * 100),
    "tile_04_data":        ( 3 * MM * 100,   0 * MM * 100),
    "tile_05_oversight":   ( 4 * MM * 100,   0 * MM * 100),
    "tile_06_errors":      ( 5 * MM * 100,   0 * MM * 100),
    "tile_07_scope":       ( 6 * MM * 100,   0 * MM * 100),
    "tile_08_finops":      ( 7 * MM * 100,   0 * MM * 100),
    # Chips + toppers: row 2
    "chip_scoring":        ( 0 * MM * 100,  -1.2 * MM * 100),
    "topper_green_go":     ( 1 * MM * 100,  -1.2 * MM * 100),
    "topper_amber_review": ( 2 * MM * 100,  -1.2 * MM * 100),
    "topper_red_halt":     ( 3 * MM * 100,  -1.2 * MM * 100),
    # Dial + flag: row 3
    "dial_base":           ( 0 * MM * 100,  -2.4 * MM * 100),
    "dial_arrow":          ( 1 * MM * 100,  -2.4 * MM * 100),
    "flag_attention":      ( 2 * MM * 100,  -2.4 * MM * 100),
}

# ─────────────────────────────────────────────────────────
# Helper: create a basic PBR material
# ─────────────────────────────────────────────────────────
def make_material(name, rgba):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = rgba
        bsdf.inputs["Roughness"].default_value = 0.6
        bsdf.inputs["Metallic"].default_value  = 0.0
    return mat

# ─────────────────────────────────────────────────────────
# Import all STLs
# ─────────────────────────────────────────────────────────
def main():
    # Clear the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Set mm scale
    bpy.context.scene.unit_settings.system      = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit  = 'MILLIMETERS'

    stl_files = [f for f in os.listdir(STL_DIR) if f.endswith('.stl')]
    if not stl_files:
        print(f"No STL files found in: {STL_DIR}")
        return

    for filename in sorted(stl_files):
        base = filename.replace('.stl', '')
        filepath = os.path.join(STL_DIR, filename)

        # Import
        bpy.ops.wm.stl_import(filepath=filepath)
        obj = bpy.context.selected_objects[-1]
        obj.name = base

        # Set scale (STL is in mm, Blender is in metres)
        obj.scale = (MM, MM, MM)
        bpy.ops.object.transform_apply(scale=True)

        # Position
        if base in LAYOUT:
            x, y = LAYOUT[base]
            obj.location = (x, y, 0)

        # Assign material
        colour_key = base
        # Chips get neutral grey (user will split into 3 colours manually)
        rgba = COLOURS.get(colour_key, (0.7, 0.7, 0.7, 1.0))
        mat  = make_material(base + "_mat", rgba)
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        print(f"  Imported: {base}")

    # Set up a simple camera + sun for a nice preview
    bpy.ops.object.light_add(type='SUN', location=(0.5, -0.3, 0.8))
    bpy.context.active_object.data.energy = 3.0

    bpy.ops.object.camera_add(location=(0.4, -0.6, 0.5))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(55), 0, math.radians(40))
    bpy.context.scene.camera = cam

    print(f"\nDone! {len(stl_files)} objects imported.")
    print("Tip: Press Numpad 0 to look through the camera, then F12 to render.")

main()
