import PySimpleGUI as sg

# Define the layout
layout = [[sg.Text("Hello, PySimpleGUI!")],
          [sg.Button("OK")]]



# Get the screen resolution
screen_width, screen_height = sg.Window.get_screen_size()

# Get the size of the window
window_width, window_height = (19 * 10, 100)

# Calculate the position of the window
x_pos = screen_width - window_width
y_pos = window_height

# Set the position of the window
window_location = (screen_width / 3, -screen_height / 3)

# Create the window
window = sg.Window("Top Right Window", layout, finalize=True, relative_location=window_location, grab_anywhere=True)

# Read events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "OK":
        break

# Close the window
window.close()
