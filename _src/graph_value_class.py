class SieveGraphObject:
    def __init__(self, value: int | float, coord: tuple | list, row: int, column: int, is_prime: bool, factors: list, colours: list,
                 hitbox):
        self.value = value
        self.coord = coord
        self.row = row
        self.column = column
        self.is_prime = is_prime
        self.factors = factors
        self.colours = colours
        self.hitbox = hitbox

    def make_hitbox(self, char_size):
        bottom_left = (
            self.coord[0] - len(str(self.value)) * (char_size / 2) , self.coord[1] + (char_size / 2) - 1)
        top_right = (
            self.coord[0] + len(str(self.value)) * (char_size / 2), self.coord[1] - (char_size / 2) - 1)
        return bottom_left, top_right
    
    def full_hitbox(self, xoffset: int = 0, yoffset: int = 0, offset: None | int = None):
        if offset is not None:
            xoffset = offset
            yoffset = offset
        bottom_left = (self.hitbox[0][0] - xoffset, self.hitbox[0][1] + yoffset)
        bottom_right = (self.hitbox[1][0] + xoffset, self.hitbox[0][1] + yoffset)
        top_right = (self.hitbox[1][0] + xoffset, self.hitbox[1][1] - yoffset)
        top_left = (self.hitbox[0][0] - xoffset, self.hitbox[1][1] - yoffset)
        return bottom_left, bottom_right, top_right, top_left
        

    def is_hit(self, click, xoffset: int = 0, yoffset: int = 0, offset: None | int = None):
        if offset is not None:
            xoffset = offset
            yoffset = offset
        dx = abs(click[0] - self.coord[0])
        dy = abs(click[1] - self.coord[1])
        half_length = abs(self.hitbox[0][0] - self.hitbox[1][0]) / 2
        half_height = abs(self.hitbox[0][1] - self.hitbox[1][1]) / 2
        if dx - half_length <= xoffset and dy - half_height <= yoffset:
            return True
        else:
            return False

    def __repr__(self):
        return f"SieveGraphObject (row={self.row}, col={self.column}, is_prime={self.is_prime})"


sieve_value_objects = []


def main():
    def make_coords(largest: int, em = 16):
        global sieve_value_objects
        column_width = len(str(largest)) + 2
        number_of_columns = 900 // (column_width * em)
        # rows = (largest // number_of_columns) + 1
        numbers = [i for i in range(2, largest + 1)]

        for index, number in enumerate(numbers):
            row = index // number_of_columns + 1
            column = index % number_of_columns + 1
            coords = (column * (column_width * em), row * 1.5 * em)
            value_object = SieveGraphObject(value=number, coord=coords, row=row, column=column, is_prime=True,
                                               factors=[], hitbox=None)
            value_object.hitbox = value_object.make_hitbox(em)
            sieve_value_objects.append(value_object)

    make_coords(100)
    my_object = SieveGraphObject(17, (30, 120), 3, 5, True, [], None)

    print(my_object.row)  # Accessing x coordinate
    print(my_object.column)  # Accessing y coordinate
    print(my_object.is_prime)  # Accessing boolean value

    # Printing the object representation
    print(my_object)
    test_hitbox = my_object.make_hitbox(16)
    print(test_hitbox)


if __name__ == '__main__':
    main()
