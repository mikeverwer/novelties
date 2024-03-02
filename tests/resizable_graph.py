import PySimpleGUI as sg
import time

sieve_graph_layout = [
    sg.Graph((500, 500), (0, 500), (500, 0),
             background_color='white', key='sieve graph', expand_y=True, float_values=True)
]

sieve_layout = [
    [sg.Text('The Sieve of Eratosthenes', font=('Helvetica', 16))],
    [sg.Text('To which number shall we search?', font=('Helvetica', 12))],
    [sg.Input(key='sieve input', size=(10, 1)), sg.Button('Go!')],
    [sg.Column(
        layout=[
            [sg.Stretch(), *sieve_graph_layout, sg.Stretch()]
        ],
        scrollable=True, vertical_scroll_only=True, size=(500, 200), key='sieve column', expand_y=True)
    ]
]
animate = False
i = 0
window = sg.Window('Sieve of Eratosthenes', sieve_layout, resizable=True, finalize=True)

window.set_min_size(window.size)

while True:
    event, values = window.read(timeout=250)

    if event == sg.WIN_CLOSED:
        break

    elif event == 'Go!':
        graph = window['sieve graph']
        text_string_list = '2 3 5 7 11 13 17 19 23'.split()
        for i, item in enumerate(text_string_list):
            graph.draw_text(item, ((1 + (i % 5)) * 25, (1 + (i // 5)) * 25), font=('Helvetica', 14))
        graph.draw_line((1, 50), (490, 50), 'black')
        graph.draw_line((10, 100), (20, 100), 'black', width=1)

        animate = True

    while event == sg.TIMEOUT_EVENT and animate and i < 10:
        graph = window['sieve graph']
        graph.draw_line((100, 100 + i), (110, 100 + i))
        i += 1

window.close()
