import os
import base64
import PySimpleGUI as sg
import icons

def convert_file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            encoded = base64.b64encode(file.read())
            variable_name = os.path.splitext(os.path.basename(file_path))[0]
            return {variable_name: encoded}
    except Exception as error:
        sg.popup_error(f'An error occurred while encoding the file: {error}')

def convert_folder_to_base64(folder_path):
    encoded_files = {}
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith('.png'):
                encoded = base64.b64encode(open(file_path, 'rb').read())
                variable_name = os.path.splitext(filename)[0]
                encoded_files[variable_name] = encoded
        return encoded_files
    except Exception as error:
        sg.popup_error(f'An error occurred while processing files: {error}')

bg = '#1b1b1b'
layout = [
    [sg.Text('Select a single PNG file:', background_color=bg)],
    [sg.InputText(key='file_path', size=(40, 1)), sg.FileBrowse(file_types=(("PNG Files", "*.png"),), button_color=bg)],
    [sg.Text('Select a folder containing PNG files:', background_color=bg)],
    [sg.InputText(key='folder_path', size=(40, 1)), sg.FolderBrowse(button_color=bg)],
    [sg.Text('Select the output .py file:', background_color=bg)],
    [sg.InputText(key='output_file', size=(40, 1)), sg.FileSaveAs(button_color=bg)],
    [sg.Button('Convert')],
]
sg.theme('DarkGrey4')
window = sg.Window('Base64 Encoder', layout, icon=icons.b64)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Convert':
        file_path = values['file_path']
        folder_path = values['folder_path']
        output_file = values['output_file']

        if file_path:
            encoded_data = convert_file_to_base64(file_path)
            if encoded_data:
                try:
                    with open(output_file, 'w') as py_file:
                        for variable_name, encoded in encoded_data.items():
                            py_file.write(f"{variable_name} = {repr(encoded)}\n")
                    sg.popup('Base64 encoding written to file:', output_file)
                except Exception as error:
                    sg.popup_error('An error occurred:', error)
        elif folder_path:
            encoded_files = convert_folder_to_base64(folder_path)
            if encoded_files:
                try:
                    with open(output_file, 'w') as py_file:
                        for variable_name, encoded in encoded_files.items():
                            py_file.write(f"{variable_name} = {repr(encoded)}\n\n")
                    sg.popup('Base64 encodings written to file:', output_file)
                except Exception as error:
                    sg.popup_error('An error occurred:', error)
        else:
            sg.popup_error('Please select a single file or a folder')

window.close()
