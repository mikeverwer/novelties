import generate_novelties
import sieve_of_eratosthenes
import usefull_prints
import PySimpleGUI as sg


def make_window(theme='Default1'):
    sg.theme(theme)
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing', 'More Nothing', 'Exit']]

    sieve_graph_layout = [
        sg.Graph((500, 500), (0, 500), (500, 0),
                 background_color='white', key='sieve graph')
    ]

    sieve_layout = [
        [sg.Text('The Sieve of Eratosthenes', font=('Helvetica', 16))],
        [sg.Text('To which number shall we search?', font=('Helvetica', 12))],
        [sg.Input(key='sieve input', size=(10, 1)), sg.Button('Go!')],
        [sg.Column(
            layout=[
                [sg.Stretch(), *sieve_graph_layout, sg.Stretch()]
            ],
            scrollable=True, vertical_scroll_only=True, size=(500, 200), key='sieve column')
        ]
    ]

    asthetic_layout = [[sg.T('Anything that you would use for asthetics is in this tab!')],
                       [sg.Image(data=sg.DEFAULT_BASE64_ICON, k='-IMAGE-')],
                       [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-'),
                        sg.Button('Test Progress bar')]]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              [sg.Text('All Things Prime', size=(38, 1), justification='center', font=("Helvetica", 16),
                       relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True)]]

    layout += [[sg.TabGroup([[sg.Tab('Sieve', sieve_layout),
                              sg.Tab('progress bar', asthetic_layout),
                              ]],  key='-TAB GROUP-', expand_x=True, expand_y=True
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
