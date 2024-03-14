import usefull_prints as uprint
from main_gui import sg, primes_so_far

save_settings_image = b'iVBORw0KGgoAAAANSUhEUgAAAIgAAAAfCAYAAAA82YWpAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAACr5JREFUeJztmntQlNUbxz/LEgiyiyuXTDDRFslwRW7KRaGggAwGVIi41ZTCRCnjGDGmRaYTNhUzdEGIKRpyoSmnGaGmMkblmkg4conQkVgwCCQhQ9gF4mV/fzC88+OHkvpb0z/289/7nvec85znfM85z3N2Je3t7XqMGLkOJnfaACN3N0aBGJkTo0CMzIlRIEbmxCgQI3NiFIiRObltAhEEge7ubv744w/0+rszk56YmODixYsMDAzcaVPuWkwN3eDVq1fJycnh5MmTCIIAwPz589m0aRPPPfccUqnU0F3eNAMDA2RnZ3Pq1CkmJycBkMvlxMXFERcXh0QiueG2RkdHEQSB+fPnA1MLQ6vVYmlpiVQqRRAEEhIS2Lp1K4899thtGc/txOACefXVV9FoNOzYsQNnZ2dGR0eprq6muLiYsbExtm/fbugubwpBEHj55ZcZGhoiPT0dJycntFotx44d46OPPkKv15OQkHDD7eXm5tLW1sbHH38MQE9PD0lJSeTk5ODu7g6Ag4MDlpaWt2U8txuDCqSzs5PGxkb27t1LSEiI+N7LywuJRMI333xDamrqHd1FWlpa+PXXX3n33Xfx9vYW33t7e/P3339TVlZ2UwL5J6RSKdnZ2QZr79/GoAIZGhoCYMGCBbPKoqOjsbe3R6fTYWVlhV6v58svv+Trr7+mv78fmUxGYGAgzz//PGZmZpSUlNDU1ERWVtYMQX3yyScMDAyQkZEBQGVlJZ999hmdnZ0sXLiQ8PBwkpKSMDG5dnj1119/AWBtbT2rLCkpifr6eiYmJjA1nXJNVVUVRUVFdHZ2olAoeOKJJ3jmmWcwMTEhNzeXH3/8Ea1Wy0svvURkZCRffPEFAHl5eTz++ONERUWRnp5OdHQ0vr6+/PDDDzQ2NhIeHs7777+PRqPh/vvvJzU1FQ8PD9GW2tpaCgoK6OnpYdmyZezatYtPP/2UuLg43N3dGRoaIi8vj7q6OnQ6Hc7OzqSkpKBSqW5l6q6LNC0tbZ+hGrOwsKC0tJT6+nomJyeRyWRYW1sjkUiQy+WoVCrMzMwAKCsro6CggOTkZBISEnB0dOTw4cPo9XrRAUVFRahUKhwcHICp8z4zMxNPT088PDw4fvw4b7zxBmvXriUpKYnFixejVqsZHR3F09Pzmjaam5tz9OhRfvrpJ0xMTJDJZMjlcgAWLlyISqUSxVVZWcnrr7+Ol5cXSUlJODo6UlJSwsjICF5eXkxMTNDV1cX4+DiRkZEolUoEQeDs2bMEBwfj7u6Ovb09WVlZuLm54eLiQlVVFd999x3V1dVERkYSFBREa2srZWVlREREYG5uTmNjI7t370alUpGYmIhCoeDQoUN0dHTg5eXF8uXLycrKQqPR8MILLxASEkJ3dzdFRUWEhYUZ9Dgz6A4il8vJysoiJyeH/Px88vPzWbBgAWvWrOGRRx4hICBAdH5XVxeJiYls3LgRABcXF06fPs3PP/8MgI+PDwqFgoqKCvEoOH36NDqdjtDQUPR6Pfn5+QQFBfHKK6+INsybN4/8/Hzi4+OxsrKaZeN9993H/v37+fDDD3nvvfcAsLGxwcPDg6CgIPz8/MRv8/LyCAgIYO/eveI7S0tLPvjgA+Lj4/Hz8+PUqVPodDoiIiKmHGpqSmFhIX5+fqhUqmtmcMPDw7z22mv4+PgAUzFKamoqFy5cwNPTE7VajZOTEwcOHJgxrkOHDonPLS0txMXFsX79egDc3d158803uXTpEjY2Njc8Z/+EwYNUd3d3ioqK6Orq4uzZszQ1NdHQ0EBFRQU+Pj4cPHgQExMT0tLSEASB9vZ2enp66O7upqmpCScnJ2Dq7H700UcpLy9n165dSKVSTpw4gaurK0uWLGFgYID+/n6USiXnz58X+1coFIyPj6PRaK673fr7++Pv7097ezuNjY00NjZSW1tLeXk5oaGh7NmzhytXrtDb20tERMSs9icmJtBoNLi5ud2Sj6RS6Yz4Z9GiRcCUcAA6OjoICgqaUScgIGCGQJYvX05hYSEdHR34+vqyevVqMjMzb8meuTCoQHQ6HXq9HktLS5YuXcrSpUuJiopCEAQKCwtRq9WcOXMGb29vKioqyM7OZmRkhGXLluHk5CQ6apqwsDCOHDlCc3MzK1eupK6ujhdffBGA/v5+AA4fPkxJScmMejKZjD///POaNmq1WkxMTJg3bx5KpRKlUkl0dDRjY2Pk5uZSWlpKTEyMmP6q1Wo+//zzWe0PDg7esp+sra1nxFX/Gy9ptVoxbZ7G1tZ2xvO+ffsoKSmhpqaGb7/9FqlUio+PDxkZGdeMAW8VgwokOzub1tbWWQ6VSqXExsaiVqv57bffeOihhzh48CAPP/wwO3fuxMLCAoADBw5w6dIlsd70BFZWVnLlyhUmJyfFlTXthN27dxMYGHjDNmZmZqLVamesRpiKTbZs2UJpaSnd3d24uroCkJ6eTnBw8M074//g3nvvnSVwrVY749nKyoqUlBRSUlIYHBykqqqKgoICiouLxUVkCAx6k7pq1Sp+//13Tpw4MauspaUFmNpO+/v7GR0dZcOGDaI4dDodra2ts+qFhYVRVVXF8ePH8ff3F+MKe3t75HI51dXVM77//vvv2bx5MyMjI9e00dXVlXPnztHQ0DCrbDr+WbRoEba2tigUCmpqamZ8U15ezqZNm8Tj4HawatUqampqGB8fF9/9t08vX75MYGAgdXV1wFRwHRUVhZOT03XHfasYdAfZuHEjx44dY//+/ZSXl/Pggw9iZmaGRqOhoqICNzc31q1bx8TEBAqFgqKiIsbGxhgaGuLo0aNIJBL6+vpobm5m9erVAAQHB5OXl0dNTQ1vvfWW2JdUKiU5OZns7GwmJyfx9PSkp6eHr776ipiYmFlb9DQxMTFUVFSQkZHB+vXrWbFiBRKJhPb2dqqqqtiwYQMrV64EIDk5mbfffhu9Xo+3tze9vb0cOXKEzZs3i0KVyWR0dnZSWFhIbGwscrkciURCcXExgiBcN5uai8TERCorK0lLSyMsLIy+vj5KS0vFcltbW9asWcM777zDli1bsLGx4ZdffqGtrY1nn332pvubC4OmuVKplJCQECwtLeno6ODMmTPiqnzyySfZvn0799xzD6ampnh4eHDu3Dlqa2sZHh5m27ZthIeH09bWhiAI4i2khYUFgiBgZ2dHbGzsjPPaxcWFBx54gObmZurq6hgZGSE+Pp7Y2NjrXpebmZkRGhqKVCpFo9FQX19PW1sbpqamPP3002zbtk3sY8WKFSiVSlpaWqirq2N4eJi4uDieeuopsX0HBwcuX75MX18fvr6+KBQKzM3N6e3txc7ODmdnZzo7O/Hy8mLx4sUMDQ0hkUjw9/cXbRIEgZ6eHtatW4ednR0ymQw/Pz8uXLhAbW0t4+PjbN26lZMnTxIeHo6joyP+/v5otVoaGhpoaGhAIpGwY8cO1q5da6jpBEBi/E/q3cf00TGdBsPUnUxmZiZqtZolS5b8a7YYf+6/Czl//jz79u2jqakJQRBobW0lLy8PpVKJo6Pjv2qLwe9BjPz/xMfHc/HiRXbu3Cmm266uruzZs+emfmk2BMYj5i7m6tWrDA4OYm9vL2Z7/zbGHeQuRiaTIZPJ7qgNxhjEyJwYBWJkTowCMTInRoEYmROjQIzMiVEgRubkP3huFuyQrU05AAAAAElFTkSuQmCC'
save_settings_inv_image = b'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'

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
         sg.Button(image_data=save_settings_image, k='save settings', enable_events=True)],
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
                       finalize=True, keep_on_top=False, font='Helvetica 10 bold')
    window.set_min_size(window.size)
    return window
