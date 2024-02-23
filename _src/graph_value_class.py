class SieveGraphObject:
    def __init__(self, value, coord: (float, float), row: int, column: int, is_prime: bool, factors: list,
                 hitbox: (float, float) = None):
        self.value = value
        self.coord = coord
        self.row = row
        self.column = column
        self.is_prime = is_prime
        self.factors = factors
        self.hitbox = hitbox

    def make_hitbox(self, char_size):
        bottom_left = (
            self.coord[0] - len(str(self.value)) * (char_size / 2), self.coord[1] + (char_size / 2) - 1)
        top_right = (
            self.coord[0] + len(str(self.value)) * (char_size / 2), self.coord[1] - (char_size / 2) - 1)
        return bottom_left, top_right

    def __repr__(self):
        return f"SieveGraphObject (row={self.row}, col={self.column}, is_prime={self.is_prime})"


def main():
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
