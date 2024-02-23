import graph_value_class as gv
import usefull_prints as uprint
import random
from main_gui import colours_list, colours_dict, sieve_font, sg, update_interval


def sieve_animation(window, values, sieve_value_objects, steps=None, em: int = 16, speed: int = 1, primes_so_far=None,
                    passes: int = 0, *args):
    if primes_so_far is None:
        primes_so_far = []
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
   # global update_interval
   # global speed
   # global steps
   # global primes_so_far
   # global passes
   # global sieve_value_objects

    def make_coords(largest: int):
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
        steps['prime colour'] = choose_colour(thing.value)
        box_colour = steps['prime colour']

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

    def draw_scratch(word, line_colour=steps['prime colour']):
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

    if steps['find coordinates']:
        max_sieve = int(values['sieve input'])
        make_coords(max_sieve)

        # move to next step
        steps['find coordinates'] = False
        steps['draw numbers'] = True
        print('[LOG] Coordinates found.')

    elif steps['draw numbers']:
        print('[LOG] Drawing numbers.')
        for number in sieve_value_objects:
            graph.draw_text(str(number.value), number.coord, font=sieve_font + ' bold')
        # move to next step
        steps['box prime'] = True
        steps['draw numbers'] = False

    elif steps['box prime']:
        # find prime
        next_prime_index = next((index for index, obj in enumerate(sieve_value_objects) if obj.is_prime), None)
        prime_obj = None if next_prime_index is None else sieve_value_objects[next_prime_index]
        print(prime_obj)

        if prime_obj is not None:
            prime_value = prime_obj.value
            if prime_value >= int(values['sieve input']) ** 0.5:
                if steps['hurry up'] is None:
                    choice = sg.popup('\nWe have reached a point where the only remaining numbers are prime.\n\n'
                                      'Fast forward to the end?\n', title='',
                                      custom_text=('Yes, please.', 'No, thanks.'),
                                      keep_on_top=True)
                    steps['hurry up'] = True if choice == 'Yes, please' else False
                    if choice == 'Yes, please.':
                        steps['hurry up'] = True
                    elif choice == 'No, thanks.':
                        steps['hurry up'] = False
                    print(f"user chose: {choice}  :  hurry up = {steps['hurry up']}")
            if prime_value <= int(values['sieve input']):
                print(f"[LOG] Prime Found {prime_value}. Drawing box.")
                prime_obj.is_prime = False
                primes_so_far.append(prime_value)
                window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
                draw_box(prime_obj)

                # move to next step
                if steps['hurry up'] is None:  # still need to scratch
                    steps['box prime'] = False  # start scratching
                    steps['scratch multiple'] = True
                    passes = 0
                    update_interval = 1 * speed  # set speed for next phase
                elif steps['hurry up']:  # scratching is done
                    print(f"[LOG] hurry up")
                    steps['box prime'] = False  # finish quickly
                    steps['hurry up'] = True
                else:  # continue drawing boxes
                    steps['box prime'] = True

            else:
                # move to next step
                steps['box prime'] = False
                steps['finished'] = True

        else:  # no primes left to find, finish
            print(f"[LOG] Nothing left to box.")
            # move to next step
            steps['box prime'] = False
            steps['finished'] = True

    elif steps['scratch multiple']:
        prime_value = primes_so_far[-1]
        # choose colour
        colour = colours_list[(prime_value * 100) % len(colours_list)]
        # find number to scratch
        scratch = (prime_value ** 2) + (passes * prime_value)
        scratch_obj = sieve_value_objects[scratch - 2]
        if scratch <= int(values['sieve input']):
            print(f"[LOG] Scratch Multiple: {scratch}")
            scratch_obj.is_prime = False
            draw_scratch(scratch_obj)

            # move to next step - scratching complete
            if scratch + prime_value <= int(values['sieve input']):  # scratch another
                steps['scratch multiple'] = True
                passes += 1
                update_interval = 75 * speed
            else:
                steps['scratch multiple'] = False  # move to next prime
                steps['box prime'] = True
                update_interval = 1 * speed

        else:
            # move to next step - no scratching needed
            steps['scratch multiple'] = False  # move to next prime
            steps['box prime'] = True
            update_interval = 1 * speed

    elif steps['hurry up']:
        for i, sieve_object in enumerate(sieve_value_objects):
            if sieve_object.is_prime:
                draw_box(sieve_object)
                sieve_object.is_prime = False
                primes_so_far.append(i + 2)
        window['found primes'].update(value=uprint.column_print(primes_so_far, 5, string=True))
        # move to next step - finished
        steps['hurry up'] = False
        steps['finished'] = True

