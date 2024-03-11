import PySimpleGUI as sg


def pt_to_px(pt: int):
    return round((pt / 72) * 96)


def update_graph(window, values):
    points = [2 * i for i in range(5, 16)]
    graph = window['graph']
    graph.erase()

    # Get graph size
    graph_width, graph_height = graph.CanvasSize
    row_delta = graph_height // len(points)
    for i, pt in enumerate(points):
        i += 1
        px = pt_to_px(pt)
        graph.draw_text(text='M', location=(0, i * row_delta), font=f'Courier {pt}')
        start_px, end_px = (-px/2, i * row_delta + pt), (px/2, i * row_delta + pt)
        start_pt, end_pt = (-pt/2, i * row_delta - pt), (pt/2, i * row_delta - pt)
        graph.draw_line(start_pt, end_pt)
        graph.draw_line(start_px, end_px)




graph_height = 10_000
rows_per_pt = [416, 350, 317, 277, 246, 229, 208, 190, 179, 166]
points = [2 * i for i in range(6, 16)]
for i, pt in enumerate(points):
    px = pt_to_px(pt)
    row_pixel_height = graph_height / rows_per_pt[i]
    print(f"{pt = },  {px = },  {row_pixel_height = }")

layout = [
        [sg.Button('Go')],
        [sg.Graph(canvas_size=(800, 800),
                  graph_bottom_left=(-400, 800),
                  graph_top_right=(400, 0),
                  key='graph', background_color='lavender')],
        [sg.Button('Exit')]
    ]

def main():
    sg.theme('Default1')

    window = sg.Window('Graph with Origin at Center', layout, resizable=True, grab_anywhere=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        elif event == 'Go':
            update_graph(window, values)

    window.close()

if __name__ == '__main__':
    main()
