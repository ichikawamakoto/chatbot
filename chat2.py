# coding:utf-8
import sys
from PySide2 import QtCore, QtScxml
import re
from flask import Flask, request, render_template

# Webサーバインスタンスの生成
app1 = Flask(__name__)

#Qtに関するおまじない
app = QtCore.QCoreApplication()
el  = QtCore.QEventLoop()

# SCXMLファイルの読み込み
sm  = QtScxml.QScxmlStateMachine.fromFile('chat.scxml')

#初期状態に遷移
sm.start()
el.processEvents()


uttdic = {"start":"こんにちは",
          "ask_name":"お名前をどうぞ",
          "ask_rename":"出身はどこですか？",
          "ask_task":"要件をどうぞ",
          "ask_retask":"要件は{}ですね。承知しました。"}


# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)


@app1.route("/")
def taiwa():
    ta = "対話を開始します。"
    return render_template("chat.html",ta=ta)

@app1.route("/req")
def req():
    current_state = sm.activeStateNames()[0]
    sysutt = uttdic[current_state]
    t = sysutt
    return render_template("req.html",t=t)

@app1.route("/res",methods=["POST"])
def res():
    chat = request.form["chat"]
    current_state = sm.activeStateNames()[0]
    print(current_state)
    if current_state == "start":
        if re.match(r"こんにちは",chat):
            sm.submitEvent("aisatu")
            el.processEvents()
            aisatu = chat
            sysutt = uttdic[current_state]
            return render_template("res.html",chat=aisatu,message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html",message=message)
    elif current_state == "ask_name":
        if re.match(r".*です。", chat):
            sm.submitEvent("name")
            el.processEvents()
            text2 = chat[:-3]
            text3 = text2 + "さんですね。"
            sysutt = uttdic[current_state]
            return render_template("res.html",chat=text2,message=text3)
        else:
            message = "再入力してください。"
            return render_template("res.html",message=message)
    elif current_state == "ask_rename":
        if re.match(r".*県", chat) or re.match(r"北海道",chat) or re.match(r"沖縄",chat):
            sm.submitEvent("task")
            el.processEvents()
            task = chat
            task2 = task + "なんですか"
            sysutt = uttdic[current_state]
            return render_template("res.html",chat=task,message=task2)
        else:
            message = "再入力してください。"
            return render_template("res.html",message=message)
    elif current_state == "ask_task":
            sysutt = uttdic[current_state]
            a = chat
            message = "かしこまりました。"
            return render_template("fin.html",chat=a,message=message)


if __name__ == "__main__":
    # webサーバーの立ち上げ
    app1.run()



