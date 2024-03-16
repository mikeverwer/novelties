import usefull_prints as uprint
from main_gui import sg, primes_so_far

import BASE64

# themes: DarkGrey4, DarkGrey9, GrayGrayGray, LightGray1, TealMono
def make_window(theme='Default1', sieve_default=200, novelty_default=200, sieve_graph_x=1000, sieve_graph_y=10000, novelty_graph_x=1200, novelty_graph_y=10000, sieve_size=14, novelty_size=14, setting_defaults: list = None, mode: str = 'dark'):
    sg.theme(theme)
    screen_width, screen_height = sg.Window.get_screen_size()
    window_size_estimate = screen_width * 0.8
    if setting_defaults is None:
        setting_defaults = [1000, 500, 1200, 1200]
    fbc = '#e5e4e2'  # frame background colour, grayish
    black = '#1b1b1b'  # 
    white = '#dcdcdc'  #
    bgColour = 'gray' 
    if mode == 'dark':
        graph_bg_colour = black
        pause = BASE64.pause_dark_mode
        play = BASE64.play_dark_mode
        start = BASE64.start_dark_mode
        clear = BASE64.clear_dark_mode
    elif mode == 'light':
        graph_bg_colour = white
        pause = BASE64.pause_light_mode
        play = BASE64.play_light_mode
        start = BASE64.start_light_mode
        clear = BASE64.clear_light_mode

    log = f'[WINDOW LOG] {mode = }, {graph_bg_colour = }\n'

    menu_def = [['&Application', ['&Full Logging','E&xit']],
                ['&Help', ['&About']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing', 'More Nothing', 'Exit']]

    def titlecard(title, key=None, k=None):
        if k is not None:
            key = k
        bg = black if mode == 'light' else white
        text = white if mode == 'light' else black
        return sg.Text(title, key=key, font=('Helvetica', 18, 'bold'), relief='raised', border_width=5, background_color=bg, text_color=text, enable_events=True, p=((0, 0), (10, 0)))
    
    

# Beginning of Novelties Layout
    novelty_graph = sg.Graph(
            (novelty_graph_x, novelty_graph_y), (0, novelty_graph_y), (novelty_graph_x, 0),
            background_color=graph_bg_colour, key='novelty graph', expand_y=True, enable_events=True)  # colour AliceBlue

    novelty_graph_column = sg.Column(layout=[
            [sg.Stretch(), novelty_graph, sg.Stretch()]
        ], scrollable=True, vertical_scroll_only=True, size=(novelty_graph_x + 10, 200), key='novelty column', expand_y=True, expand_x=True
    )

    novelty_interact_display_frame = sg.Frame(layout=[
            [sg.T('Value:'.ljust(20), k='novelty clicked value', font='Helvetica 12 bold', background_color=fbc, text_color=black)],
            [sg.T('Conversion:\n'.ljust(20), k='conversion', font='Helvetica 12 bold', background_color=fbc, text_color=black)]
        ], title='', background_color='#e5e4e2', relief='solid', vertical_alignment='bottom')

    novelty_left_column = sg.Column(layout=[
            [titlecard(' The Novelties ')],
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
        [sg.vtop(novelty_left_column), sg.VerticalSeparator(), sg.Stretch(), novelty_graph_column, sg.T('')]
    ]
    
# Beginning of Sieve Layout
    sieve_graph_layout = [
        sg.Graph((sieve_graph_x, sieve_graph_y), (0, sieve_graph_y), (sieve_graph_x, 0),
                 background_color=graph_bg_colour, key='sieve graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]
    
    sieve_size_selection_layout = [
        [sg.T('Text Size ', font='Helvetica 12 bold')], 
        [sg.Push(), sg.DropDown(([2 * i + 10 for i in range(15)]), size=(5, 1), font='Helvetica 14', default_value=sieve_size, k='sieve font', enable_events=True, readonly=True), sg.Push()]
    ]
    
    sieve_interact_display_frame = sg.Frame(layout=[
            [sg.T('Value:'.ljust(20), k='sieve clicked value', font='Helvetica 14 bold', background_color=fbc, text_color=black)],
            [sg.T('Prime Factors:'.ljust(20), k='sieve clicked primes', font='Helvetica 14 bold', background_color=fbc, text_color=black)]
            ],
                title='', background_color='#e5e4e2', relief='solid', vertical_alignment='bottom')
    
    
    tick_positions = ['1/4', '1/2', '1', '2', '4', '8', '16', ' 32']
    speed_slider_layout = [
        [sg.Text("Set Animation Speed:", font='Helvetica 10 bold')],
        [sg.Slider(range=(0.25, 7), orientation="h", size=(31, 20), default_value=2, key="sieve speed", enable_events=True, disable_number_display=True)],  # 4, 32
        [sg.Text(f"{tick_positions[i]}x".ljust(5), font='Helvetica 8 bold') for i in range(len(tick_positions))],
    ]


    sieve_in_go_clear_pause_layout = [
        [sg.Text('  To which number\n  shall we search?', font=('Helvetica', 16)),
         sg.Push(), sg.Input(key='sieve input', size=(7, 1), default_text=str(sieve_default), font='Helvetica 14'), sg.Push()],
        [sg.Push(), sg.Button(image_data=start, font='bold', key='go-sieve'),
         sg.Button(image_data=pause, font='bold', k='pause sieve'),
         sg.Button(image_data=clear, font='bold', k='clear sieve'), sg.Push(),
        ]
    ]

    left_layout_sieve = [
        [sg.Push(), titlecard(' The Sieve of\n Eratosthenes ', k='sieve title'), 
         sg.Column(layout=sieve_size_selection_layout, vertical_alignment='center'), sg.Push()]
    ]

    left_layout_sieve += [
        [sg.Column(layout=sieve_in_go_clear_pause_layout)],
        [sg.Column(layout=speed_slider_layout)],
        [sieve_interact_display_frame],
        [sg.Text('Primes found so far:', font='Helvetica 16')],
        [sg.Column(
            layout=[
                [sg.Text(uprint.column_print(primes_so_far, 5, string=True), key='found primes',
                         font='Courier 14 bold', expand_x=False, size=(50, 100), background_color='gray', relief='raised', p = (5, 0))]
            ],
            expand_x=True, expand_y=True, vertical_scroll_only=True, scrollable=True, size=(100, 200), sbar_width=5, sbar_arrow_width=5, sbar_relief='flat')]
    ]


    sieve_layout = [
        [sg.Column(layout=left_layout_sieve),
        sg.Column(
            layout=[[sg.Stretch(), *sieve_graph_layout, sg.Stretch()]],
            scrollable=True, vertical_scroll_only=True, size=(sieve_graph_x + 10, 200), key='sieve column', expand_y=True),
        ]
    ]  # End of sieve layout

   # Settings Layout
    simple_names = ['Sieve Graph X ', 'Sieve Graph Y ', 'Novelty Graph X', 'Novelty Graph Y']
    names, ranges, resolutions, tick_intervals = [f'{name:<16}:' for name in simple_names], [(100, 2000), (100, 31000), (100, 2000), (100, 31000)], [100, 100, 100, 100], [1900, 30900, 1900, 30900]

    names_column_layout = []
    for name in names:
        names_column_layout.append([sg.T(name, background_color=bgColour, font='Courier 12 bold', p=(16, 22))])

    graph_dimension_sliders_layout = [
        [
            sg.Slider(
                k=f'dimension {axis}',
                range=ranges[i],
                default_value=setting_defaults[i],
                resolution=resolutions[i],
                tick_interval=tick_intervals[i],
                orientation='h',
                background_color=bgColour,
                trough_color=white,
                text_color=black,
                enable_events=True
            ),
            sg.Text('', background_color=bgColour)
        ]
        for i, (axis, range_val) in enumerate(zip(['sx', 'sy', 'nx', 'ny'], ranges))
    ]

    graph_dimension_settings_layout = [
        [sg.Text(text='Graph Settings:', background_color=bgColour, font='Helvetica 12 bold'), sg.T('Default', k='default graphs', font='Helvetica 10 bold', text_color=black, background_color=bgColour, enable_events=True)],
        [sg.Column(layout=names_column_layout, background_color=bgColour, vertical_alignment='top'), sg.Column(layout=graph_dimension_sliders_layout, background_color=bgColour)],
        [sg.Text('', background_color=bgColour)],
        
    ]
    
    theme_selection_layout = [
        [sg.Text('Theme Browser', font='Helvetica 12 bold', background_color=bgColour),
         sg.T('Default', k='default graphs', font='Helvetica 10 bold', text_color=black, background_color=bgColour, enable_events=True)],
        [sg.Text('Click to see a demo window.', background_color=bgColour)],
        [sg.Listbox(values=sg.theme_list(), size=(24, 12), key='theme list', text_color=black, highlight_background_color=black, highlight_text_color=white, sbar_background_color=bgColour, sbar_trough_color=white, sbar_frame_color=black, enable_events=True, background_color=bgColour)],
        [sg.Text('Current theme:', background_color=bgColour), sg.Text(theme, background_color=bgColour, text_color=black)],
        [sg.Push(background_color=bgColour), sg.Button(image_data=BASE64.dark_mode, k='mode', enable_events=True), sg.Push(background_color=bgColour)],
    ]

    settings_layout = [
        [titlecard('Settings'),
         sg.Button(image_data=BASE64.save_settings, k='save settings', enable_events=True)],
        [sg.Column(layout=graph_dimension_settings_layout, background_color=bgColour, pad=15),
         sg.Column(layout=theme_selection_layout, background_color=bgColour)
        ]
    ]

    # Log Layout
    log_layout = [
        [titlecard('Log'), sg.Button(' Show Values ', k='show values'), sg.Button('    Clear    ', k='clear log')],
        [sg.Multiline(size=(60, 15), k='log', font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                      auto_refresh=True, default_text=log)]
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
    window = sg.Window('Primes and Novelties', layout, right_click_menu=right_click_menu_def, location=((screen_width - window_size_estimate) // 2, 25),
                       right_click_menu_tearoff=False, grab_anywhere=True, resizable=True, margins=(5, 5),
                       finalize=True, keep_on_top=False, font='Helvetica 10 bold', icon=BASE64.icon)
    window.set_min_size(window.size)
    return window
