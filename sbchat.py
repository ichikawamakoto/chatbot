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
sm  = QtScxml.QScxmlStateMachine.fromFile()

#初期状態に遷移
sm.start()
el.processEvents()

uttdic = {"start":"SoftBank光5年更新プランの契約解除料は？(税抜き)",
          "ask_q1":"かんたんスマホで入れないオプションは？",
          "ask_q2":""}


