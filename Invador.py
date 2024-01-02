import Console as Dev
import time
import threading

screenBuffer = [ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "),
    ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord(" "), ord("0")]

#描画共通処理
def Render():
    global isRenderOk
    if isRenderOk:
        #コールバック一時解除
        global tm
        tm.cancel()
        del tm
        #転送
        Dev.transferScreen(screenBuffer)
        #フレーム共通処理を動かす
        isRenderOk = False
        #描画スレッド待機
        tm = threading.Timer(1, Render)
        tm.start()

#描画スレッドスタート
tm = threading.Timer(1, Render)
tm.start()
isRenderOk = False

#フレーム共通処理
while True:
    if not isRenderOk:
        screenBuffer[19] += 1
        isRenderOk = True
