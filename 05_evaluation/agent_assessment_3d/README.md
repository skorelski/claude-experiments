# AI Agent Assessment Kit — 3D Print Files

All 15 STL files are ready, plus the Blender import script. Here's what you have:

## Files

The **8 hex tiles** (`tile_01_purpose.stl` through `tile_08_finops.stl`) are 86mm point-to-point, 8mm tall. Each has a raised rim, a chip slot on one edge, and an embossed symbol on the top surface — star for Purpose, cross for Tasks, downward triangle for Context, pentagon for Data, eye shape for Oversight, ring for Errors, frame for Scope, and coin ridge for FinOps.

The **scoring chip** (`chip_scoring.stl`) is a 28mm disc with a small edge ridge so it stands upright in the tile slot. Print 10 copies in red, 10 in amber/yellow, and 10 in green.

The **three status toppers** (`topper_green_go.stl`, `topper_amber_review.stl`, `topper_red_halt.stl`) are ~95mm tall with a base, stem, and distinctive top — checkmark for GO, warning triangle with exclamation for REVIEW, and octagonal column for HALT. Each prints in its respective colour.

The **score dial** (`dial_base.stl`) is an 80mm disc with raised red/amber/green arc zones and a centre peg. The **arrow** (`dial_arrow.stl`) fits onto the peg and rotates to show the final score.

The **attention flags** (`flag_attention.stl`) are 48mm pennant-on-stick pieces. Print 8 in bright yellow.

## Using in Blender

Open `import_all_in_blender.py` in Blender's Scripting tab, set the `STL_DIR` path at the top to your folder, and run it — it imports everything with the correct colours and a basic camera setup for rendering.

## Colour Guide

| File | Colour |
|---|---|
| tile_01_purpose | Deep blue |
| tile_02_tasks | Teal |
| tile_03_context | Purple |
| tile_04_data | Dark red |
| tile_05_oversight | Orange |
| tile_06_errors | Navy |
| tile_07_scope | Grey |
| tile_08_finops | Gold / yellow |
| chip_scoring | 10× RED + 10× AMBER + 10× GREEN |
| topper_green_go | Green |
| topper_amber_review | Orange / yellow |
| topper_red_halt | Red |
| dial_base | White or light grey |
| dial_arrow | Black |
| flag_attention | Bright yellow (×8 copies) |

## Reference Card

`card_reference.stl` is a flat plastic card (190×130×3.8 mm) sized to fit neatly in the 20×20 cm storage box alongside the tiles.

The card has a 2.8 mm solid base with a raised border lip around all four edges, three thin horizontal divider lines separating the content blocks, and all text embossed 1 mm above the surface using a clean sans-serif font. The content covers four blocks:

- The 8 section tiles with one-line descriptions
- The scoring chip colour guide (GREEN / AMBER / RED with score ranges)
- The three status toppers with their verdict labels
- The dial and flag instructions at the bottom

Print it in white or light grey filament so the raised text casts clear shadows and reads easily.

## Print Settings

**Layer height:** 0.15 mm | **Infill:** 20% | **Supports:** none needed

All models have 3–5° draft angles built in and are self-supporting.
