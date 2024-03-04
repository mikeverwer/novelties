import usefull_prints as uprint
from main_gui import sg, primes_so_far


def make_window(theme='Default1', sieve_graph_x=1000, sieve_graph_y=1000, novelty_graph_x=1000, novelty_graph_y=1000):
    sg.theme(theme)
    menu_def = [['&Application', ['E&xit']],
                ['&Help', ['&About']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing', 'More Nothing', 'Exit']]

# Beginning of Novelties Layout
    novelty_graph_layout = [
        sg.Graph((novelty_graph_x, novelty_graph_y), (0, novelty_graph_y), (novelty_graph_x, 0),
                 background_color='lavender', key='novelty graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]

    novelty_graph_column = sg.Column(layout=[
            [sg.Stretch(), *novelty_graph_layout, sg.Stretch()]
        ], scrollable=True, size=(novelty_graph_x, 500), key='novelty column', expand_y=True, expand_x=True
    )
    
    conversion_chart_column = sg.Column(layout=[
            [sg.Text('Ordinal to Prime Conversion Chart:')], [sg.Multiline('', key='conversion chart', font='Courier 12 bold', expand_x=True, expand_y=True, write_only=True, auto_size_text=True)],
        ], expand_x=True, expand_y=True, vertical_scroll_only=True, scrollable=True, size_subsample_width=2, visible=True
    )

    left_column = sg.Column(layout=[
            [sg.Text(' The Novelties ', font='Helvetica 18 bold', pad=(5,15), relief='raised', border_width=5)],
            [sg.Text("Enter the largest natural number to reach: ")],
            [sg.Input(key='novelty input', size=(10, 1), default_text='250'), sg.Button('Show', key='generate novelties')],
            [sg.Button('Show Chart', k='-SHOW CHART-')],
            [sg.pin(conversion_chart_column)]
        ], expand_x=True
    )

    novelties_layout = [
        [left_column, sg.Stretch(), novelty_graph_column],
    ]
    
# Beginning of Sieve Layout
    sieve_graph_layout = [
        sg.Graph((sieve_graph_x, sieve_graph_y), (0, sieve_graph_y), (sieve_graph_x, 0),
                 background_color='lavender', key='sieve graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]
    
    sieve_size_selection_layout = [
        [sg.T('Text Size ', font='Helvetica 10 bold')], 
        [sg.DropDown(([2 * i + 10 for i in range(15)]), size=(4, 1), default_value=14, k='sieve font', enable_events=True, readonly=True)],
        [sg.T('')]
    ]
    
    fbc = 'lavender'  # frame background colour
    sieve_interact_display_frame = sg.Frame(layout=[
            [sg.T('Value:'.ljust(20), k='sieve clicked value', font='Helvetica 14 bold', background_color=fbc, text_color='black')],
            [sg.T('Prime Factors:'.ljust(20), k='sieve clicked primes', font='Helvetica 14 bold', background_color=fbc, text_color='black')]
            ],
                title='', background_color='lavender', relief='solid', vertical_alignment='bottom')
    
    
    tick_positions = ['1/4', '1/2', '1', '2', '4', '8', '16', ' 32']
    speed_slider_layout = [
        [sg.Text("Set Animation Speed:", font='Helvetica 10 bold')],
        [sg.Slider(range=(0.25, 7), orientation="h", size=(32, 20), default_value=2, key="sieve speed", enable_events=True, disable_number_display=True)],  # 4, 32
        [sg.Text(f"{tick_positions[i]}x".center(4), background_color='lavender', text_color='black') for i in range(len(tick_positions))],
    ]


    sieve_in_go_clear_pause_layout = [
        [sg.Text('  To which number shall we search?', font=('Helvetica', 16))],
        [sg.T(''), sg.Input(key='sieve input', size=(10, 1), default_text='200'),
         sg.Button('  Begin  ', font='bold', key='go-sieve', button_color='sea green'),
         sg.Button('Clear', font='bold', k='clear sieve', button_color='firebrick3'),
         sg.Button('Pause/Play', font='bold', k='pause sieve', button_color='gray50'),
        ]
    ]

    sieve_layout = [
        [sg.Text(' The Sieve of Eratosthenes ', font=('Helvetica', 18, 'bold'), relief='raised', border_width=5), sg.T('', s=(4, 1)), sieve_interact_display_frame
        ]
    ]

    sieve_layout += [
        [sg.Column(layout=sieve_in_go_clear_pause_layout), sg.T('', s=(1, 1)),
         sg.Column(layout=speed_slider_layout), sg.T('', s=(1, 1)),
         sg.Column(layout=sieve_size_selection_layout), sg.T('', s=(1, 1)),
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
    # End of sieve layout

    log_layout = [
        [sg.Text('Log:', font='Helvetica 16')],
        [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                      auto_refresh=True)]
    ]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              ]

    layout += [[sg.TabGroup([[sg.Tab('Sieve', sieve_layout),
                              sg.Tab('The Novelties', novelties_layout),
                              sg.Tab('Log', log_layout)
                              ]], key='-TAB GROUP-', expand_x=True, expand_y=True
                            ),
                ]]

    # layout[-1].append(sg.Sizegrip())
    window = sg.Window('Primes and Novelties', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       finalize=True, keep_on_top=False)
    window.set_min_size(window.size)
    return window
