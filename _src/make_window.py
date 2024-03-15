import usefull_prints as uprint
from main_gui import sg, primes_so_far

import BASE64
BASE64.icon

# themes: DarkGrey4, DarkGrey9, GrayGrayGray, LightGray1, TealMono
def make_window(theme='Default1', sieve_default=200, novelty_default=200, sieve_graph_x=1000, sieve_graph_y=10000, novelty_graph_x=1200, novelty_graph_y=10000, sieve_size=14, novelty_size=14):
    sg.theme(theme)
    menu_def = [['&Application', ['&Theme', ['DarkGrey4', 'DarkGrey9', 'GrayGrayGray', 'TealMono'],'E&xit']],
                ['&Help', ['&About']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing', 'More Nothing', 'Exit']]

# Beginning of Novelties Layout
    novelty_graph_layout = [
        sg.Graph((novelty_graph_x, novelty_graph_y), (0, novelty_graph_y), (novelty_graph_x, 0),
                 background_color='#dcdcdc', key='novelty graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]

    novelty_graph_column = sg.Column(layout=[
            [sg.Stretch(), *novelty_graph_layout, sg.Stretch()]
        ], scrollable=True, vertical_scroll_only=True, size=(novelty_graph_x + 10, 500), key='novelty column', expand_y=True, expand_x=True
    )

    fbc = '#e5e4e2'  # frame background colour
    novelty_interact_display_frame = sg.Frame(layout=[
            [sg.T('Value:'.ljust(20), k='novelty clicked value', font='Helvetica 12 bold', background_color=fbc, text_color='#1b1b1b')],
            [sg.T('Conversion:\n'.ljust(20), k='conversion', font='Helvetica 12 bold', background_color=fbc, text_color='#1b1b1b')]
            ],
                title='', background_color='#e5e4e2', relief='solid', vertical_alignment='bottom')

    left_column = sg.Column(layout=[
            [sg.Text(' The Novelties ', font='Helvetica 18 bold', pad=(5,15), relief='raised', border_width=5)],
            [sg.Push(), sg.Column(layout=[
                [sg.Text("Enter the largest natural\nnumber to reach: ")],
                [sg.Input(key='novelty input', size=(10, 1), default_text=str(novelty_default)), sg.Button('Build', key='generate novelties')],
                [sg.T('Font Size:'), sg.DropDown(([2 * i + 10 for i in range(15)]), size=(4, 1), default_value=novelty_size, k='novelty font', enable_events=True, readonly=True)]
                ])
            ],
            [sg.Radio('Natural\nOrdering', 'RADIO1', k='natural order', default=True, enable_events=True), sg.Radio('Novelty\nOrdering', 'RADIO1', k='novelty order', enable_events=True)],
            [sg.Push(), novelty_interact_display_frame, sg.Push()],
            [sg.Push(), sg.Button('Oridinal to Prime\nConversion Chart', k='-SHOW CHART-', s=(14, 2)), sg.Push()],
        ], expand_x=True
    )

    novelties_layout = [
        [sg.vtop(left_column), sg.VerticalSeparator(), sg.Stretch(), novelty_graph_column, sg.T('')]
    ]
    
# Beginning of Sieve Layout
    sieve_graph_layout = [
        sg.Graph((sieve_graph_x, sieve_graph_y), (0, sieve_graph_y), (sieve_graph_x, 0),
                 background_color='#dcdcdc', key='sieve graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]
    
    sieve_size_selection_layout = [
        [sg.T('Text Size ', font='Helvetica 10 bold')], 
        [sg.DropDown(([2 * i + 10 for i in range(15)]), size=(4, 1), default_value=sieve_size, k='sieve font', enable_events=True, readonly=True)],
        [sg.T('')]
    ]
    
    fbc = '#e5e4e2'  # frame background colour
    sieve_interact_display_frame = sg.Frame(layout=[
            [sg.T('Value:'.ljust(20), k='sieve clicked value', font='Helvetica 14 bold', background_color=fbc, text_color='#1b1b1b')],
            [sg.T('Prime Factors:'.ljust(20), k='sieve clicked primes', font='Helvetica 14 bold', background_color=fbc, text_color='#1b1b1b')]
            ],
                title='', background_color='#e5e4e2', relief='solid', vertical_alignment='bottom')
    
    
    tick_positions = ['1/4', '1/2', '1', '2', '4', '8', '16', ' 32']
    speed_slider_layout = [
        [sg.Text("Set Animation Speed:", font='Helvetica 10 bold')],
        [sg.Slider(range=(0.25, 7), orientation="h", size=(31, 20), default_value=2, key="sieve speed", enable_events=True, disable_number_display=True)],  # 4, 32
        [sg.Text(f"{tick_positions[i]}x".ljust(5), font='Helvetica 8 bold') for i in range(len(tick_positions))],
    ]


    sieve_in_go_clear_pause_layout = [
        [sg.Text('  To which number shall we search?', font=('Helvetica', 16))],
        [sg.T(''), sg.Input(key='sieve input', size=(10, 1), default_text=str(sieve_default)),
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
        scrollable=True, vertical_scroll_only=True, size=(sieve_graph_x + 10, 500), key='sieve column', expand_y=True),
        sg.Column(
            layout=[
                [sg.Text('Primes found so far:', font='Helvetica 16'), sg.T('')],
                [sg.Text(uprint.column_print(primes_so_far, 5, string=True), key='found primes',
                         font='Courier 12 bold', expand_x=True, size=(200, 100))]
            ],
            expand_x=True, expand_y=True, vertical_scroll_only=True, scrollable=True, size=(215, 500))
    ]
    ]  # End of sieve layout

   # Settings Layout
    bgColour = 'gray' 
    names, ranges, defaults, resolutions, tick_intervals = ['Sieve Graph X   :', 'Sieve Graph Y   :', 'Novelty Graph X:', 'Novelty Graph Y:'], [(500, 2000), (500, 31000), (500, 2000), (500, 31000)], [1000] * 4, [100, 500, 100, 500], [1500, 30500, 1500, 30500]
    
    graph_dimension_sliders_layout = [
        [sg.Text(text='Graph Dimensions:', background_color=bgColour, font='Helvetica 12 bold'), sg.T('Default', k='default graphs', font='Helvetica 10 bold', text_color='#1b1b1b', background_color=bgColour, enable_events=True)],
        [sg.Text('', background_color=bgColour), sg.T(names[0], background_color=bgColour), sg.Slider(k=f'dimension sx', range=ranges[0], default_value=defaults[0], resolution=resolutions[0], tick_interval=tick_intervals[0], orientation='h', background_color=bgColour, enable_events=True), sg.Text('', background_color=bgColour)],
        [sg.Text('', background_color=bgColour), sg.T(names[1], background_color=bgColour), sg.Slider(k=f'dimension sy', range=ranges[1], default_value=defaults[1], resolution=resolutions[1], tick_interval=tick_intervals[1], orientation='h', background_color=bgColour, enable_events=True), sg.Text('', background_color=bgColour)],
        [sg.Text('', background_color=bgColour), sg.T(names[2], background_color=bgColour), sg.Slider(k=f'dimension nx', range=ranges[2], default_value=defaults[2], resolution=resolutions[2], tick_interval=tick_intervals[2], orientation='h', background_color=bgColour, enable_events=True), sg.Text('', background_color=bgColour)],
        [sg.Text('', background_color=bgColour), sg.T(names[3], background_color=bgColour), sg.Slider(k=f'dimension ny', range=ranges[3], default_value=defaults[3], resolution=resolutions[3], tick_interval=tick_intervals[3], orientation='h', background_color=bgColour, enable_events=True), sg.Text('', background_color=bgColour)],
        [sg.Text('', background_color=bgColour)]
        ]
    
    theme_selection_layout = [
        [sg.Text('Theme Browser', font='Helvetica 12 bold', background_color=bgColour),
         sg.T('Default', k='default graphs', font='Helvetica 10 bold', text_color='#1b1b1b', background_color=bgColour, enable_events=True)],
        [sg.Text('Click to see a demo window.', background_color=bgColour)],
        [sg.Listbox(values=sg.theme_list(), size=(22, 15), key='theme list', enable_events=True, background_color=bgColour)],
    ]

    settings_layout = [
        [sg.Text(' Settings ', font=('Helvetica', 18, 'bold'), relief='raised', border_width=5, p=15),
         sg.Button(image_data=BASE64.save_settings_image, k='save settings', enable_events=True)],
        [sg.Column(layout=graph_dimension_sliders_layout, background_color='gray', pad=15),
         sg.Column(layout=theme_selection_layout, background_color=bgColour)
        ]
    ]

    # Log Layout
    log_layout = [
        [sg.Text('Log:', font=('Helvetica', 18, 'bold'), relief='raised', border_width=5), sg.Button('Clear', k='clear log')],
        [sg.Multiline(size=(60, 15), font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                      auto_refresh=True)]
    ]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
              ]

    layout += [[sg.TabGroup([[sg.Tab('Sieve', sieve_layout),
                              sg.Tab('The Novelties', novelties_layout),
                              sg.Tab('Settings', settings_layout),
                              sg.Tab('Log', log_layout)
                              ]], key='-TAB GROUP-', expand_x=True, expand_y=True
                            ),
                ]]

    layout[-1].append(sg.Sizegrip())
    window = sg.Window('Primes and Novelties', layout, right_click_menu=right_click_menu_def,
                       right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0, 0),
                       finalize=True, keep_on_top=False, font='Helvetica 10 bold', icon=BASE64.icon)
    window.set_min_size(window.size)
    return window
