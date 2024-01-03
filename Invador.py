import Console as Dev
import time
import threading
from enum import Enum

screenBuffer = [ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" ")]

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
    screenBuffer[row * 16 + column] = code

#ASCII文字列の書き込み
def SetAsciiStr(row, column, str):
    strlen = len(str);
    for i in range(strlen):
        code = ord(str[i:i+1])
        SetAscii(row, column + i, code)

#文字を全て空白に
def SetAllSpace():
    for r in range(2):
        for c in range(16):
            SetAscii(r, c, ord(" "))

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
def TitleLogo(button):
    global titleFrameCount
    global currentState
    SetAsciiStr(0, 0, ("DENTAKU INVADOR")[0:int(titleFrameCount/15)])
    titleFrameCount += 1
    if titleFrameCount / 15 > 15:
        currentState = State.TITLE_WAIT
        titleFrameCount = 0

#タイトル入力待ち
def TitleWait(button):
    global currentState
    SetAsciiStr(0, 0, "DENTAKU INVADOR")
    SetAsciiStr(1, 0, "PRESS R BUTTON")
    if button & 0x02 > 0:
        SetAllSpace()
        currentState = State.GAME_READY

#READY
def GameReady(button):
    global titleFrameCount
    titleFrameCount += 1
    SetAsciiStr(1, 7, "READY?")
    if titleFrameCount / 15 > 1:
        currentState = State.GAME_MAIN
        titleFrameCount = 0
        score = 0

#ゲーム中
def GameMain(button):
    pass

#GAME OVER
def GameOver(button):
    global titleFrameCount
    titleFrameCount += 1
    SetAsciiStr(0, 4, " GAME OVER ")
    if titleFrameCount / 15 > 1 and button & 0x02 > 0:
        currentState = State.TITLE_WAIT

#状態関数
state = {State.TITLE_LOGOANIMATION: TitleLogo,
    State.TITLE_WAIT: TitleWait,
    State.GAME_READY: GameReady,
    State.GAME_MAIN: GameMain,
    State.GAME_GAMEOVER: GameOver}

currentState = State.TITLE_LOGOANIMATION
button = 0
score = 0

#フレーム共通処理
while True:
    if not isRenderOk:
        state[currentState](button)
        isRenderOk = True
        button = Dev.PopCurrentButton()
