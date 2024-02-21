import generate_novelties
import sieve_of_eratosthenes as soe
import usefull_prints as uprint
import colours
import PySimpleGUI as sg
import time

colours = colours.colours()
primes = soe.primes_up_to_100()
primes_for_display = uprint.column_print(primes, 10, True)
sieve_value_coord = {}
sieve_isprime = {}
sieve_current_value = 2
em_12 = 16
update_interval = 1
animate_sieve = False
primes_so_far = ['None']
scratch_animation_passes = 1
sieve_graph_x = 1000
sieve_graph_y = 20000


def make_window(theme='Default1', sieve_graph_x=1000, sieve_graph_y=1000):
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
        sg.Graph((sieve_graph_x, sieve_graph_y), (0, sieve_graph_y), (sieve_graph_x, 0),
                 background_color='white', key='sieve graph', expand_y=True)
    ]

    sieve_layout = [
        [sg.Text('The Sieve of Eratosthenes', font=('Helvetica', 16))],
        [sg.Text('To which number shall we search?', font=('Helvetica', 12))],
        [sg.Input(key='sieve input', size=(10, 1), default_text='200'), sg.Button('Go!', key='go-sieve'),
         sg.Button('Pause', k='pause sieve')],
        [sg.Column(
            layout=[
                [sg.Stretch(), *sieve_graph_layout, sg.Stretch()]
            ],
            scrollable=True, vertical_scroll_only=True, size=(sieve_graph_x, 500), key='sieve column', expand_y=True),
         sg.Column(
             layout=[
                 [sg.Text('Primes found so far:', font='Helvetica 16')],
                 [sg.Text(uprint.column_print(primes_so_far, 5, string=True), key='found primes',
                          font='Courier 12', expand_x=False)]
             ],
         expand_x=False, vertical_scroll_only=True)
        ]
    ]

    log_layout = [
        [sg.Text('Log:', font='Helvetica 16')],
        [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                      auto_refresh=True)]
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
                              sg.Tab('The Novelties', novelties_layout),
                              sg.Tab('Log', log_layout)
                              ]], key='-TAB GROUP-', expand_x=True, expand_y=True
                            ),
                ]]

    # layout[-1].append(sg.Sizegrip())
    window = sg.Window('Primes and Novelties', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       finalize=True, keep_on_top=True)
    window.set_min_size(window.size)
    return window


sieve_animation_steps = {'find coordinates': False,
                         'draw numbers': False,
                         'box prime': False,
                         'scratch multiple': False,
                         'finished': False
                         }


def sieve_animation(window, values, sieve_passes: int | float, em=em_12):
    graph = window['sieve graph']
    global update_interval
    global sieve_animation_steps
    global primes_so_far
    global sieve_value_coord
    global sieve_isprime
    global sieve_current_value
    global scratch_animation_passes

    if sieve_animation_steps['find coordinates']:
        max_sieve = int(values['sieve input'])
        sieve_column_width = len(str(max_sieve)) + 2
        columns = 900 // (sieve_column_width * em)
        # rows = (max_sieve // columns) + 1
        numbers = [i for i in range(2, max_sieve + 1)]
        sieve_value_coord = {}
        sieve_isprime = [True] * len(numbers)

        for index, number in enumerate(numbers):
            row = index // columns + 1
            column = index % columns + 1
            sieve_value_coord[number] = (column * (sieve_column_width * em), row * 1.5 * em)

        # move to next step
        sieve_animation_steps['find coordinates'] = False
        sieve_animation_steps['draw numbers'] = True
        print('[LOG] Coordinates found.')

    elif sieve_animation_steps['draw numbers']:
        print('[LOG] Drawing numbers.')
        for number in sieve_value_coord:
            graph.draw_text(str(number), sieve_value_coord[number], font='Courier 12')
        sieve_animation_steps['box prime'] = True
        sieve_animation_steps['draw numbers'] = False

    elif sieve_animation_steps['box prime']:
        # find prime
        if True in sieve_isprime:
            prime = sieve_isprime.index(True) + 2
            update_interval = 25 if prime > int(values['sieve input']) ** 0.5 else 1
            if prime <= int(values['sieve input']):
                print(f"[LOG] Prime Found {prime}. Drawing box.")
                sieve_isprime[prime - 2] = False
                primes_so_far.append(prime)
                window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
                # choose colour
                colour = colours[(prime * 100) % len(colours)]
                bottom_left = (sieve_value_coord[prime][0] - (len(str(prime)) * em / 2), sieve_value_coord[prime][1] - (em / 2))
                bottom_right = (sieve_value_coord[prime][0] + (len(str(prime)) * em / 2), sieve_value_coord[prime][1] - (em / 2))
                top_left = (sieve_value_coord[prime][0] - (len(str(prime)) * em / 2), sieve_value_coord[prime][1] + (em / 2))
                top_right = (sieve_value_coord[prime][0] + (len(str(prime)) * em / 2), sieve_value_coord[prime][1] + (em / 2))
                graph.draw_line(bottom_left, bottom_right, colour)
                graph.draw_line(bottom_left, top_left, colour)
                graph.draw_line(top_right, top_left, colour)
                graph.draw_line(top_right, bottom_right, colour)

                # move to next step
                sieve_animation_steps['box prime'] = False
                scratch_animation_passes = 0
                sieve_animation_steps['scratch multiple'] = True
            else:
                sieve_animation_steps['box prime'] = False
                sieve_animation_steps['finished'] = True

        else:
            sieve_animation_steps['box prime'] = False
            sieve_animation_steps['finished'] = True

    elif sieve_animation_steps['scratch multiple']:
        update_interval = 75  # speed up animation
        prime = primes_so_far[-1]
        # choose colour
        colour = colours[(prime * 100) % len(colours)]
        # find number to scratch
        scratch = (prime ** 2) + (scratch_animation_passes * prime)
        if scratch <= int(values['sieve input']):
            print(f"[LOG] Scratch Multiple: {scratch}")
            sieve_isprime[scratch - 2] = False
            # find draw height
            center = sieve_value_coord[scratch]
            length = len(str(scratch)) * em
            # bump = sieve_passes // em
            bump = 2
            h_offsets = [(((-1) ** (i - 1)) * (bump * ((i + 1) // 2))) for i in range((em // 2) + 1)]
            h_offset = h_offsets[(len(primes_so_far) - 1) % len(h_offsets)]
            height = center[1] + h_offset
            graph.draw_line((sieve_value_coord[scratch][0] - (length / 2), height),
                            (sieve_value_coord[scratch][0] + (length / 2), height), colour)

            # move to next step
            if scratch + prime <= int(values['sieve input']):  # scratch another
                sieve_animation_steps['scratch multiple'] = True
                scratch_animation_passes += 1
            else:
                sieve_animation_steps['scratch multiple'] = False  # move to next prime
                sieve_animation_steps['box prime'] = True
                update_interval = 1

        else:
            sieve_animation_steps['scratch multiple'] = False  # move to next prime
            sieve_animation_steps['box prime'] = True
            update_interval = 1



def main():
    window = make_window(sg.theme(), sieve_graph_x, sieve_graph_y)
    sieve_graph = window['sieve graph']
    global animate_sieve
    global primes_so_far

    # This is an Event Loop
    while True:
        event, values = window.read(timeout=1000 // update_interval)
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
                if time.time() % 100 == 0:
                    print("[LOG] Updating progress bar by 1 step (" + str(i) + ")")
                    progress_bar.update(current_count=i + 1)
            print("[LOG] Progress bar complete!")

        elif event == 'go-sieve':
            max_sieve = int(values['sieve input'])
            sieve_column_width = len(str(max_sieve)) + 2
            columns = 900 // (sieve_column_width * em_12)
            rows = (max_sieve // columns) + 1
            _, required_passes, _ = soe.fast_sieve(max_sieve, get_checks=True)
            primes_so_far = []
            # check graph size, remake if too small
            if rows <= (sieve_graph_y // em_12) + em_12:  # enough rows
                sieve_graph.erase()
                sieve_animation_steps['finished'] = False
                animate_sieve = True
                sieve_animation_steps['find coordinates'] = True
            else:
                # event = sg.popup('Warning', 'Will reset the window.', keep_on_top=True, grab_anywhere=True)
                event = sg.popup('This will cause the window to reset.\n\nContinue?\n', title='Warning',
                                 custom_text=('Continue', 'Cancel'), keep_on_top=True)

                print(f'button: {event}')
                print((sieve_graph_y // em_12) + em_12)
                if event == 'Continue':
                    window.close()
                    window = make_window(sg.theme(), sieve_graph_y=sieve_graph_y)

        elif event == 'pause sieve':
            animate_sieve = not animate_sieve

        elif event == 'OK':
            print("[LOG] Rebuild the window.")
            window.close()
            window = make_window(sg.theme(), sieve_graph_y=sieve_graph_y)

        if animate_sieve:
            print('[LOG] Animation Pass')
            sieve_animation(window, values, required_passes, em_12)
            if sieve_animation_steps['finished']:
                animate_sieve = False

    window.close()
    exit(0)


if __name__ == "__main__":
    main()
