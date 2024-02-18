import PySimpleGUI as sg
import time


def draw_line(canvas, start_point, end_point):
    canvas.draw_line(start_point, end_point, color='blue')


layout = [
    [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), background_color='white',
              key='graph')],
    [sg.Button('Exit')]
]

window = sg.Window('Draw Line Every Second', layout, finalize=True)
graph = window['graph']

while True:
    event, values = window.read(timeout=60)  # Wait for 1000 milliseconds (1 second)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # Calculate new line points
    start_point = (5 + time.time() % 400, 0)
    end_point = (5 + time.time() % 400, 400)

    # Clear the graph before drawing a new line
    graph.erase()

    # Draw the line
    draw_line(graph, start_point, end_point)

window.close()
