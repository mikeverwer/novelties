def sRGBtoLin(colourChannel):
    # Send this function a decimal sRGB gamma encoded color value
    # between 0.0 and 1.0, and it returns a linearized value.
    if colourChannel <= 0.04045:
        return colourChannel / 12.92
    else:
        return ((colourChannel + 0.055) / 1.055) ** 2.4


def YtoLstar(Y):
    # Send this function a luminance value between 0.0 and 1.0,
    # and it returns L* which is "perceptual lightness"

    if Y <= (216/24389):       # The CIE standard states 0.008856 but 216/24389 is the intent for 0.008856451679036
        return Y * (24389/27)  # The CIE standard states 903.3, but 24389/27 is the intent, making 903.296296296296296
    else:
        return ((Y ** (1/3)) * 116) - 16
    

def is_bright_color(hex_code):
    # Convert hex code to RGB values, normalized to 1
    vr = int(hex_code[1:3], 16) / 255.0
    vg = int(hex_code[3:5], 16) / 255.0
    vb = int(hex_code[5:7], 16) / 255.0

    # Calculate luminance, Y
    Y = (0.2126 * sRGBtoLin(vr) + 0.7152 * sRGBtoLin(vb) + 0.0722 * sRGBtoLin(vg))

    # Calculate perceived luminance, L*
    luminance = YtoLstar(Y)

    # Define a threshold for brightness (higher = more colour diversity, but poorer visibility)
    brightness_threshold = 0.53

    print(luminance)

    # Return True if the color is considered bright, False otherwise
    return luminance > brightness_threshold

colour = '#525252'
is_bright_color(colour)