import os
import threading
from pynput import keyboard

def OnPressKey(key):
    global buttonBuffer
    if key.char == 'z':
        buttonBuffer |= 0x01
    elif key.char == 'x':
        buttonBuffer |= 0x02
    return True

def OnReleaseKey(key):
    pass

def Init():
    global buttonBuffer
    buttonBuffer = 0
    listener = keyboard.Listener(on_press=OnPressKey,
        on_release=OnReleaseKey)
    listener.start()
    os.system("clear")

def TransferScreen(screenBuf):
    print("\033[2A", end="")
    for r in range(2):
        for c in range(16):
            print(chr(screenBuf[r * 16 + c]), end="")
        print("", end="\n")

def PopCurrentButton():
    global buttonBuffer
    button = buttonBuffer
    buttonBuffer = 0
    return button

def InnerRender():
    global renderFunc
    #コールバック一時解除
    global tm
    tm.cancel()
    del tm
    renderFunc()
    tm = threading.Timer(0.016, InnerRender)
    tm.start()

def SetRenderFunc(func):
    global renderFunc
    global tm
    renderFunc = func
    tm = threading.Timer(0.016, InnerRender)
    tm.start()
