import usefull_prints as uprint
from main_gui import sg, primes_so_far

import BASE64

# themes: DarkGrey4, DarkGrey9, GrayGrayGray, LightGray1, TealMono
def make_window(theme='Default1', values: dict=None, graph_dimensions: dict = None, mode: str = 'dark'):
    #################################################################################################
    # ----- Initialize Variables --------------------------------------------------------------------
    #################################################################################################
    sg.theme(theme)
    if graph_dimensions is None:
        graph_dimensions = {
            'sx' : 500,
            'sy' : 600,
            'nx' : 600,
            'ny' : 1200
        }
    if values is None:
        values = {
            'sieve font' : 14,
            'sieve input' : 200,
            'sieve speed' : 2.0,
            'novelty input' : 200,
            'novelty font' : 14,
            'slider sx' : graph_dimensions['sx'],
            'slider sy' : graph_dimensions['sy'],
            'slider nx' : graph_dimensions['nx'],
            'slider ny' : graph_dimensions['ny'],
        }
    
    screen_width, screen_height = sg.Window.get_screen_size()
    desired_window_width, desired_window_height = screen_width * 0.625, (screen_height * 0.125) - 60  # desired_window_height is for how much of the vertical graph is visible
    # Left Panel of Sieve tab is ~300 px
    # Therefore, window_width ~ 300 + 2*window_margin + canvas_width
    # where canvas_width = max(_name_graph_x)
    graph_width = desired_window_width - 310
    graph_dimensions['sx'], graph_dimensions['nx'] = graph_width, graph_width + 100
    window_width_estimate = 310 + graph_width

    slider_values = [values[key] for key in values if key.startswith('slider')]

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

    #################################################################################################
    # ----- Define Functions ------------------------------------------------------------------------
    #################################################################################################
    def titlecard(title, key=None, k=None, pad=((0, 0), (10, 0)), p=None):
        if k is not None:
            key = k
        if p is not None:
            pad = p
        bg = black if mode == 'light' else white
        text = white if mode == 'light' else black
        return sg.Text(title, key=key, font=('Helvetica', 18, 'bold'), relief='raised', border_width=5, background_color=bg, text_color=text, enable_events=True, p=pad)
    
    def make_dimension_sliders_layout(keys: list, ranges, slider_values, resolutions, tick_intervals):
        layout = [
            [
                sg.Slider(
                    k=f'slider {axis}',
                    range=ranges[i],
                    default_value=slider_values[i],
                    resolution=resolutions[i],
                    tick_interval=tick_intervals[i],
                    orientation='h',
                    background_color=bgColour,
                    trough_color=white,
                    text_color=black,
                    enable_events=True,
                    pad = ((0, 16), (0, 0))
                )
            ]
            for i, axis in enumerate(keys)
        ]
        return layout
    
    def make_graph_settings_layout(names, keys: list, ranges, slider_values, resolutions, tick_intervals):
        names_column_layout = []
        for i, name in enumerate(names):
            names_column_layout.append([sg.T(name, background_color=bgColour, font='Courier 12 bold', text_color=black, p=(16, 0)), sg.T("⥂", font='_ 16 bold', background_color=bgColour, p=((0, 16), (0, 0)))])
            names_column_layout.append([sg.In(k=f'manual {keys[i]}', s=(6, 1), font='Helvetica 8', p=((32, 0),(0, 20)), background_color=white, enable_events=True)])
        layout = [
            [sg.Column(layout=names_column_layout, background_color=bgColour, vertical_alignment='bottom', p=((0,0), (32,0))),
             sg.Column(layout=make_dimension_sliders_layout(keys, ranges, slider_values, resolutions, tick_intervals), background_color=bgColour)]
        ]
        return layout
    
    #################################################################################################
    # ----- Novelty Layout --------------------------------------------------------------------------
    #################################################################################################
    novelty_graph = sg.Graph(
            (graph_dimensions['nx'], graph_dimensions['ny']), (0, graph_dimensions['ny']), (graph_dimensions['nx'], 0),
            background_color=graph_bg_colour, key='novelty graph', expand_y=True, enable_events=True)  # colour AliceBlue

    novelty_graph_column = sg.Column(layout=[
            [sg.Stretch(), novelty_graph, sg.Stretch()]
        ], scrollable=True, vertical_scroll_only=True, size=(graph_dimensions['nx'] + 10, desired_window_height), key='novelty column', expand_y=True, expand_x=True
    )

    novelty_interact_display_frame = sg.Frame(layout=[
            [sg.T('Value:'.ljust(20), k='novelty clicked value', font='Helvetica 12 bold', background_color=fbc, text_color=black)],
            [sg.T('Conversion:\n'.ljust(20), k='conversion', font='Helvetica 12 bold', background_color=fbc, text_color=black)]
        ], title='', background_color='#e5e4e2', relief='solid', vertical_alignment='bottom')

    novelty_left_column = sg.Column(layout=[
            [sg.Push(), titlecard(' The Novelties '), sg.Push()],
            [sg.Push(), sg.Column(layout=[
                [sg.Text("Enter the largest natural\nnumber to reach: ")],
                [sg.Input(key='novelty input', size=(10, 1), default_text=str(values['novelty input'])), sg.Button('Build', key='generate novelties')],
                [sg.T('Font Size:'), sg.DropDown(([2 * i + 10 for i in range(15)]), size=(4, 1), default_value=values['novelty font'], k='novelty font', enable_events=True, readonly=True)]
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
    
    #################################################################################################
    # ----- Sieve Layout ----------------------------------------------------------------------------
    #################################################################################################
    sieve_graph_layout = [
        sg.Graph((graph_dimensions['sx'], graph_dimensions['sy']), (0, graph_dimensions['sy']), (graph_dimensions['sx'], 0),
                 background_color=graph_bg_colour, key='sieve graph', expand_y=True, enable_events=True)  # colour AliceBlue
    ]
    
    sieve_size_selection_layout = [
        [sg.T('Text Size ', font='Helvetica 12 bold')], 
        [sg.Push(), sg.DropDown(([2 * i + 10 for i in range(15)]), size=(5, 1), font='Helvetica 14', default_value=values['sieve font'], k='sieve font', enable_events=True, readonly=True), sg.Push()]
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
         sg.Push(), sg.Input(key='sieve input', size=(7, 1), default_text=str(values['sieve input']), font='Helvetica 14'), sg.Push()],
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
            scrollable=True, vertical_scroll_only=True, size=(graph_dimensions['sx'] + 10, desired_window_height), key='sieve column', expand_y=True),
        ]
    ]  # End of sieve layout

    #################################################################################################
    # ----- Settings Layout -------------------------------------------------------------------------
    #################################################################################################
    simple_names = ['Sieve Graph X ', 'Sieve Graph Y ', 'Novelty Graph X', 'Novelty Graph Y']
    names, ranges, resolutions, tick_intervals = [f'{name:<15}' for name in simple_names], [(100, 2000), (100, 31000), (100, 2000), (100, 31000)], [100, 100, 100, 100], [1900, 30900, 1900, 30900]

    graph_dimension_settings_layout = [[sg.Text('Graph Settings', font='Helvetica 14 bold', background_color=bgColour),
         sg.T('Default', k='default graphs', font='Helvetica 12 bold', text_color=black, background_color=bgColour, enable_events=True)]]
    graph_dimension_settings_layout += make_graph_settings_layout(names[0:2], ['sx', 'sy'], ranges, slider_values, resolutions, tick_intervals) 
    graph_dimension_settings_layout += [[sg.HorizontalSeparator(color=black)]]
    graph_dimension_settings_layout += make_graph_settings_layout(names[2:4], ['nx', 'ny'], ranges, slider_values, resolutions, tick_intervals)

    theme_selection_layout = [
        [sg.Text('Theme Browser', font='Helvetica 12 bold', background_color=bgColour),
         sg.T('Default', k='default graphs', font='Helvetica 10 bold', text_color=black, background_color=bgColour, enable_events=True)],
        [sg.Text('Click to see a demo window.', background_color=bgColour)],
        [sg.Listbox(values=sg.theme_list(), size=(24, 15), key='theme list', text_color=black, highlight_background_color=black, highlight_text_color=white, sbar_background_color=bgColour, sbar_trough_color=white, sbar_frame_color=black, enable_events=True, background_color=bgColour)],
        [sg.Text('Current theme:', background_color=bgColour), sg.Text(theme, background_color=bgColour, text_color=black)],
    ]

    settings_layout = [
        [titlecard('Settings', p=((15, 15), (10, 0))),
         sg.Button(image_data=BASE64.save_settings, k='save settings', enable_events=True, p=((10, 10), (10, 0))), sg.Button(image_data=BASE64.dark_mode, k='mode', enable_events=True,  p=((10, 10), (10, 0)))],
        [sg.Column(layout=graph_dimension_settings_layout, background_color=bgColour, pad=15),
         sg.Column(layout=theme_selection_layout, background_color=bgColour)
        ]
    ]

    #################################################################################################
    # ----- Log Layout ------------------------------------------------------------------------------
    #################################################################################################
    log_layout = [
        [titlecard('Log'), sg.Button(' Show Values ', k='show values'), sg.Button('    Clear    ', k='clear log')],
        [sg.Multiline(size=(60, 15), k='log', font='Courier 8', expand_x=True, expand_y=True, write_only=True,
                      reroute_stdout=True, reroute_stderr=True, echo_stdout_stderr=True, autoscroll=True,
                      auto_refresh=True, default_text=log)]
    ]

    layout = [[sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=False)],
              ]

    layout += [[sg.TabGroup([[sg.Tab('Sieve', sieve_layout),
                              sg.Tab('The Novelties', novelties_layout),
                              sg.Tab('Settings', settings_layout),
                              sg.Tab('Log', log_layout)
                              ]], key='-TAB GROUP-', expand_x=True, expand_y=True
                            ),
                ]]

    layout[-1].append(sg.Sizegrip())

    #################################################################################################
    # ----- Create Window ---------------------------------------------------------------------------
    #################################################################################################
    window = sg.Window('Primes and Novelties', layout=layout, 
                       right_click_menu_tearoff=False, grab_anywhere=True, resizable=True, margins=(5, 5),
                       finalize=True, keep_on_top=False, font='Helvetica 10 bold', icon=BASE64.icon)
    window.set_min_size(window.size)
    return window


def main():
    window = make_window('DarkGrey')
    update_interval = 1
    # This is an Event Loop #################################################################################################
    while True:
        event, values = window.read(timeout=1000 // update_interval)
        sieve_graph = window['sieve graph']
        novelty_graph = window['novelty graph']

        # log events and handle closing
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print(f'============ Event :: {event} : {values[event] if event in values else None} ==============')
            if (event == 'show values'):
                print('-------- Values Dictionary (key=value) --------')
                for key in values:
                    print(f'\'{key}\' : {values[key]},')
        if event in (None, 'Exit', sg.WINDOW_CLOSED):
            print("[LOG] Clicked Exit!")
            window.close()
            break

if __name__ == '__main__':
    main()