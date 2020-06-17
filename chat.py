# coding:utf-8
import sys
from PySide2 import QtCore, QtScxml
import re
from flask import Flask, request, render_template

# Webサーバインスタンスの生成
app1 = Flask(__name__)

# Qtに関するおまじない
app = QtCore.QCoreApplication()
el  = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm  = QtScxml.QScxmlStateMachine.fromFile('chat.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト
print("SYS> 対話を開始")


uttdic = {"start":"こんにちは",
          "ask_name":"お名前をどうぞ",
          "ask_rename":"{}ですね。",
          "ask_task":"要件をどうぞ",
          "ask_retask":"要件は{}ですね。承知しました。"}


# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)

# ユーザ入力の処理

while True:
    text = input("> ")
# ユーザ入力を用いて状態遷
    if current_state == "start":
        if re.match(r"こんにちは",text):
            sm.submitEvent("aisatu")
            el.processEvents()
            aisatu = text
    elif current_state == "ask_name":
        if re.match(r".*です。", text):
            sm.submitEvent("name")
            el.processEvents()
            text2 = text[:-2]
            name = text2
    elif current_state == "ask_rename":
        if re.match(r"はい", text):
            sm.submitEvent("task")
            el.processEvents()
            task = text
    elif current_state == "ask_task":
        if re.match(r".*", text):
            sm.submitEvent("retask")
            el.processEvents()
            retask = text
    elif current_state == "ask_retask":
        if re.match(r"ok", text):
            sm.submitEvent("task")
            el.processEvents()

    # 遷移先の状態を取得
    current_state = sm.activeStateNames()[0]
    print("current_state=", current_state)
    sysutt = uttdic[current_state]
    print("SYS>", sysutt.format(text))


    if current_state == "ask_retask":
        break


if __name__ == "__main__":
    # webサーバーの立ち上げ
    app1.run()


