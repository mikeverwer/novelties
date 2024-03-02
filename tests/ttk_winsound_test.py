import tkinter as tk
import winsound as ws


def sound_decorator(function):
    def wrapped_function(*args, **kwargs):
        ws.PlaySound('Speech Misrecognition.wav', ws.SND_FILENAME)
        print('I am here')
    return wrapped_function


@sound_decorator
def cmd():
    print('command')


root = tk.Tk()
button = tk.Button(root, text = 'Play', command = cmd)
button.pack()
root.mainloop()