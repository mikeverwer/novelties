import generate_novelties
import sieve_of_eratosthenes as soe
import usefull_prints as uprint
import colours
import PySimpleGUI as sg
import time
import random

colours_list = colours.list_colour_names()
colours_dict = colours.dict_colours()
primes = soe.primes_up_to_100()

em_12 = 16
em_14 = 18.66666667
em_16 = 21.33333333
em_18 = 24
sieve_graph_x = 1000
sieve_graph_y = 20000
update_interval = 1
sieve_font = 'Courier 14'

primes_for_display = uprint.column_print(primes, 10, True)
sieve_animation_steps = {'find coordinates': False,
                         'draw numbers': False,
                         'box prime': False,
                         'scratch multiple': False,
                         'finished': False,
                         'hurry up': None
                         }
sieve_value_coord = {}
sieve_isprime = {}
animate_sieve = False
primes_so_far = ['None']
scratch_animation_passes = int
animation_speed_sieve = 1


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
                 background_color='lavender', key='sieve graph', expand_y=True)  # colour AliceBlue
    ]

    sieve_layout = [
        [sg.Text('The Sieve of Eratosthenes', font=('Helvetica', 18, 'bold'))],
        [sg.Text('To which number shall we search?', font=('Helvetica', 16))],
        [sg.T(''), sg.Input(key='sieve input', size=(10, 1), default_text='200'),
         sg.Button('  Begin  ', font='bold', key='go-sieve', button_color='sea green'),
         sg.Button('Clear', font='bold', k='clear sieve', button_color='firebrick3'),
         sg.Button('Pause/Play', font='bold', k='pause sieve', button_color='gray50'),
         sg.T('    Set Speed: ', font='Helvetica 14'),
         sg.Button('0.25x', k='sieve_speed:0.25'), sg.Button('0.5x ', k='sieve_speed:0.5'),
         sg.Button('  1x  ', k='sieve_speed:1'), sg.Button('  2x  ', k='sieve_speed:2'),
         sg.Button('  4x  ', k='sieve_speed:4'), sg.Button('  8x  ', k='sieve_speed:8'),
         sg.T('    Size:', font='Helvetica 14'),
         sg.DropDown((10, 12, 14, 16, 18), default_value=14, k='sieve_font', enable_events=True, readonly=True)
         ],
        [sg.Column(
            layout=[
                [sg.Stretch(), *sieve_graph_layout, sg.Stretch()]
            ],
            scrollable=True, vertical_scroll_only=True, size=(sieve_graph_x, 500), key='sieve column', expand_y=True),
            sg.Column(
                layout=[
                    [sg.Text('Primes found so far:', font='Helvetica 16'), sg.T('')],
                    [sg.Text(uprint.column_print(primes_so_far, 5, string=True), key='found primes',
                             font='Courier 12 bold', expand_x=True, size=(200, 100))]
                ],
                expand_x=True, expand_y=True, vertical_scroll_only=True, scrollable=True, size=(215, 500))
        ]
    ]

    log_layout = [
        [sg.Text('Log:', font='Helvetica 16')],
        [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                      auto_refresh=True)],
        [sg.T("Butts")]
    ]

    placeholder_layout = [[sg.T('placeholder tab!')],
                          [sg.Image(data=sg.DEFAULT_BASE64_ICON, k='-IMAGE-')],
                          [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-'),
                           sg.Button('Test Progress bar')]]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              [sg.Stretch(), sg.Text('All Things Prime', size=(38, 1), justification='center', font=("Helvetica", 16),
                                     relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=True), sg.Stretch()]]

    layout += [[sg.TabGroup([[sg.Tab('Sieve', sieve_layout),
                              sg.Tab('progress bar', placeholder_layout),
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


def reset_globals():
    global update_interval
    global animation_speed_sieve
    global sieve_animation_steps
    global primes_so_far
    global sieve_value_coord
    global sieve_isprime
    global scratch_animation_passes

    sieve_animation_steps = {'find coordinates': False,
                             'draw numbers': False,
                             'box prime': False,
                             'prime colour': '',
                             'scratch multiple': False,
                             'finished': False,
                             'hurry up': None
                             }
    sieve_value_coord = {}
    sieve_isprime = {}
    primes_so_far = []
    scratch_animation_passes = 0
    animation_speed_sieve = 1


def sieve_animation(window, values, em=em_12):
    graph = window['sieve graph']
    global update_interval
    global animation_speed_sieve
    global sieve_animation_steps
    global primes_so_far
    global sieve_value_coord
    global sieve_isprime
    global scratch_animation_passes

    def choose_colour(seed):

        def is_bright_color(hex_code):
            # Convert hex code to RGB values
            r = int(hex_code[1:3], 16) / 255.0
            g = int(hex_code[3:5], 16) / 255.0
            b = int(hex_code[5:7], 16) / 255.0

            # Calculate luminance
            luminance = (0.2126 * r) + (0.587 * g) + (0.0722 * b)

            # Define a threshold for brightness (adjust as needed)
            brightness_threshold = 0.2

            print(luminance)

            # Return True if the color is considered bright, False otherwise
            return luminance > brightness_threshold

        # colour_name = random.choice(colours_list)  # colour is random each run
        colour_name = colours_list[(int(seed) * 100) % len(colours_list)]  # colour tied to prime
        colour_hex = colours_dict[colour_name]
        attempts = 1  # ensure the colour is "appropriate"
        print(f"attempt: {attempts},  colour: {colour_name}  :  {colour_hex}")
        while is_bright_color(colour_hex):
            attempts += 1
            # colour_name = random.choice(colours_list)  # colour is random each run
            colour_name = colours_list[(int(seed) ** (attempts * 2)) % len(colours_list)]  # colour tied to prime
            colour_hex = colours_dict[colour_name]
            print(f"attempt: {attempts},  colour: {colour_name}  :  {colour_hex}")
            if attempts > 5:  # limit attempts
                colour_name = random.choice(colours_list)  # colour is random each run
                colour_hex = colours_dict[colour_name]

        return colour_name

    def draw_box(thing):
        # choose colour
        sieve_animation_steps['prime colour'] = choose_colour(int(thing))
        box_colour = sieve_animation_steps['prime colour']

        # get geometry
        bottom_left = (
            sieve_value_coord[thing][0] - (len(str(thing)) * em / 2), sieve_value_coord[thing][1] - (em / 2))
        bottom_right = (
            sieve_value_coord[thing][0] + (len(str(thing)) * em / 2), sieve_value_coord[thing][1] - (em / 2))
        top_left = (
            sieve_value_coord[thing][0] - (len(str(thing)) * em / 2), sieve_value_coord[thing][1] + (em / 2))
        top_right = (
            sieve_value_coord[thing][0] + (len(str(thing)) * em / 2), sieve_value_coord[thing][1] + (em / 2))

        # draw
        graph.draw_line(bottom_left, bottom_right, box_colour, width=2)
        graph.draw_line(bottom_left, top_left, box_colour, width=2)
        graph.draw_line(top_right, top_left, box_colour, width=2)
        graph.draw_line(top_right, bottom_right, box_colour, width=2)

    def draw_scratch(word, line_colour=sieve_animation_steps['prime colour']):
        # find draw height
        center = sieve_value_coord[scratch]
        length = len(str(scratch)) * em - (em * len(str(scratch)) % 2)
        bump = int(em / 6) + 1  # decent approximation?
        # generate the sequence: [0, bump, -bump, 2bump, -2bump, ..., nbump, -nbump] where nbump < em / 2
        # sequence is used to handle the gap becoming too large, so we cycle through the sequence in that case
        h_offsets = [(((-1) ** (i - 1)) * (bump * ((i + 1) // 2))) for i in range((int(em) + 1) // 2)]  #
        h_offset = h_offsets[(len(primes_so_far) - 1) % len(h_offsets)]
        height = center[1] + h_offset
        graph.draw_line((sieve_value_coord[scratch][0] - (length / 2), height),
                        (sieve_value_coord[scratch][0] + (length / 2), height), line_colour, width=2)

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
            graph.draw_text(str(number), sieve_value_coord[number], font=sieve_font)
        # move to next step
        sieve_animation_steps['box prime'] = True
        sieve_animation_steps['draw numbers'] = False

    elif sieve_animation_steps['box prime']:
        # find prime
        if True in sieve_isprime:
            prime = sieve_isprime.index(True) + 2
            if prime >= int(values['sieve input']) ** 0.5:
                if sieve_animation_steps['hurry up'] is None:
                    choice = sg.popup('\nWe have reached a point where the only remaining numbers are prime.\n\n'
                                      'Fast forward to the end?\n', title='',
                                      custom_text=('Yes, please.', 'No, thanks.'),
                                      keep_on_top=True)
                    sieve_animation_steps['hurry up'] = True if choice == 'Yes, please' else False
                    if choice == 'Yes, please.':
                        sieve_animation_steps['hurry up'] = True
                    elif choice == 'No, thanks.':
                        sieve_animation_steps['hurry up'] = False
                    print(f"user chose: {choice}  :  hurry up = {sieve_animation_steps['hurry up']}")
            if prime <= int(values['sieve input']):
                print(f"[LOG] Prime Found {prime}. Drawing box.")
                sieve_isprime[prime - 2] = False
                primes_so_far.append(prime)
                window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
                draw_box(prime)

                # move to next step
                if sieve_animation_steps['hurry up'] is None:  # still need to scratch
                    sieve_animation_steps['box prime'] = False  # start scratching
                    sieve_animation_steps['scratch multiple'] = True
                    scratch_animation_passes = 0
                    update_interval = 1 * animation_speed_sieve  # set speed for next phase
                elif sieve_animation_steps['hurry up']:  # scratching is done
                    print(f"[LOG] hurry up")
                    sieve_animation_steps['box prime'] = False  # finish quickly
                else:  # continue drawing boxes
                    sieve_animation_steps['box prime'] = True

            else:
                # move to next step
                sieve_animation_steps['box prime'] = False
                sieve_animation_steps['finished'] = True

        else:  # no primes left to find, finish
            print(f"[LOG] Nothing left to box.")
            # move to next step
            sieve_animation_steps['box prime'] = False
            sieve_animation_steps['finished'] = True

    elif sieve_animation_steps['scratch multiple']:
        prime = primes_so_far[-1]
        # choose colour
        colour = colours_list[(prime * 100) % len(colours_list)]
        # find number to scratch
        scratch = (prime ** 2) + (scratch_animation_passes * prime)
        if scratch <= int(values['sieve input']):
            print(f"[LOG] Scratch Multiple: {scratch}")
            sieve_isprime[scratch - 2] = False
            draw_scratch(scratch)

            # move to next step - scratching complete
            if scratch + prime <= int(values['sieve input']):  # scratch another
                sieve_animation_steps['scratch multiple'] = True
                scratch_animation_passes += 1
                update_interval = 75 * animation_speed_sieve
            else:
                sieve_animation_steps['scratch multiple'] = False  # move to next prime
                sieve_animation_steps['box prime'] = True
                update_interval = 1 * animation_speed_sieve

        else:
            # move to next step - no scratching needed
            sieve_animation_steps['scratch multiple'] = False  # move to next prime
            sieve_animation_steps['box prime'] = True
            update_interval = 1 * animation_speed_sieve

    elif sieve_animation_steps['hurry up']:
        for i, isprime in enumerate(sieve_isprime):
            if isprime:
                draw_box(i + 2)
                sieve_isprime[i] = False
                primes_so_far.append(i + 2)
        window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
        # move to next step - finished
        sieve_animation_steps['hurry up'] = False
        sieve_animation_steps['finished'] = True


def main():
    window = make_window(sg.theme(), sieve_graph_x, sieve_graph_y)
    sieve_graph = window['sieve graph']
    global animate_sieve
    global animation_speed_sieve
    global primes_so_far
    global sieve_font
    text_height = em_12

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
            columns = 900 // (sieve_column_width * text_height)
            rows = (max_sieve // columns) + 1
            primes_so_far = []
            reset_globals()
            # check graph size, remake if too small
            if rows <= (sieve_graph_y // text_height) + text_height:  # enough rows
                sieve_graph.erase()
                sieve_animation_steps['finished'] = False
                animate_sieve = True
                sieve_animation_steps['find coordinates'] = True
            else:
                # event = sg.popup('Warning', 'Will reset the window.', keep_on_top=True, grab_anywhere=True)
                event = sg.popup('This will cause the window to reset.\n\nContinue?\n', title='Warning',
                                 custom_text=('Continue', 'Cancel'), keep_on_top=True)

                print(f'button: {event}')
                print((sieve_graph_y // text_height) + text_height)
                if event == 'Continue':
                    window.close()
                    window = make_window(sg.theme(), sieve_graph_y=sieve_graph_y)

        elif event.startswith('sieve_speed:'):
            speed = event.split(':')[1]
            animation_speed_sieve = float(speed)

        elif event == 'sieve_font':
            print("[LOG] Clicked Font Size")
            sieve_font = 'Courier ' + str(values[event])
            text_height = round((values[event] / 72) * 96)  # calculate text size in pixels

        elif event == 'pause sieve':
            print("[LOG] Clicked Pause/Play")
            animate_sieve = not animate_sieve

        elif event == 'clear sieve':
            print("[LOG] Clicked Clear.")
            animate_sieve = False
            sieve_graph.erase()

        elif event == 'OK':
            print("[LOG] Rebuild the window.")
            window.close()
            window = make_window(sg.theme(), sieve_graph_y=sieve_graph_y)

        if animate_sieve:
            print('[LOG] Animation Pass')
            sieve_animation(window, values, em=text_height)
            if sieve_animation_steps['finished']:
                animate_sieve = False

    window.close()
    exit(0)


if __name__ == "__main__":
    main()
