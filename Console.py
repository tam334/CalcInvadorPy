import os

def OnPressKey(key):
    #global buttonBuffer
    #if key.char == 'z':
    #    buttonBuffer |= 0x01
    #elif key.char == 'x':
    #    buttonBuffer |= 0x02
    return True

def Init():
    global buttonBuffer
    buttonBuffer = 0
    #listener = keyboard.Listener(on_press=OnPressKey)
    #listener.start()
    os.system("clear")

def TransferScreen(screenBuf):
    print("\033[2A", end="")
    for r in range(2):
        for c in range(16):
            print(chr(screenBuf[r * 16 + c]), end="")
        print("", end="\n")

def PopCurrentButton():
    global buttonBuffer
    button = 0x2
    buttonBuffer = 0
    return button
