import PySimpleGUI as sg

# Define the layout
layout = [
    [sg.TabGroup([[sg.Tab('Tab 1', [[sg.Button('Button 1', key='-BUTTON1-')]]),
                   sg.Tab('Tab 2', [[sg.Button('Button 2', key='-BUTTON2-')]])]], k='tabgroup')],
    [sg.Button("Exit")]
]

# Create the window
window = sg.Window("Tab Example", layout, finalize=True)

# Focus on Tab 2
window['tabgroup'].Widget.select(1)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == '-BUTTON1-':
        # sg.popup('Button 1 clicked')
        window['tabgroup'].Widget.select(1)
    elif event == '-BUTTON2-':
        sg.popup('Button 2 clicked')

# Close the window
window.close()