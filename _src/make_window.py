import usefull_prints as uprint
from main_gui import sg, primes_so_far, primes_for_display


def make_window(theme='Default1', sieve_graph_x=1000, sieve_graph_y=1000):
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
                                    [sg.Text('primes list:')], [sg.T(primes_for_display)],
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
                 background_color='lavender', key='sieve graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]

    sieve_layout = [
        [sg.Column(layout=[
                [sg.Text('The Sieve of Eratosthenes', font=('Helvetica', 18, 'bold'))],
                [sg.Text('To which number shall we search?', font=('Helvetica', 16))]]), sg.T('', s=(16, 1)),
            sg.Column(layout=[
            [sg.Frame(layout=[[sg.T('Values:        \nPrime Factors: ', k='sieve value display',
                                    font='Helvetica 14 bold', background_color='lavender', text_color='black')]],
                      title='', background_color='lavender', )],
            ])
        ]
    ]

    sieve_layout += [[sg.Column(layout=[
        [sg.T(''), sg.Input(key='sieve input', size=(10, 1), default_text='200'),
         sg.Button('  Begin  ', font='bold', key='go-sieve', button_color='sea green'),
         sg.Button('Clear', font='bold', k='clear sieve', button_color='firebrick3'),
         sg.Button('Pause/Play', font='bold', k='pause sieve', button_color='gray50'),
         sg.T('', s=(2, 1)), sg.T('    Set Speed: ', font='Helvetica 14'),
         sg.Button('0.25x', k='sieve_speed:0.25'), sg.Button('0.5x ', k='sieve_speed:0.5'),
         sg.Button('  1x  ', k='sieve_speed:1'), sg.Button('  2x  ', k='sieve_speed:2'),
         sg.Button('  4x  ', k='sieve_speed:4'), sg.Button('  8x  ', k='sieve_speed:8'),
         sg.T('', s=(2, 1)), sg.T('    Size:', font='Helvetica 14'),
         sg.DropDown(([2 * i + 10 for i in range(15)]), size=(4, 1), default_value=14, k='sieve_font',
                     enable_events=True, readonly=True),
         ]
    ]),
    ],
    ]

    sieve_layout += [[sg.Column(
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
                      auto_refresh=True)]
    ]

    placeholder_layout = [[sg.T('placeholder tab!')],
                          [sg.Image(data=sg.DEFAULT_BASE64_ICON, k='-IMAGE-')],
                          [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-'),
                           sg.Button('Test Progress bar')]]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              ]

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
