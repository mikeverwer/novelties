import PySimpleGUI as sg

sieve_graph_layout = [
    sg.Graph((500, 500), (0, 500), (500, 0),
             background_color='white', key='sieve graph', expand_y=True)
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

window = sg.Window('Sieve of Eratosthenes', sieve_layout, resizable=True, finalize=True)

window.set_min_size(window.size)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'Go!':
        graph = window['sieve graph']
        graph.draw_text('2 3 5 7 11 13 17 19 23')

window.close()