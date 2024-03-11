def pt_to_px(pt: int):
    return round((pt / 72) * 96)


graph_height = 10_000
rows_per_pt = [416, 350, 317, 277, 246, 229, 208, 190, 179, 166]
for i, pt in enumerate(range(12, 31, 2)):
    px = pt_to_px(pt)
    row_pixel_height = graph_height / rows_per_pt[i]
    print(f"{pt = },  {px = },  {row_pixel_height = }")
