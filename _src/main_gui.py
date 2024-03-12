import generate_novelties as gn
import sieve_of_eratosthenes as soe
import usefull_prints as uprint
import make_window as mk
import graph_object_classes as go
import colours
import brightness
# import sieve_animation
import PySimpleGUI as sg
import time
import random

update_interval = 1
colours_list = colours.list_colour_names()
colours_dict = colours.dict_colours()
primes = soe.primes_up_to_100()

sieve_graph_x = 1000
sieve_graph_y = 10000
novelty_graph_x = 1000
novelty_graph_y = 10000
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


def reset_globals(speed=None):
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
    update_interval = 1
    scratch_animation_passes = 0
    animation_speed_sieve = speed if speed is not None else 1


def pt_to_px(pt: int):
    return int(pt)
    # return round((pt / 72) * 96)


def super(char):
    if len(char) == 1 and char.isdigit():
        superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        unicode_superscript = char.translate(superscript_digits)
        return unicode_superscript
    else:
        raise ValueError("Input must be a single-digit string.")


def conversion_chart_window(chart_string, longest):
    x_size = 1 + (len(str(longest)) + 2) * 10
    layout = [[sg.Multiline(chart_string, size=(x_size, 15), font='Courier 12 bold', expand_x=False, expand_y=True, write_only=True, disabled=True,
                      reroute_cprint=True, autoscroll=True, auto_refresh=True)]]
    window = sg.Window('Prime to Ordinal Conversion Chart', layout, use_default_focus=False, resizable=True, modal=False, finalize=True)
    return window


def make_novelty_objects(graph_width: int | float, longest: int, largest: int, em: int, novelties: dict[str], factors: dict[dict[int: int]]):
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
            value_object_Na = go.NoveltyObject(natural=number, novelty=novelties[number], coord=coords, row=row, column=column, factorization=factors[number], hitbox=None)
            value_object_Na.hitbox = value_object_Na.make_hitbox(em)
            value_object_No = go.NoveltyObject(natural=number, novelty=novelties[number], coord=coords, row=row, column=column, factorization=factors[number], hitbox=None)
            value_object_No.hitbox = value_object_No.make_hitbox(em)
            NatOrd.append(value_object_Na)
            NovOrd.append(value_object_No)  # copy to be sorted
        
        # sort NovKey and reassign coordinates based on new order
        sorted_list = sorted(NovOrd, key=lambda s: (s.novelty.count('•'), int(s.novelty.replace('•', ''))))
        for index, value in enumerate(sorted_list):
            row = index // number_of_columns + 1
            column = index % number_of_columns + 1
            coords = (em + (column * pixel_width) - (pixel_width / 2), row * 4 * em)
            value.coord = coords
            value.hitbox = value.make_hitbox(em)

        NovOrd = sorted_list

        return NatOrd, NovOrd


def draw_novelties(window, values, nat_list: list[go.NoveltyObject] = None, nov_list: list[go.NoveltyObject] = None, ordering='novelty', pt=16):
    global primes
    graph = window['novelty graph']
    graph.erase()
    # draw novelties
    print(f'[LOG] Drawing novelties.')
    if ordering == 'natural':
        for value in nat_list:
            graph.draw_text(text=f"{str(value.natural) : ^{value.length}}\n{str(value.novelty) : ^{value.length}}", location=value.coord, font=f'Courier {pt} bold')
            draw_box(value, graph)
    elif ordering == 'novelty':
        i = 0
        for value in nov_list:
            to_print = f"{str(value.natural) : ^{value.length}}\n{str(value.novelty) : ^{value.length}}"
            coordinate = value.coord
            graph.draw_text(text=to_print, location=coordinate, font=f'Courier {pt} bold')
            draw_box(value, graph)
            i += 1


def draw_box(thing, graph, box_colour='black', line_width=2):
    # get geometry
    bottom_left, bottom_right, top_right, top_left = thing.full_hitbox()

    # draw
    graph.draw_line(bottom_left, bottom_right, box_colour, width=line_width)
    graph.draw_line(bottom_left, top_left, box_colour, width=line_width)
    graph.draw_line(top_right, top_left, box_colour, width=line_width)
    graph.draw_line(top_right, bottom_right, box_colour, width=line_width)


def sieve_animation(window, values, max_sieve, em: int = 16, outline_ids=None):
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
        number_of_columns = (975 // pixel_width)
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
        colour_name = colours_list[(int(seed) * 97) % len(colours_list)]  # colour tied to prime, first try
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
        sieve_animation_steps['prime colour'] = choose_colour(thing.value)
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
            graph.draw_text(str(number.value), number.coord, font=sieve_font + ' bold')
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
                                      'Fast forward to the end?\n', title='',
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
                window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
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
        window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
        # move to next step - finished
        sieve_animation_steps['hurry up'] = False
        sieve_animation_steps['finished'] = True

    return outline_ids


def main():
    current_theme = 'DarkGray4'
    main_window = mk.make_window(current_theme, 1000, 200, sieve_graph_x, 10_000, novelty_graph_x, novelty_graph_y)  # themes: DarkGrey4, DarkGrey9, GrayGrayGray, LightGray1, TealMono
    windows = [main_window]
    sieve_graph = main_window['sieve graph']
    novelty_graph = main_window['novelty graph']
    global sieve_graph_y
    global animate_sieve
    global animation_speed_sieve
    global primes_so_far
    global sieve_font
    global sieve_speed_ticks
    global update_interval
    text_height_sieve = pt_to_px(int(sieve_font[-2:]))
    outline_ids = None
    sieve_selection_box = None
    window = main_window
    chart_open: bool = False
    novelty_objects_NatKey, novelty_objects_NovKey = None, None
    max_value = None

    # This is an Event Loop
    while True:
        event, values = window.read(timeout=1000 // update_interval)
        sieve_graph = window['sieve graph']

        # log events and handle closing
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])
        if event in (None, 'Exit', sg.WINDOW_CLOSED):
            print("[LOG] Clicked Exit!")
            window.close()
            windows.pop()
            break

    # ----- Novelty Tab -----------------------------------------------------------------------------
        elif event == 'generate novelties':
            print("[LOG] Clicked Build.")
            try: 
                novelty_graph.erase()
                biggest = int(values['novelty input'])
                novelties, factorizations = gn.generate_up_to(biggest)
                longest = max(len(novelties[item]) for item in novelties)
                novelty_font = int(values['novelty font'])
                em = pt_to_px(novelty_font)
                print(em)
                order = 'novelty' if values['novelty order'] else 'natural'
                # reset variables
                novelty_objects_NatKey, novelty_objects_NovKey = make_novelty_objects(novelty_graph_x, longest, biggest, em, novelties, factorizations)
                draw_novelties(window, values, novelty_objects_NatKey, novelty_objects_NovKey, order, pt=novelty_font)
            except ValueError as ve:
                print(f"[ERROR]: Could not get values from window.\n{ve}")
                pass

        elif event.endswith('order'):
            print(f"[LOG] Clicked {event}")
            order: str = event.split()[0]
            novelty_graph.erase()
            if novelty_objects_NatKey is not None and novelty_objects_NovKey is not None:
                novelty_font = int(values['novelty font'])
                draw_novelties(window, values, novelty_objects_NatKey, novelty_objects_NovKey, order, pt=novelty_font)

        elif event == '-SHOW CHART-':
            print(f"[LOG] Clicked {event}")
            if chart_open:
                chart_window.close()
            try:
                if max_value is None:
                    max_value = int(values['novelty input'])
                primes = soe.sieve_of_eratosthenes(max_value, show=False)  # Build list of primes, useful for primality testing and converting
                prime_ordinals = [i for i in range(1, len(primes) + 1)]
                chart = uprint.multi_list_print([['e'] + prime_ordinals, ['1'] + primes], cutoff=10, give_string=True, headings_every_row=False)
                chart_window = conversion_chart_window(chart, max_value)
                windows.append(chart_window)
            except ValueError:
                pass
            

    # ----- Sieve Tab -------------------------------------------------------------------------------
        elif event == 'go-sieve':
            print(f"[LOG] Clicked {event}")
            try:
                max_sieve = int(values['sieve input'])
                text_height_sieve = pt_to_px(int(sieve_font[-2:]))  # calculate text size in pixels
                sieve_column_width = len(str(max_sieve)) + 1
                columns = 975 // (sieve_column_width * text_height_sieve)
                rows = (max_sieve // columns) + 1
                primes_so_far = []
                reset_globals(speed=values['sieve speed'])
                # check graph size, remake if too small
                required_size = (rows + 1) * (2 * text_height_sieve)
                available_rows = (sieve_graph_y // text_height_sieve) + 1
                print(f'[LOG] {rows} required rows', end=', ')
                print(f"{required_size = }, {sieve_graph_y = }", end=', ')
                print(f"{available_rows = }")
                if rows <= (sieve_graph_y // (text_height_sieve * 2)) + 1:  # enough rows
                    window['found primes'].update(value='None')
                    sieve_graph.erase()
                    outline_ids = None
                    sieve_animation_steps['finished'] = False
                    animate_sieve = True
                    sieve_animation_steps['find coordinates'] = True
                else:  
                    if required_size > 32_500:  # max canvas size
                        sg.popup('Can not make a large enough canvas.\nTry selecting a smaller font size, or input a lower value.', title='Warning', custom_text=('Cancel'), keep_on_top=True)
                        pass
                    else:    
                        popup_event = sg.popup('This will cause the window to reset.\n\nContinue?\n', title='Warning',
                                        custom_text=('Continue', 'Cancel'), keep_on_top=True)
                        if popup_event == 'Continue':
                            sieve_graph_y = required_size
                            window.close()
                            window = mk.make_window(current_theme, sieve_default=max_sieve, sieve_graph_y=required_size, sieve_size=text_height_sieve)
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

        elif event == 'pause sieve':
            print("[LOG] Clicked Pause/Play")
            animate_sieve = not animate_sieve
            old_interval = update_interval
            if animate_sieve:
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

    # ----- Animations -------------------------------------------------------------------------------
        if animate_sieve:
            print('[LOG] Animation Pass')
            outline_ids = sieve_animation(window, values, max_sieve, text_height_sieve, outline_ids)
            # sieve_animation.sieve_animation(window, values, )
            if sieve_animation_steps['finished']:
                animate_sieve = False

    for window in windows:
        window.close()
        exit(0)


if __name__ == "__main__":
    main()
