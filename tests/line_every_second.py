import colours
import PySimpleGUI as sg
import time
import random


def draw_line(graph):
    start_point = (random.randint(10, 390), random.randint(10, 390))
    end_point = (random.randint(10, 390), random.randint(10, 390))
    colour = random.choice(colours.colours())
    graph.draw_line(start_point, end_point, color=colour)


layout = [[sg.Button('Go'), sg.Button('Pause'), sg.Button('Clear'),
           sg.T('Speed: '), sg.Button('1x'), sg.Button('2x'), sg.Button('4x'), sg.Button('8x')],
          [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400),
                    background_color='white', key='-GRAPH-')],
          [sg.Button('Exit')]]

window = sg.Window('Draw Line Example', layout, finalize=True)
graph = window['-GRAPH-']

animate = False
update_interval = 1  # update every 1 second

while True:
    event, values = window.read(timeout=1000 // update_interval)

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    if event == 'Clear':
        # Erase previous drawings on the graph
        graph.erase()

    if event == 'Go':
        animate = True

    if event == 'Pause':
        animate = False

    if event == '1x':
        update_interval = 1

    if event == '2x':
        update_interval = 2

    if event == '4x':
        update_interval = 4

    if event == '8x':
        update_interval = 8

    if animate:
        # randomize points

        # Draw the line on the graph
        draw_line(graph)

window.close()
