import colours
import PySimpleGUI as sg
import time
import random


def draw_line(graph, start_point, end_point):
    graph.draw_line(start_point, end_point, color='black')


layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400),
                    background_color='white', key='-GRAPH-')],
          [sg.Button('Exit')]]

window = sg.Window('Draw Line Example', layout, finalize=True)
graph = window['-GRAPH-']

start_point = (50, 50)
end_point = (150, 150)
update_interval = 1  # update every 1 second

while True:
    event, values = window.read(timeout=1000 // update_interval)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # Erase previous drawings on the graph
    # graph.erase()

    # randomize points
    start_point = (random.randint(10, 390), random.randint(10, 390))
    end_point = (random.randint(10, 390), random.randint(10, 390))

    # Draw the line on the graph
    draw_line(graph, start_point, end_point)

window.close()
