import Console as Dev
import time
import threading
from enum import Enum

screenBuffer = [ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" ")]

#描画共通処理
def Render():
    global isRenderOk
    if isRenderOk:
        #コールバック一時解除
        global tm
        tm.cancel()
        del tm
        #転送
        Dev.TransferScreen(screenBuffer)
        #フレーム共通処理を動かす
        isRenderOk = False
        #描画スレッド待機
        tm = threading.Timer(0.016, Render)
        tm.start()

#ASCII文字の書き込み
def SetAscii(row, column, code):
    screenBuffer[row * 20 + column] = code

#ASCII文字列の書き込み
def SetAsciiStr(row, column, str):
    strlen = len(str);
    for i in range(strlen):
        code = ord(str[i:i+1])
        SetAscii(row, column + i, code)

#初期化
Dev.Init()

#描画スレッドスタート
tm = threading.Timer(0.016, Render)
tm.start()
isRenderOk = False

#状態定義
class State(Enum):
    TITLE_LOGOANIMATION = 1,
    TITLE_WAIT = 2,
    GAME_READY = 3,
    GAME_MAIN = 4,
    GAME_GAMEOVER = 5,

#タイトル
titleFrameCount = 0
def TitleLogo():
    global titleFrameCount
    global currentState
    SetAsciiStr(0, 4, ("DENTAKU INVADOR")[0:int(titleFrameCount/15)])
    titleFrameCount += 1
    if titleFrameCount / 15 > 15:
        currentState = State.TITLE_WAIT
        titleFrameCount = 0

#タイトル入力待ち
def TitleWait():
    SetAsciiStr(0, 2, "DENTAKU INVADOR")
    SetAsciiStr(1, 2, "PRESS RIGHT BUTTON")

#状態関数
state = {State.TITLE_LOGOANIMATION: TitleLogo,
    State.TITLE_WAIT: TitleWait}

currentState = State.TITLE_LOGOANIMATION

#フレーム共通処理
while True:
    if not isRenderOk:
        state[currentState]()
        isRenderOk = True
