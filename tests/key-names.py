import tkinter as tk

def key(event):
    print(event.keysym)

root = tk.Tk()
frame = tk.Frame(root, width=100, height=100)
frame.bind("<Key>", key)
frame.focus_set()
frame.pack()
root.mainloop()