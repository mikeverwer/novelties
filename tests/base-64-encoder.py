import os
import base64
import PySimpleGUI as sg

def convert_file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            encoded = base64.b64encode(file.read())
            return encoded
    except Exception as error:
        sg.popup_error(f'An error occurred while encoding the file: {error}')

def convert_folder_to_base64(folder_path):
    encoded_files = {}
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith('.png'):
                encoded_files[filename] = base64.b64encode(open(file_path, 'rb').read())
        return encoded_files
    except Exception as error:
        sg.popup_error(f'An error occurred while processing files: {error}')

layout = [
    [sg.Radio('File Input', 'RADIO1', default=True, key='file_input_radio'),
     sg.Radio('Folder Input', 'RADIO1', key='folder_input_radio')],
    [sg.Text('Select a file or folder containing PNG files:')],
    [sg.InputText(key='input_path', size=(40, 1)), sg.FileBrowse()],
    [sg.Text('Select the output .py file:')],
    [sg.InputText(key='output_file', size=(40, 1)), sg.FileSaveAs()],
    [sg.Button('Convert')],
]

window = sg.Window('Base64 Encoder', layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Convert':
        input_path = values['input_path']
        output_file = values['output_file']

        try:
            if values['file_input_radio']:
                encoded_data = convert_file_to_base64(input_path)
                if encoded_data:
                    with open(output_file, 'w') as py_file:
                        variable_name = input_path.split('/')[-1].split('.')[0]
                        py_file.write(f"{variable_name} = {repr(encoded_data)}")
                    sg.popup('Base64 encoding written to file:', output_file)
            elif values['folder_input_radio']:
                encoded_files = convert_folder_to_base64(input_path)
                if encoded_files:
                    with open(output_file, 'w') as py_file:
                        for filename, encoded_data in encoded_files.items():
                            variable_name = os.path.splitext(filename)[0]
                            py_file.write(f"{variable_name} = {repr(encoded_data)}\n")
                    sg.popup('Base64 encodings written to file:', output_file)
        except Exception as error:
            sg.popup_error('An error occurred:', error)

window.close()

