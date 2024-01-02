import os

def Init():
    pass

def TransferScreen(screenBuf):
    os.system("clear")
    for r in range(2):
        for c in range(10):
            print(chr(screenBuf[r * 10 + c]), end="")
        print("")
