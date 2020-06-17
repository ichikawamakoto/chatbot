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
sm  = QtScxml.QScxmlStateMachine.fromFile('sbyk.scxml')

# 初期状態に遷移
sm.start()
el.processEvents()

# システムプロンプト

uttdic = {"start":"ご用件はなんですか？",
            "ask_pay": "ご利用料金はいくらですか？",
            "ask_net": "インターネット環境はどちらをご利用されていますか？",
            "ask_net_pay": "インターネットの料金はいくらですか？",
            "ask_denki": "ちなみに電力会社はどこですか？",
            "ask_meigi": "電気の名義はお客様ですか？",
            "ask_paypay": "paypay使ってる？",
            "ask_family": "ご家族様はソフトバンクですか？",
            "ask_tablet": "タブレットは持っていますか？",
            "tell_info": "情報を確認して参りますので少々お待ちください",
            "end": "それでは席までご案内いたします"}

# 初期状態の取得
current_state = sm.activeStateNames()[0]
print("current_state=", current_state)

# 初期状態に紐づいたシステム発話の取得と出力
sysutt = uttdic[current_state]
print("SYS>", sysutt)


@app1.route("/")
def taiwa():
    ta = "ヒアリング開始"
    return render_template("chat.html",ta=ta)


@app1.route("/req")
def req():
    current_state = sm.activeStateNames()[0]
    sysutt = uttdic[current_state]
    t = sysutt
    return render_template("req.html",t=t)


# ユーザ入力の処理

@app1.route("/res", methods=["POST"])
def res():
    chat = request.form["chat"]
    current_state = sm.activeStateNames()[0]
    if current_state == "start":
        if re.match(r".*です",chat):
            sm.submitEvent("youken")
            el.processEvents()
            youken = chat
            sysutt = uttdic[current_state]
            return render_template("res.html",chat=youken,message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html",message=message)
    elif current_state == "ask_pay":
        if re.match(r"\d", chat):
            sm.submitEvent("pay")
            el.processEvents()
            mobile = chat
            sysutt = uttdic[current_state]
            return render_template("res.html",chat=mobile,message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html",message=message)
    elif current_state == "ask_net":
        if re.match(r"(ソフトバンク|ドコモ|au|NURO)光",chat):
            sm.submitEvent("net")
            el.processEvents()
            net = chat
            chat2 = chat + "ですね。"
            sysutt = uttdic[current_state]
            return render_template("res.html",chat=net,message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html",message=message)
    elif current_state == "ask_net_pay":
        if re.match(r"\d",chat):
            sm.submitEvent("price")
            el.processEvents()
            price = chat
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=price, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "ask_denki":
        if re.match(r".*電力",chat) or re.match(r".*電気"):
            sm.submitEvent("denki")
            el.processEvents()
            denki = chat
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=denki, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "ask_meigi":
        if re.match(r".*",chat):
            sm.submitEvent("name")
            el.processEvents()
            name = chat
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=name, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "ask_paypay":
        if chat == "yes"or chat == "no":
            sm.submitEvent("pa")
            el.processEvents()
            pa = chat
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=pa, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "ask_family":
        if re.match(r".*です",chat):
            sm.submitEvent("fa")
            el.processEvents()
            fa = chat
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=fa, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "ask_tablet":
        if re.match(r".*",chat):
            sm.submitEvent("ta")
            el.processEvents()
            ta = chat
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=ta, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "tell_info":
        if chat == "ok":
            sm.submitEvent("ok")
            el.processEvents()
            sysutt = uttdic[current_state]
            return render_template("res.html", chat=chat, message=sysutt)
        else:
            message = "再入力してください。"
            return render_template("res.html", message=message)
    elif current_state == "end":
        sysutt = uttdic[current_state]
        message = "それでは席までご案内致します。"
        return render_template("fin.html",message=message)

    # # 遷移先の状態を取得
    # current_state = sm.activeStateNames()[0]
    # print("current_state=", current_state)
    # sysutt = uttdic[current_state]
    # print("SYS>", sysutt)

    # # 遷移先がtell_infoの場合は情報を伝えて終了
    # if current_state == "tell_info":
    #     print("手続き内容は", youken, "\n")
    #     print("利用料金は", mobile)
    #     print("ネットは", net)
    #     print("利用料金は",price)
    #     print("電力会社は",denki)
    #     print("名義は",name)
    #     print("ペイペイ>",pa)
    #     print("家族は",fa)
    #     print("タブレットは",ta)
    # if current_state == "end":
    #     break

if __name__ == "__main__":
    # webサーバーの立ち上げ
    app1.run()