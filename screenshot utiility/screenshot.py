import time
import pyautogui as pag
from tkinter import *


def screenshot():
    name = int(time.time() * 1000)
    name = f'{name}.png'
    pag.screenshot('images/'+name)

def close():
    quit()

root = Tk()

frame = Frame(root)
frame.pack()


screenshot_button = Button(frame, text='Screenshot', command=screenshot)
screenshot_button.pack(side=LEFT)

quit_button = Button(frame, text='quit', command=close)
quit_button.pack(side=RIGHT)

root.mainloop()
