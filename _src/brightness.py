"""
Written by Mike Verwer.

The "brightness" of a colour turns out to be very complicated. This module calculates two measures of 
"brightness"; luminance and perceived lightness.  Luminance is required to calculate percieved lightness.
The following code is an implementation of psudocode provided by StackExchange users Myndex and VC.One on this post:
    https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color
    direct: https://stackoverflow.com/a/56678483
They provide an excellent breakdown of the process in their answer.

The main functions of this module are lightness(args) and luminance(args). They take a colour hex code and return the 
percieved lightness of the colour and the luminance, respectively.  Brightness, as perceived by the human eye, and 
luminance are not the same.  See the linked post above for more information.
The value L* (Lstar) is the percieved brightness while Y is the luminance. 

If you are wondering which one to use for your needs, good luck!  (it's perceived lightness... i think)
"""

def hex_to_linRGB(hex: str = '#FFFFFF'):
    """
    Convert hex code to RGB values, normalized to 1
    """
    vr = int(hex[1:3], 16) / 255.0
    vg = int(hex[3:5], 16) / 255.0
    vb = int(hex[5:7], 16) / 255.0  
    return vr, vg, vb


def sRGBtoLin(colourChannel):
    """
    :param colourChannel: Float [0, 1]: A normalized R, G or B value (sRGB encoded colour value)
    :return: Float: Linearized RBG value (vRGB)
    """
    if colourChannel <= 0.04045:
        return colourChannel / 12.92
    else:
        return ((colourChannel + 0.055) / 1.055) ** 2.4


def luminance(hex_code: str = '#FFFFFF', luminance_threshold: None | float = None):
    """
    Calculates the luminance of a colour based on a hex code.
    If, in addition, is passed a float threshold in [0, 1], will return True if the luminance is larger than the threshold.
    :param hex_code: Type - String:  A colour hex code string, beginning with '#'
    :param luminance_threshold: Type - None | Float: A luminance threshold.  
        Controls what the function will return. If not None will return True if luminance is greater than the threshold.

    :return: luminance: Type: float | bool: Returns Y, the luminance.  Value in [0, 1].
l    """
    Vr, Vb, Vg = hex_to_linRGB(hex_code)
    Y = (0.2126 * sRGBtoLin(Vr) + 0.7152 * sRGBtoLin(Vb) + 0.0722 * sRGBtoLin(Vg))
    if luminance_threshold is None:
        return Y
    else:
        return Y > luminance_threshold


def YtoLstar(Y):
    """
    :param Y: Float [0, 1]: Luminance value
    :return: Float: L* which is "perceptual lightness"
    """
    if Y <= (216/24389):       # The CIE standard states 0.008856 but 216/24389 is the intent for 0.008856451679036
        return Y * (24389/27)  # The CIE standard states 903.3, but 24389/27 is the intent, making 903.296296296296296
    else:
        return ((Y ** (1/3)) * 116) - 16


def lightness(hex_code: str = '#FFFFFF', lightness_threshold: None | float = None):
    """
    Calculates the 'lightness' of a colour based on a hex code.
    If, in addition, is passed a float threshold in [0, 1], will return True if the lightness is larger than the threshold.
    :param hex_code: Type - String:  A colour hex code string, beginning with '#'.
    :param lightness_threshold: Type - None | Float: A lightness threshold.  
        Controls what the function will return. If not None will return True if lightness is greater than the threshold.

    :return: lightness: Type: float | bool: Returns L*, the percieved lightness. Value in [0, 1].
l    """
    # Calculate linearized RGB values
    vr, vb, vg = hex_to_linRGB(hex_code)

    # Calculate luminance, Y
    Y = (0.2126 * sRGBtoLin(vr) + 0.7152 * sRGBtoLin(vb) + 0.0722 * sRGBtoLin(vg))

    # Calculate perceived lightness, L*
    lightness = YtoLstar(Y) / 100

    if lightness_threshold is None:
        return lightness
    else:  
        return lightness > lightness_threshold  # Return True if the color is considered bright, False otherwise


def main():
    colour = '#30022'  # Cadmium red
    colour = '#00EEEE'
    print(f'{colour = }' + f'\n{lightness(colour) = }' + f'\n{luminance(colour) = }')


if __name__ == '__main__':
    main()
