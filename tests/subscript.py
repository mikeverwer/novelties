def convert_to_unicode(char, subscript=False):
    if len(char) == 1 and char.isdigit():
        # Calculate the Unicode code point offset for subscript or superscript digits
        offset = ord('₀') - ord('0') if subscript else ord('⁰') - ord('0')
        unicode_char = chr(ord(char) + offset)
        return unicode_char
    else:
        raise ValueError("Input must be a single-digit string.")

# Example usage:
input_char = "2"
subscript_result = convert_to_unicode(input_char, subscript=True)
superscript_result = convert_to_unicode(input_char, subscript=False)

print("Subscript:", subscript_result)  # Output: ₂
print("Superscript:", superscript_result)  # Output: ²

def convert_to_superscript(char):
    if len(char) == 1 and char.isdigit():
        superscript_digits = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        unicode_superscript = char.translate(superscript_digits)
        return unicode_superscript
    else:
        raise ValueError("Input must be a single-digit string.")

# Example usage:
input_char = "2"
superscript_result = convert_to_superscript(input_char)

print("Superscript:", superscript_result)  # Output: ²
