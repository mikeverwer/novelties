import generate_novelties
import sieve_of_eratosthenes as soe
import usefull_prints as uprint
import make_window as mk
import colours
# import sieve_animation
import PySimpleGUI as sg
import time
import random
import graph_value_class as gv

colours_list = colours.list_colour_names()
colours_dict = colours.dict_colours()
primes = soe.primes_up_to_100()

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
sieve_value_objects = []
animate_sieve = False
primes_so_far = ['None']
scratch_animation_passes = int
animation_speed_sieve = 1


def reset_globals():
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
    animation_speed_sieve = 1


def pt_to_px(pt: int):
    return round((pt / 72) * 96)


def sieve_animation(window, values, steps=None, em: int = 16):
    if steps is None:
        steps = {'find coordinates': False,
                 'draw numbers': False,
                 'box prime': False,
                 'prime colour': '',
                 'scratch multiple': False,
                 'hurry up': None,
                 'finished': False
                 }
    graph = window['sieve graph']
    global update_interval
    global animation_speed_sieve
    global sieve_animation_steps
    global primes_so_far
    global scratch_animation_passes
    global sieve_value_objects

    def make_coords(largest: int):
        global sieve_value_objects
        column_width = len(str(largest)) + 2
        number_of_columns = 900 // (column_width * em)
        # rows = (largest // number_of_columns) + 1
        numbers = [i for i in range(2, largest + 1)]

        for index, number in enumerate(numbers):
            row = index // number_of_columns + 1
            column = index % number_of_columns + 1
            coords = (column * (column_width * em), row * 1.5 * em)
            value_object = gv.SieveGraphObject(value=number, coord=coords, row=row, column=column, is_prime=True,
                                               factors=[], hitbox=None)
            value_object.hitbox = value_object.make_hitbox(em)
            sieve_value_objects.append(value_object)

    def choose_colour(seed):

        def is_bright_color(hex_code):
            # Convert hex code to RGB values
            r = int(hex_code[1:3], 16) / 255.0
            g = int(hex_code[3:5], 16) / 255.0
            b = int(hex_code[5:7], 16) / 255.0

            # Calculate luminance
            luminance = (0.2126 * r) + (0.587 * g) + (0.0722 * b)

            # Define a threshold for brightness (adjust as needed)
            brightness_threshold = 0.55

            print(luminance)

            # Return True if the color is considered bright, False otherwise
            return luminance > brightness_threshold

        # colour_name = random.choice(colours_list)  # colour is random each run
        colour_name = colours_list[(int(seed) * 97) % len(colours_list)]  # colour tied to prime
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
        sieve_animation_steps['prime colour'] = choose_colour(thing.value)
        box_colour = sieve_animation_steps['prime colour']

        # get geometry
        bottom_left = thing.hitbox[0]  # obj.hitbox = (tuple1, tuple2) where each tuple is (x, y); tuple1 is bottom_left, tuple2 is top_right
        bottom_right = (thing.hitbox[1][0], thing.hitbox[0][1])
        top_right = thing.hitbox[1]
        top_left = (thing.hitbox[0][0], thing.hitbox[1][1])

        # draw
        graph.draw_line(bottom_left, bottom_right, box_colour, width=2)
        graph.draw_line(bottom_left, top_left, box_colour, width=2)
        graph.draw_line(top_right, top_left, box_colour, width=2)
        graph.draw_line(top_right, bottom_right, box_colour, width=2)

    def draw_scratch(word, line_colour=sieve_animation_steps['prime colour']):
        # find draw height
        center = word.coord
        length = len(str(word.value)) * em - (em * len(str(word.value)) % 2)
        bump = 2  # (em / 6) + 1 decent approximation?
        # generate the sequence: [0, bump, -bump, 2bump, -2bump, ..., nbump, -nbump] where nbump < em / 2
        # sequence is used to handle the gap becoming too large, so we cycle through the sequence in that case
        h_offsets = [(((-1) ** (i - 1)) * (bump * ((i + 1) // 2))) for i in range((int(em) + 1) // 2)]  #
        h_offset = h_offsets[(len(primes_so_far) - 1) % len(h_offsets)]
        height = center[1] + h_offset
        graph.draw_line((word.coord[0] - (length / 2), height),
                        (word.coord[0] + (length / 2), height), line_colour, width=2)

    if sieve_animation_steps['find coordinates']:
        max_sieve = int(values['sieve input'])
        make_coords(max_sieve)

        # move to next step
        sieve_animation_steps['find coordinates'] = False
        sieve_animation_steps['draw numbers'] = True
        print('[LOG] Coordinates found.')

    elif sieve_animation_steps['draw numbers']:
        print('[LOG] Drawing numbers.')
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
        print(prime_obj)

        if prime_obj is not None:
            prime_value = prime_obj.value
            if prime_value >= int(values['sieve input']) ** 0.5:
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
            if prime_value <= int(values['sieve input']):
                print(f"[LOG] Prime Found {prime_value}. Drawing box.")
                prime_obj.is_prime = False
                primes_so_far.append(prime_value)
                prime_obj.factors.append(prime_value)
                window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
                draw_box(prime_obj)

                # move to next step
                if sieve_animation_steps['hurry up'] is None:  # still need to scratch
                    sieve_animation_steps['box prime'] = False  # start scratching
                    sieve_animation_steps['scratch multiple'] = True
                    scratch_animation_passes = 0
                    update_interval = 1 * animation_speed_sieve  # set speed for next phase
                elif sieve_animation_steps['hurry up']:  # scratching is done
                    print(f"[LOG] hurry up")
                    sieve_animation_steps['box prime'] = False  # finish quickly
                    sieve_animation_steps['hurry up'] = True
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
        prime_value = primes_so_far[-1]
        # choose colour
        colour = colours_list[(prime_value * 100) % len(colours_list)]
        # find number to scratch
        scratch = (int(prime_value) ** 2) + (scratch_animation_passes * int(prime_value))
        scratch_obj = sieve_value_objects[scratch - 2]
        if scratch <= int(values['sieve input']):
            print(f"[LOG] Scratch Multiple: {scratch}")
            scratch_obj.is_prime = False
            scratch_obj.factors.append(prime_value)
            draw_scratch(scratch_obj)

            # move to next step - scratching complete
            if scratch + int(prime_value) <= int(values['sieve input']):  # scratch another
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
        for i, sieve_object in enumerate(sieve_value_objects):
            if sieve_object.is_prime:
                draw_box(sieve_object)
                sieve_object.is_prime = False
                primes_so_far.append(i + 2)
                sieve_object.factors.append(sieve_object.value)
        window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
        # move to next step - finished
        sieve_animation_steps['hurry up'] = False
        sieve_animation_steps['finished'] = True


def main():
    window = mk.make_window(sg.theme(), sieve_graph_x, sieve_graph_y)
    sieve_graph = window['sieve graph']
    global animate_sieve
    global animation_speed_sieve
    global primes_so_far
    global sieve_font
    text_height = pt_to_px(int(sieve_font[-2:]))

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
            try:
                max_sieve = int(values['sieve input'])
                sieve_column_width = len(str(max_sieve)) + 2
                columns = 900 // (sieve_column_width * text_height)
                rows = (max_sieve // columns) + 1
                primes_so_far = []
                reset_globals()
                # check graph size, remake if too small
                if rows <= (sieve_graph_y // text_height) + text_height:  # enough rows
                    window['found primes'].update(value='None')
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
                        window = mk.make_window(sg.theme(), sieve_graph_y=sieve_graph_y)
            except ValueError:
                pass

        elif event.startswith('sieve_speed:'):
            speed = event.split(':')[1]
            animation_speed_sieve = float(speed)

        elif event == 'sieve_font':
            print("[LOG] Clicked Font Size")
            sieve_font = 'Courier ' + str(values[event])
            text_height = pt_to_px(values[event])  # calculate text size in pixels

        elif event == 'pause sieve':
            print("[LOG] Clicked Pause/Play")
            animate_sieve = not animate_sieve

        elif event == 'clear sieve':
            print("[LOG] Clicked Clear.")
            animate_sieve = False
            window['found primes'].update(value='None')
            sieve_graph.erase()

        elif event == 'OK':
            print("[LOG] Rebuild the window.")
            window.close()
            window = mk.make_window(sg.theme(), sieve_graph_y=sieve_graph_y)

        elif event == 'sieve graph':  # display info about value at coords
            click_x = float(values[event][0])
            click_y = float(values[event][1])
            for value_object in sieve_value_objects:
                if value_object.is_hit((click_x, click_y)):
                    update_text = f'Value: {value_object.value:<}\nPrime Factors: {value_object.factors}'
                    print(f'[LOG] ' + update_text)
                    window['sieve value display'].update(value=update_text)

        if animate_sieve:
            print('[LOG] Animation Pass')
            sieve_animation(window, values, dict, em=text_height)
            # sieve_animation.sieve_animation(window, values, )
            if sieve_animation_steps['finished']:
                animate_sieve = False

    window.close()
    exit(0)


if __name__ == "__main__":
    main()
