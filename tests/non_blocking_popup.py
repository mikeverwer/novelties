from random import randint
import PySimpleGUI as sg

def new_window(index):
    w, h = sg.Window.get_screen_size()
    location = (randint(500, w-500), randint(200, h-200))
    layout = [[sg.Text(f'This is sub-window {index}', key='TEXT')], [sg.Button('OK')]]
    return sg.Window(f'Window {index}', layout, location=location, no_titlebar=True, grab_anywhere=True, finalize=True)

layout = [[sg.Button('New Window')]]
main_window = sg.Window('Main Window', layout=layout, grab_anywhere=True, finalize=True)
windows = [main_window]
index = 0
while True:

    win, event, values = sg.read_all_windows()
    print(win)
    if event in (sg.WINDOW_CLOSED, 'OK'):
        if win == main_window:
            break
        win.close()
        windows.remove(win)
        index -= 1
        for i, w in enumerate(windows[1:]):
            w['TEXT'].update(f'This is sub-window {i+1}')

    elif event == 'New Window':
        index += 1
        new_win = new_window(index)
        windows.append(new_win)
        main_window.force_focus()

for win in windows:
    win.close()