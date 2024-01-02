import os
from pynput import keyboard

def OnPressKey(key):
    global buttonBuffer
    if key.char == 'z':
        buttonBuffer |= 0x01
    elif key.char == 'x':
        buttonBuffer |= 0x02
    return True

def Init():
    global buttonBuffer
    buttonBuffer = 0
    listener = keyboard.Listener(on_press=OnPressKey)
    listener.start()

def TransferScreen(screenBuf):
    os.system("clear")
    for r in range(2):
        for c in range(20):
            print(chr(screenBuf[r * 20 + c]), end="")
        print("", end="\n")

def PopCurrentButton():
    global buttonBuffer
    button = buttonBuffer
    buttonBuffer = 0
    return button
