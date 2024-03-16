import PySimpleGUI as sg

def add_carriage_returns(text, n):
    result = ''
    for i in range(0, len(text), n):
        result += text[i:i+n] + '\n'
    return result

layout = [
    [sg.Text('Select a file containing plaintext characters:')],
    [sg.InputText(key='file_path'), sg.FileBrowse()],
    [sg.Text('Or enter plaintext characters:')],
    [sg.Multiline(key='input_text', size=(40, 4))],
    [sg.Text('Enter value of n:')],
    [sg.InputText(key='n')],
    [sg.Button('Add Carriage Returns')],
    [sg.Button('Copy to Clipboard')],
    [sg.Multiline(key='output_text', size=(40, 10))]
]

window = sg.Window('Carriage Return Adder', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Add Carriage Returns':
        file_path = values['file_path']
        input_text = values['input_text']

        try:
            if file_path:
                with open(file_path, 'r') as file:
                    input_text = file.read()
        except Exception as e:
            sg.popup_error(f"An error occurred while reading the file: {e}")
            continue

        try:
            n = int(values['n'])
            output_text = add_carriage_returns(input_text, n)
            window['output_text'].update(output_text)
        except ValueError:
            sg.popup_error("Please enter a valid value for n")
            continue
    elif event == 'Copy to Clipboard':
        sg.clipboard_set(values['output_text'])

window.close()

