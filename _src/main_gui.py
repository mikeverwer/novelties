import generate_novelties as gn
import sieve_of_eratosthenes as soe
import usefull_prints as uprint
import make_window as mk
import graph_object_classes as go
import colours
import brightness
import BASE64
# import sieve_animation
import PySimpleGUI as sg
import webbrowser
import time
import random

update_interval = 1
colours_list = colours.list_colour_names()
colours_dict = colours.dict_colours()
primes = soe.primes_up_to_100()
screen_width, screen_height = sg.Window.get_screen_size()


black = '#1b1b1b'  # light-mode/dark-mode text/backgrounds
white = '#dcdcdc'  #

graph_dimensions = {
            'sx' : int,
            'sy' : int,
            'nx' : int,
            'ny' : int
        }
sieve_font = 'Courier 14'
novelty_font = 'Courier 14'

sieve_animation_steps = {'find coordinates': False,
                         'draw numbers': False,
                         'box prime': False,
                         'scratch multiple': False,
                         'finished': False,
                         'hurry up': None
                         }
sieve_value_objects = []
animate_sieve = False
primes_so_far = ['None']
scratch_animation_passes = int
animation_speed_sieve = 1
sieve_speed_ticks = ['1/4', '1/2', '1', '2', '4', '8', '16', '32']


def reset_globals(set_interval=1, speed=None):
    global update_interval
    global animation_speed_sieve
    global sieve_animation_steps
    global primes_so_far
    global sieve_value_objects
    global scratch_animation_passes

    sieve_animation_steps = {'find coordinates': False,
                             'draw numbers': False,
                             'box prime': False,
                             'prime colour': '',
                             'scratch multiple': False,
                             'finished': False,
                             'hurry up': None
                             }
    sieve_value_objects = []
    primes_so_far = []
    update_interval = set_interval
    scratch_animation_passes = 0
    animation_speed_sieve = speed if speed is not None else 1


def pt_to_px(pt: int):
    return int(pt)
    # return round((pt / 72) * 96)


def super(number):
    # Define a dictionary mapping regular digits to their superscript equivalents
    superscript_digits = {
        '0': '\u2070', '1': '\u00B9', '2': '\u00B2', '3': '\u00B3',
        '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077',
        '8': '\u2078', '9': '\u2079'
    }
    number_str = str(number)
    return ''.join(superscript_digits.get(digit, digit) for digit in number_str)


def conversion_chart_window(chart_string, longest):
    x_size = 1 + (len(str(longest)) + 2) * 10
    layout = [[sg.Multiline(chart_string, size=(x_size, 15), font='Courier 12 bold', expand_x=False, expand_y=True, write_only=True, disabled=True,
                      reroute_cprint=True, autoscroll=True, auto_refresh=True)]]
    window = sg.Window('Prime to Ordinal Conversion Chart', layout, use_default_focus=False, resizable=True, modal=False, finalize=True)
    return window


def make_novelty_objects(graph_width: int | float, longest: int, largest: int, em: int, novelties: dict[str], factors: dict[dict[int: int]], mode='dark'):
        print(f'[LOG] Building co-ordinates.')
        # Initialzes objects to a graph
        column_chars = longest  # was + 2
        pixel_width = column_chars * (em)
        number_of_columns = ((graph_width) // pixel_width)
        # rows = (largest // number_of_columns) + 1
        numbers = [i for i in range(1, largest + 1)]

        NatOrd: list = []  # for ordering, maybe make 2 lists rather than sorting each time
        NovOrd: list = []  # still needs to be ordered according to novelty ordering definition
        print(f'[LOG] Generating objects.')
        for index, number in enumerate(numbers):
            row = index // number_of_columns + 1
            column = index % number_of_columns + 1
            coords = (em + (column * pixel_width) - (pixel_width / 2), row * 4 * em)
            value_object_Na = go.NoveltyObject(natural=number, novelty=novelties[number], coord=coords, row=row, column=column, factors=factors[number], hitbox=None)
            value_object_Na.hitbox = value_object_Na.make_hitbox(em, longest)
            value_object_No = go.NoveltyObject(natural=number, novelty=novelties[number], coord=coords, row=row, column=column, factors=factors[number], hitbox=None)
            value_object_No.hitbox = value_object_No.make_hitbox(em, longest)
            NatOrd.append(value_object_Na)
            NovOrd.append(value_object_No)  # copy to be sorted
        
        # sort NovKey and reassign coordinates based on new order
        sorted_list = sorted(NovOrd, key=lambda s: (s.novelty.count('•'), int(s.novelty.replace('•', ''))))
        for index, value in enumerate(sorted_list):
            row = index // number_of_columns + 1
            column = index % number_of_columns + 1
            coords = (em + (column * pixel_width) - (pixel_width / 2), row * 4 * em)
            value.coord = coords
            value.hitbox = value.make_hitbox(em, longest)

        NovOrd = sorted_list

        return NatOrd, NovOrd


def draw_novelties(window, values, nat_list: list[go.NoveltyObject] = None, nov_list: list[go.NoveltyObject] = None, ordering='novelty', pt=16, mode='dark'):
    global primes
    text_colour = white if mode =='dark' else black
    graph = window['novelty graph']
    graph.erase()
    # draw novelties
    print(f'[LOG] Drawing novelties.')
    if ordering == 'natural':
        for value in nat_list:
            graph.draw_text(text=f"{str(value.natural) : ^{value.length}}\n{str(value.novelty) : ^{value.length}}", location=value.coord, font=f'Courier {pt} bold', color=text_colour)
            draw_box(value, graph, box_colour=text_colour)
    elif ordering == 'novelty':
        i = 0
        for value in nov_list:
            to_print = f"{str(value.natural) : ^{value.length}}\n{str(value.novelty) : ^{value.length}}"
            coordinate = value.coord
            graph.draw_text(text=to_print, location=coordinate, font=f'Courier {pt} bold', color=text_colour)
            draw_box(value, graph, box_colour=text_colour)
            i += 1


def draw_box(thing, graph, box_colour='#dcdcdc', line_width=2, xoffset=0, yoffset=0, offset=None):
    if offset is not None:
            xoffset = offset
            yoffset = offset 
    # get geometry
    bottom_left, bottom_right, top_right, top_left = thing.full_hitbox(xoffset=xoffset, yoffset=yoffset)

    # draw
    l1 = graph.draw_line(bottom_left, bottom_right, box_colour, width=line_width)
    l2 = graph.draw_line(bottom_left, top_left, box_colour, width=line_width)
    l3 = graph.draw_line(top_right, top_left, box_colour, width=line_width)
    l4 = graph.draw_line(top_right, bottom_right, box_colour, width=line_width)
    return l1, l2, l3, l4


def sieve_animation(window: sg.Window, values, max_sieve, em: int = 16, outline_ids=None, mode = 'dark'):
    text_colour = white if mode == 'dark' else black
    graph = window['sieve graph']
    global update_interval
    global animation_speed_sieve
    global sieve_animation_steps
    global primes_so_far
    global scratch_animation_passes
    global sieve_value_objects
    global sieve_speed_ticks

    def make_coords(largest: int):
        global sieve_value_objects
        column_chars = len(str(largest)) + 1  # was + 2
        pixel_width = column_chars * em
        number_of_columns = ((graph_dimensions['sx'] - (em * 2)) // pixel_width)
        # rows = (largest // number_of_columns) + 1
        numbers = [i for i in range(2, largest + 1)]

        for index, number in enumerate(numbers):
            row = index // number_of_columns + 1
            column = index % number_of_columns + 1
            coords = ((column * pixel_width), row * 2 * em)
            value_object = go.SieveGraphObject(value=number, coord=coords, row=row, column=column, is_prime=True,
                                               factors=[], colours=[], hitbox=None)
            value_object.hitbox = value_object.make_hitbox(em)
            sieve_value_objects.append(value_object)

    def choose_colour(seed):
        # colour_name = random.choice(colours_list)  # colour is random each run
        colour_name = colours_list[((int(seed) * 97)) % len(colours_list)]  # colour tied to prime, first try
        colour_hex = colours_dict[colour_name]
        attempts = 1  # ensure the colour is "appropriate"
        print(f"[LOG] Choosing Colour: {attempts = }, {colour_name}, {colour_hex}")
        while brightness.lightness(colour_hex, 0.80):
            attempts += 1
            if attempts > 5:  # limit attempts to break out of cyclic subgroups
                colour_name = random.choice(colours_list)  # colour is random each run
                colour_hex = colours_dict[colour_name]
            else:
                # colour_name = random.choice(colours_list)  # colour is random each run
                colour_name = colours_list[(int(seed) ** (attempts * 2)) % len(colours_list)]  # colour tied to prime
                colour_hex = colours_dict[colour_name]
                print(f"[LOG] Choosing Colour: {attempts = },  {colour_name = },  {colour_hex = }")

        return colour_name

    def draw_box(thing, graph=graph):
        if outline_ids is not None:  # remove previous outline outline
                for outline_id in outline_ids:
                    graph.delete_figure(outline_id)
                    outline_ids.remove(outline_id)
        # choose colour
        sieve_animation_steps['prime colour'] = choose_colour(thing.value) if thing.value > 2 else ('white' if mode == 'dark' else 'black')
        box_colour = sieve_animation_steps['prime colour']
        thing.colours.append(box_colour)

        # get geometry
        bottom_left, bottom_right, top_right, top_left = thing.full_hitbox()

        # draw
        graph.draw_line(bottom_left, bottom_right, box_colour, width=2)
        graph.draw_line(bottom_left, top_left, box_colour, width=2)
        graph.draw_line(top_right, top_left, box_colour, width=2)
        graph.draw_line(top_right, bottom_right, box_colour, width=2)

    def draw_outline(word, outline_colour=sieve_animation_steps['prime colour']):
        # get geometry.
        # bottom_left, bottom_right, top_right, top_left = word.full_hitbox(offset=1)
        corners = word.full_hitbox(offset=2)
        vdash_length = abs(word.hitbox[0][1] - word.hitbox[1][1]) / 3
        hdash_length = abs(word.hitbox[0][0] - word.hitbox[1][0]) / 3
        ids = []

        for i, corner in enumerate(corners):
            vsign = -1 if i == 0 or i == 1 else 1
            hsign = 1 if i % 4 == 0 or i % 4 == 3 else -1
            vdash = (corner, (corner[0], corner[1] + vsign * vdash_length))
            hdash = (corner, (corner[0] + hsign * hdash_length, corner[1]))
            v_id = graph.draw_line(vdash[0], vdash[1], outline_colour)
            h_id = graph.draw_line(hdash[0], hdash[1], outline_colour)
            ids.append(v_id)
            ids.append(h_id)

        return ids

    def draw_scratch(word, line_colour=sieve_animation_steps['prime colour']):
        # find draw height
        center = word.coord
        word.colours.append(line_colour)
        pixel_width = len(str(word.value)) * em
        length = pixel_width - (pixel_width % 3)
        bump = 2  # (em / 6) + 1 decent approximation?
        # generate the sequence: [0, bump, -bump, 2bump, -2bump, ..., nbump, -nbump] where nbump < em / 2
        # sequence is used to handle the gap becoming too large, so we cycle through the sequence in that case
        h_offsets = [(((-1) ** (i - 1)) * (bump * ((i + 1) // 2))) for i in range((int(em) + 1) // 2)]  #
        h_offset = h_offsets[(len(primes_so_far) - 1) % len(h_offsets)]
        height = center[1] + h_offset
        graph.draw_line((center[0] - (length / 2), height),
                        (center[0] + (length / 2), height), line_colour, width=2)
        graph.draw_text(str(word.value), word.coord, font=sieve_font + ' bold', color=text_colour)

    speed_index = int(values['sieve speed'])
    animation_speed_sieve = float(eval(sieve_speed_ticks[speed_index]))
    # these are the steps of the animation: 
    # 1) Build co-ordinate system -> 2) draw numbers at each co-ordinate node -> 3) find prime and draw box -> 4) scratch out multiples -> Repeat from 3 until complete
    if sieve_animation_steps['find coordinates']:
        update_interval = 1000
        make_coords(max_sieve)

        # move to next step
        sieve_animation_steps['find coordinates'] = False
        sieve_animation_steps['draw numbers'] = True
        print('[LOG] Coordinates found.')

    elif sieve_animation_steps['draw numbers']:
        print('[LOG] Drawing numbers.')
        update_interval = 1 * animation_speed_sieve
        for number in sieve_value_objects:
            graph.draw_text(str(number.value), number.coord, font=sieve_font + ' bold', color=text_colour)
            # show hitboxes
            # graph.draw_rectangle(bottom_right=(number.hitbox[1][0], number.hitbox[0][1]), top_left=(number.hitbox[
            # 0][0], number.hitbox[1][1]), line_width=1)
        # move to next step
        sieve_animation_steps['box prime'] = True
        sieve_animation_steps['draw numbers'] = False

    elif sieve_animation_steps['box prime']:
        # find prime
        next_prime_index = next((index for index, obj in enumerate(sieve_value_objects) if obj.is_prime), None)
        prime_obj = None if next_prime_index is None else sieve_value_objects[next_prime_index]

        if prime_obj is not None:
            prime_value = prime_obj.value
            if prime_value >= max_sieve ** 0.5:
                if sieve_animation_steps['hurry up'] is None:
                    choice = sg.popup('\nWe have reached a point where the only remaining numbers are prime.\n\n'
                                      'Fast forward to the end?\n', title='', icon=BASE64.icon,
                                      custom_text=('Yes, please.', 'No, thanks.'),
                                      keep_on_top=True)
                    sieve_animation_steps['hurry up'] = True if choice == 'Yes, please' else False
                    if choice == 'Yes, please.':
                        sieve_animation_steps['hurry up'] = True
                        animation_speed_sieve = 50
                    elif choice == 'No, thanks.':
                        sieve_animation_steps['hurry up'] = False
                    print(f"user chose: {choice}  :  hurry up = {sieve_animation_steps['hurry up']}")
            if prime_value <= max_sieve:
                print(f"[LOG] Prime Found {prime_value}. Drawing box.")
                prime_obj.is_prime = False
                primes_so_far.append(prime_value)
                prime_obj.factors.append(prime_value)
                col = (200 // (12 * len(str(max_sieve)))) + 1
                window['found primes'].update(value=uprint.column_print(primes_so_far, col, string=True))
                draw_box(prime_obj, graph)

                # move to next step
                if sieve_animation_steps['hurry up'] is None:  # still need to scratch
                    sieve_animation_steps['box prime'] = False  # start scratching
                    sieve_animation_steps['scratch multiple'] = True
                    scratch_animation_passes = 0
                    update_interval = 1 * animation_speed_sieve  # set speed for next phase
                    print(f"[LOG] Update Interval set to: {update_interval}, speed was set at: {animation_speed_sieve}")
                elif sieve_animation_steps['hurry up']:  # scratching is done
                    print(f"[LOG] hurry up")
                    sieve_animation_steps['box prime'] = False  # finish quickly
                    sieve_animation_steps['hurry up'] = True
                else:  # continue drawing boxes
                    sieve_animation_steps['box prime'] = True

            else:
                # move to next step
                print['[LOG] ended here']
                sieve_animation_steps['box prime'] = False
                sieve_animation_steps['finished'] = True

        else:  # no primes left to find, finish
            print(f"[LOG] Nothing left to box.")
            # move to next step
            sieve_animation_steps['box prime'] = False
            sieve_animation_steps['finished'] = True

    elif sieve_animation_steps['scratch multiple']:
        prime_value = primes_so_far[-1]
        scratch = (int(prime_value) ** 2) + (scratch_animation_passes * int(prime_value))  # find number to scratch
        scratch_obj = sieve_value_objects[scratch - 2]
        if scratch <= max_sieve:
            print(f"[LOG] Scratch Multiple: {scratch}")
            if outline_ids is not None:  # remove previous outline outline
                for outline_id in outline_ids:
                    graph.delete_figure(outline_id)
            outline_ids = draw_outline(scratch_obj)  # draw outline
            scratch_obj.is_prime = False
            scratch_obj.factors.append(prime_value)
            draw_scratch(scratch_obj)

            # move to next step - scratching complete
            if scratch + int(prime_value) <= max_sieve:  # scratch another
                sieve_animation_steps['scratch multiple'] = True
                scratch_animation_passes += 1
                update_interval = 5 * animation_speed_sieve
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
        for i, sieve_object in enumerate(sieve_value_objects):
            if sieve_object.is_prime:
                draw_box(sieve_object, graph)
                sieve_object.is_prime = False
                primes_so_far.append(i + 2)
                sieve_object.factors.append(sieve_object.value)
        col = (200 // (12 * len(str(max_sieve)))) + 1
        window['found primes'].update(value=uprint.column_print(primes_so_far, col, string=True))
        # move to next step - finished
        sieve_animation_steps['hurry up'] = False
        sieve_animation_steps['finished'] = True

    return outline_ids


def check_size(graph: sg.Graph, value: int, char_width: int, lines_per_row: int | float, px: int, get: bool):
                # checks if the graph will be large enough to display enough items in a given coloumn width
                graph_width, graph_height = graph.get_size()
                px_width = char_width * px
                px_height = lines_per_row * px
                columns = graph_width // px_width
                rows = (value // columns) + 2
                required_size = rows * px_height
                available_rows = (graph_height // px_height) + 1
                print(f'[LOG] {rows} required rows', end=', ')
                print(f"{required_size = }, {graph_height = }", end=', ')
                print(f"{available_rows = }")
                if get: 
                    return required_size, rows <= (graph_height // px_height) + 1  # enough rows
                else: 
                    return rows <= (graph_height // px_height) + 1  # enough rows


def largest_power_of_2_less_than(n):
    if n <= 1:
        return 0  # No power of 2 less than or equal to 1
    power = 0
    while n >= 2:
        n //= 2
        power += 1
    return power


def convert_factors_to_string(prime_dict):
    if prime_dict is None:
        prime_dict = {}
    factors = []
    for prime, exponent in prime_dict.items():
        factors.append(f"{prime}{super(exponent)}")
    return "\u00B7".join(factors)


#################################################################################################
# MAIN
#################################################################################################
def main():
    about_text = 'Made by Mike Verwer;\nPT-Professor of Mathematics and Statistics @ Mohawk College\n\n\ncontact:   mike.verwer@mohawkcollege.ca\ngithub:     github.com\mikeverwer\nwebsite:  mikeverwer.github.io\n\n\n© 2024'
    current_theme = 'DarkGray4'
    default_theme = current_theme
    new_theme = None
    global primes_so_far
    main_window = mk.make_window(sg, theme=default_theme, primes_so_far=primes_so_far)  # themes: DarkGrey4, DarkGrey9, GrayGrayGray, LightGray1, TealMono
    windows = [main_window]
    sieve_graph = main_window['sieve graph']
    novelty_graph = main_window['novelty graph']
    window = main_window
    global graph_dimensions
    global animate_sieve
    global animation_speed_sieve
    global sieve_font
    global sieve_speed_ticks
    global update_interval
    px_sieve = pt_to_px(int(sieve_font[-2:]))
    outline_ids = None
    sieve_selection_box = None
    novelty_selection_box = None
    chart_open: bool = False
    novelty_objects_NatKey, novelty_objects_NovKey = None, None
    max_novelty = None
    mode = 'dark'
    logging = False
    tab_names = {'sieve tab': 0,
                 'novelty tab': 1,
                 'settings tab': 2,
                 'log tab': 3}
    animation_start = False

    def too_big(columns, pt, lines_per_row):
        largest_possible = (31_000 // (pt * lines_per_row)) * columns
        sg.popup(f'Can not make a large enough canvas.\nAt {pt} pt font, the largest value that can be displayed is {largest_possible}\n\nTry selecting a smaller font size, or input a lower value.\nYou can also make the graph wider in Settings.\n\n', title='Warning', custom_text=('    Ok    '), keep_on_top=True, any_key_closes=True, icon=BASE64.icon)

    def generate_novelties(value: int):
        novelty_graph.erase()
        novelties, factorizations = gn.generate_up_to(value)
        order = 'novelty' if values['novelty order'] else 'natural'
        NatKey, NovKey = make_novelty_objects(graph_dimensions['nx'], novelty_char_width, value, novelty_px, novelties, factorizations)
        draw_novelties(window, values, NatKey, NovKey, order, pt=novelty_font, mode=mode)
        return NatKey, NovKey

    def begin_animation(window, values):
        global animate_sieve
        sieve_graph = window['sieve graph']
        reset_globals(set_interval=1000, speed=values['sieve speed'])
        window['found primes'].update(value='None')
        window['pause sieve'].update(disabled=False)
        sieve_graph.erase()
        animate_sieve = True
        sieve_animation_steps['find coordinates'] = True
        return True
    
    def set_window(window, values, graph_dimensions:dict, mode='dark'):
        button_image = BASE64.dark_mode if mode == 'dark' else BASE64.light_mode
        inputs = ['sieve input', 'sieve font', 'novelty input', 'novelty font', 'sieve speed']
        dimensions = ['sx', 'sy', 'nx', 'ny']
        for event in inputs:
            window[event].update(values[event])
        for event in dimensions:
            manual = f'manual {event}'
            slider = f'slider {event}'
            window[manual].update(value=graph_dimensions[event])  # fix when refactor dimension variables into a dict of dicts/lists
            window[slider].update(value=graph_dimensions[event])
        window['mode'].update(image_data=button_image)


    # This is an Event Loop #################################################################################################
    while True:
        event, values = window.read(timeout=1000 // update_interval)
        sieve_graph = window['sieve graph']
        novelty_graph = window['novelty graph']
        sieve_graph.grab_anywhere_exclude()
        novelty_graph.grab_anywhere_exclude()
        if mode == 'dark':
            pause = BASE64.pause_dark_mode
            play = BASE64.play_dark_mode
        elif mode == 'light':
            pause = BASE64.pause_light_mode
            play = BASE64.play_light_mode

        # log events and handle closing
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print(f'============ Event :: {event} : {values[event] if event in values else None} ==============')
            if (logging == True or event == 'show values'):
                print('-------- Values Dictionary (key=value) --------')
                for key in values:
                    print(f'\'{key}\' : {values[key]},')
        if event in (None, 'Exit', sg.WINDOW_CLOSED):
            print("[LOG] Clicked Exit!")
            window.close()
            windows.pop()
            break

    #################################################################################################
    # ----- Novelty Tab -----------------------------------------------------------------------------
    #################################################################################################
        elif event == 'generate novelties' or (event == 'enter' and values['-TAB GROUP-'] == 'novelty tab'):
            print("[LOG] Clicked Build.")
            if values['novelty input'].isnumeric():
                graph_dimensions['nx'], graph_dimensions['ny'] = novelty_graph.get_size()
                max_novelty = int(values['novelty input'])
                novelty_font = int(values['novelty font'])
                novelty_px = pt_to_px(novelty_font)
                longest = largest_power_of_2_less_than(max_novelty)
                novelty_char_width = ((2 * longest) - 1)
                columns = graph_dimensions['nx'] // (novelty_char_width * novelty_font)
                # check size
                required_size, enough_rows = check_size(graph=novelty_graph, value=max_novelty, char_width=novelty_char_width, lines_per_row=4, px=novelty_px, get=True)
                if enough_rows:  # enough rows, build
                    novelty_objects_NatKey, novelty_objects_NovKey = generate_novelties(max_novelty)
                else:
                    if required_size > 31_000:  # max canvas size
                        too_big(columns=columns, pt=novelty_font, lines_per_row=4)
                        pass
                    else:    
                        popup_event = sg.popup('A larger canvas is needed.\nThis will cause the window to reset.\n\nContinue?\n', title='Warning',
                                        custom_text=('Continue', 'Cancel'), keep_on_top=True, icon=BASE64.icon)
                        if popup_event == 'Continue':
                            # get graph dimensions
                            for key in graph_dimensions:
                                graph_dimensions[key] = int(values[f'manual {key[-2:]}'])
                            graph_dimensions['ny'] = int(required_size)
                            required_size = None  # cleanup
                            window.close()
                            window = mk.make_window(sg, current_theme, values, graph_dimensions, mode=mode, primes_so_far=primes_so_far)
                            window['-TAB GROUP-'].Widget.select(1)
                            set_window(window, values, graph_dimensions, mode)
                            novelty_objects_NatKey, novelty_objects_NovKey = generate_novelties(max_novelty)
            else:
                sg.popup("    Input value error.    \n    Please enter only integer values for     \n    the largest value and font.    \n", title='Value Error', custom_text=('    Ok    '), any_key_closes=True)

        elif str(event).endswith('order'):
            print(f"[LOG] Clicked {event}")
            order: str = event.split()[0]
            novelty_graph.erase()
            if novelty_objects_NatKey is not None and novelty_objects_NovKey is not None:
                draw_novelties(window, values, novelty_objects_NatKey, novelty_objects_NovKey, order, pt=novelty_font, mode=mode)

        elif event == 'novelty graph':
            print(f"[LOG] Clicked {event}")
            if novelty_objects_NatKey is not None and novelty_objects_NovKey is not None:
                if novelty_selection_box is not None:
                    for line in novelty_selection_box:
                        novelty_graph.delete_figure(line)
                    window['novelty clicked value'].update(value=f"{'Value:':<{20}}")
                    window['conversion'].update(value=f"{'Conversion:':<{20}}\n")
                click_x = float(values[event][0])
                click_y = float(values[event][1])
                found: bool = False
                order = novelty_objects_NovKey if values['novelty order'] else novelty_objects_NatKey
                longest = len(str(values['novelty input']))
                for value_object in order:
                    if not found:
                        if value_object.is_hit((click_x, click_y), xoffset=0, yoffset=0):
                            novelty_selection_box = draw_box(value_object, novelty_graph, box_colour='magenta', line_width=3, xoffset = -6, yoffset=-4)
                            update_text = f"{'Value:':<{20}}" + f'{value_object.natural:<{longest}}'
                            window['novelty clicked value'].update(value=update_text)
                            conversion = convert_factors_to_string(value_object.factors)
                            update_text = f"{'Conversion:':<{20}}\n" + f"{f'{conversion}':>{longest + 25}}"
                            window['conversion'].update(value=update_text)
                            print(f"[LOG] {value_object}")
                            found = True

        elif event == '-SHOW CHART-':
            print(f"[LOG] Clicked {event}")
            if chart_open:
                chart_window.close()
            try:
                if max_novelty is None:
                    max_novelty = int(values['novelty input'])
                primes = soe.sieve_of_eratosthenes(max_novelty, show=False)  # Build list of primes, useful for primality testing and converting
                prime_ordinals = [i for i in range(1, len(primes) + 1)]
                chart = uprint.multi_list_print([['e'] + prime_ordinals, ['1'] + primes], cutoff=10, give_string=True, headings_every_row=False)
                chart_window = conversion_chart_window(chart, max_novelty)
                windows.append(chart_window)
            except ValueError:
                pass
            
    
    #################################################################################################
    # ----- Sieve Tab -------------------------------------------------------------------------------
    #################################################################################################
        elif event == 'go-sieve' or (event == 'enter' and values['-TAB GROUP-'] == 'sieve tab'):
            print(f"[LOG] Clicked {event}")
            try:
                graph_dimensions['sx'], graph_dimensions['sy'] = sieve_graph.get_size()
                max_sieve = int(values['sieve input'])
                px_sieve = pt_to_px(int(sieve_font[-2:]))  # calculate text size in pixels
                sieve_column_width = len(str(max_sieve)) + 1
                columns = (graph_dimensions['sx'] - (px_sieve * 2)) // (sieve_column_width * px_sieve)
                rows = (max_sieve // columns) + 1
                print(f'[LOG] {rows*columns = }')
                # check graph size, remake if too small
                required_size = (rows + 1) * (2 * px_sieve)
                available_rows = (graph_dimensions['sy'] // (px_sieve * 2)) + 1
                print(f'[LOG] {rows} required rows', end=', ')
                print(f"{required_size = }, {graph_dimensions['sy'] = }", end=', ')
                print(f"{available_rows = }")
                if rows <= (graph_dimensions['sy'] // (px_sieve * 2)) + 1:  # enough rows
                    animation_start = begin_animation(window, values)
                else:  
                    if required_size > 31_000:  # max canvas size
                        too_big(columns=columns, pt=px_sieve, lines_per_row=2)
                        pass
                    else:    
                        popup_event = sg.popup('A larger canvas is needed.\nThis will cause the window to reset.\n\nContinue?\n', title='Warning',
                                        custom_text=('Continue', 'Cancel'), keep_on_top=True, icon=BASE64.icon)
                        if popup_event == 'Continue':
                            # get graph dimensions
                            for key in graph_dimensions:
                                graph_dimensions[key] = int(values[f'manual {key[-2:]}'])
                            graph_dimensions['sy'] = required_size
                            required_size = None  # cleanup
                            window.close()
                            window = mk.make_window(sg, current_theme, values, graph_dimensions, mode=mode, primes_so_far=primes_so_far)
                            window['-TAB GROUP-'].Widget.select(0)
                            set_window(window, values, graph_dimensions, mode)
                            animation_start = begin_animation(window, values)
            except ValueError:
                pass

        elif event == 'sieve speed':
            speed_index = int(values[event])
            animation_speed_sieve = float(eval(sieve_speed_ticks[speed_index]))
            print(f"[LOG] Changed Sieve Speed. Slider value: {values[event]}.  Animation speed: {animation_speed_sieve}")
            # print(speed)
           #  animation_speed_sieve = float(speed)
           #  window[event].update(values[event])

        elif event == 'sieve font':
            print("[LOG] Clicked Font Size")
            sieve_font = 'Courier ' + str(values[event])
            # text_height = pt_to_px(values[event])  # calculate text size in pixels
            window[event].update(values[event])

        elif (event == 'pause sieve' or (event == 'spacebar' and values['-TAB GROUP-'] == 'sieve tab')) and animation_start:
            print("[LOG] Clicked Pause/Play")
            if max_sieve is not None:
                animate_sieve = not animate_sieve
                button_image = pause if animate_sieve else play
                window['pause sieve'].update(image_data=button_image)
                old_interval = update_interval
                if animate_sieve and old_interval is not None:
                    update_interval = old_interval
                else:  # prevent high refresh rate when idle.
                    update_interval = 1

        elif event == 'clear sieve':
            print("[LOG] Clicked Clear.")
            animate_sieve = False
            window['found primes'].update(value='None')
            sieve_graph.erase()
            reset_globals()

        elif event == 'sieve graph':  # display info about value at coords
            print(f"[LOG] Clicked {event}")
            if sieve_selection_box is not None:
                sieve_graph.delete_figure(sieve_selection_box)
            click_x = float(values[event][0])
            click_y = float(values[event][1])
            found: bool = False
            for value_object in sieve_value_objects:
                if not found:
                    if value_object.is_hit((click_x, click_y), xoffset=4, yoffset=3):
                        bottom_right = (value_object.hitbox[1][0] + 4, value_object.hitbox[0][1] + 3)
                        top_left = (value_object.hitbox[0][0] - 4, value_object.hitbox[1][1] - 3)
                        sieve_selection_box = sieve_graph.draw_rectangle(bottom_right, top_left, line_color='magenta')
                        update_text = f"{'Value:':<{23}}" + f'{value_object.value:<}'
                        window['sieve clicked value'].update(value=update_text)
                        print(f"[LOG] {value_object}")
                        if value_object.value in primes_so_far:
                            update_text = f"{'Colour:':<{19}}" + value_object.colours[0]
                            window['sieve clicked primes'].update(value=update_text)
                        else:
                            update_text = f"{'Prime Factors:':<{15}}" + str(value_object.factors) if value_object.factors is not None else f"{'Prime Factors:':<{20}}"
                            window['sieve clicked primes'].update(value=update_text)
                        found = True

    #################################################################################################
    # ----- Settings Tab ----------------------------------------------------------------------------
    #################################################################################################
        elif str(event).startswith('slider'):
            values[event] = int(values[event])
            parameter = event[-2:]
            graph_dimensions[parameter] = values[event]
            window[f'manual {parameter}'].update(value=values[event])
        
        elif str(event).startswith('manual'):
            try:
                set_to = int(values[event])
                parameter = event[-2:]
                if set_to < 100:
                    set_to = 100
                if set_to > screen_width:
                    set_to = screen_width
                graph_dimensions[parameter] = values[event]
                window[f'slider {parameter}'].update(value=values[event])
            except ValueError:
                pass

        elif event == 'mode':
            print(f"[LOG] Clicked {event}", end=': ')
            mode = 'dark' if mode == 'light' else 'light'
            print(f"{mode = }")
            mode_image = BASE64.dark_mode if mode == 'dark' else BASE64.light_mode
            window['mode'].update(image_data=mode_image)
        
        elif event == 'default graphs':
            defaults = [int(screen_width * 0.5 - 310), 600, int(screen_width * 0.5 - 210), 3000]
            for i, key in enumerate(graph_dimensions):
               graph_dimensions[key] = defaults[i]
               window[f'slider {key}'].update(value=defaults[i])
               window[f'manual {key}'].update(value=defaults[i])

        elif event == 'theme list':
            print(f"[LOG] Clicked {event}")
            new_theme = values[event][0]
            sg.change_look_and_feel(values['theme list'][0])
            sg.popup_get_text('This is {}'.format(values['theme list'][0]), icon=BASE64.icon)
        
        elif event == 'default theme':
            new_theme = default_theme
            sg.change_look_and_feel(default_theme)
            sg.popup_get_text(f'This is {default_theme}', icon=BASE64.icon)

        elif event == 'save settings':
            print(f"[LOG] Clicked {event}")
            popup_event = sg.popup_ok_cancel("This will cause the window to be remade.\n\nContinue?\n", icon=BASE64.icon)
            print(f'[LOG] {popup_event = }')
            if popup_event == 'OK':
                if new_theme is None:
                    new_theme = current_theme
                current_theme, values['theme list'] = new_theme, new_theme
                new_theme = None
                # get window values
                for key in graph_dimensions:
                    graph_dimensions[key] = int(values[f'manual {key[-2:]}'])
                window.close()
                window = mk.make_window(sg, current_theme, values, graph_dimensions, mode=mode, primes_so_far=primes_so_far)
                window['-TAB GROUP-'].Widget.select(2)
                set_window(window, values, graph_dimensions, mode)
            else:
                pass

    #################################################################################################
    # ----- Logging Tab -----------------------------------------------------------------------------
    #################################################################################################
        elif event == 'clear log':
            print(f"[LOG] Clicked {event}")
            window['log'].update(value='')

    #################################################################################################
    # ----- Key Binds/Titlebar/Misc. ----------------------------------------------------------------
    #################################################################################################
        elif event == "Full Logging":
            print(f"[LOG] Clicked {event}, {not logging}")
            logging =  not logging
        
        elif event == 'About':
            sg.popup_no_buttons(about_text, title='About Me', icon=BASE64.icon, font= '_ 12')

        elif event == 'Read about the Sieve of Eratosthenes':
            webbrowser.open('https://mikeverwer.github.io/docs/eratosthenes.html')
        
        elif event == 'Read about the Novelties':
            webbrowser.open('https://mikeverwer.github.io/docs/the-novelties.html')

        elif str(event).startswith("change tab"):
            next_tab_name = event.split()[2]
            next_tab = tab_names[next_tab_name + ' tab']
            window['-TAB GROUP-'].Widget.select(next_tab)
        
        elif str(event).startswith('speed') and values['-TAB GROUP-'] == 'sieve tab':
            print(f"[LOG] Clicked {event}")
            new_speed = values['sieve speed']
            new_speed = new_speed + 1 if event.endswith('up') else new_speed - 1
            if new_speed < 0:
                new_speed = 0
            if new_speed > len(sieve_speed_ticks) - 1:
                new_speed = len(sieve_speed_ticks) - 1
            window['sieve speed'].update(value=new_speed)

    #################################################################################################
    # ----- Animations ------------------------------------------------------------------------------
    #################################################################################################
        if animate_sieve:
            print('[LOG] Animation Pass')
            outline_ids = sieve_animation(window, values, max_sieve, px_sieve, outline_ids, mode)
            if sieve_animation_steps['finished']:
                update_interval = 1
                animate_sieve = False

    for window in windows:
        window.close()
        exit(0)


if __name__ == "__main__":
    main()
