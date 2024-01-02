import os

def Init():
    pass

def TransferScreen(screenBuf):
    os.system("clear")
    for r in range(2):
        for c in range(20):
            print(chr(screenBuf[r * 20 + c]), end="")
        print("")
