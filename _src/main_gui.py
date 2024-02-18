import generate_novelties
import sieve_of_eratosthenes as soe
import usefull_prints as uprint
import PySimpleGUI as sg

primes = soe.primes_up_to_100()
primes_for_display = uprint.column_print(primes, 10, True)

def make_window(theme='Default1'):
    global primes
    sg.theme(theme)
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing', 'More Nothing', 'Exit']]

    novelty_column = [sg.Multiline(
        primes_for_display,
        size=(45, 200), expand_x=True, expand_y=False, k='novelty output', font=('Helvetica', 14), write_only=True,
        enable_events=False),
    ]

    novelties_layout = [[sg.Text("Enter the largest natural number to reach: ")],
                        [sg.Input(key='max novelty', size=(10, 1), default_text='250'),
                         sg.Button('Show', key='generate novelties')],
                        [sg.Pane([
                            sg.Col([[sg.T('Largest Known Prime: ##')],
                                    [sg.Text('primes list:'), sg.T(primes_for_display)],
                                    ]),
                            sg.Column(
                                layout=[
                                    [sg.Stretch(), *novelty_column, sg.Stretch()]
                                ],
                                scrollable=True, vertical_scroll_only=False, size=(50, 200), key='novelty output',
                                expand_y=True),
                        ], size=(50, 200), orientation='h', expand_y=True, expand_x=True)],
                        ]

    sieve_graph_layout = [
        sg.Graph((1000, 1000), (0, 1000), (1000, 0),
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
            scrollable=True, vertical_scroll_only=True, size=(1000, 500), key='sieve column', expand_y=True)
        ]
    ]

    asthetic_layout = [[sg.T('Anything that you would use for asthetics is in this tab!')],
                       [sg.Image(data=sg.DEFAULT_BASE64_ICON, k='-IMAGE-')],
                       [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-'),
                        sg.Button('Test Progress bar')]]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              [sg.Stretch(), sg.Text('All Things Prime', size=(38, 1), justification='center', font=("Helvetica", 16),
                                     relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True), sg.Stretch()]]

    layout += [[sg.TabGroup([[sg.Tab('Sieve', sieve_layout),
                              sg.Tab('progress bar', asthetic_layout),
                              sg.Tab('The Novelties', novelties_layout)
                              ]], key='-TAB GROUP-', expand_x=True, expand_y=True
                            ),
                ]]

    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Primes and Novelties', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       use_custom_titlebar=True, finalize=True, keep_on_top=True)
    window.set_min_size(window.size)
    return window


def main():
    window = make_window(sg.theme())

    # This is an Event Loop
    while True:
        event, values = window.read(timeout=1)
        # keep an animation running so show things are happening
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        if event == 'Test Progress bar':
            print("[LOG] Clicked Test Progress Bar!")
            progress_bar = window['-PROGRESS BAR-']
            for i in range(100):
                print("[LOG] Updating progress bar by 1 step (" + str(i) + ")")
                progress_bar.update(current_count=i + 1)
            print("[LOG] Progress bar complete!")

    window.close()
    exit(0)


if __name__ == "__main__":
    main()
