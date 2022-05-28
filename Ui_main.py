# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide2.QtWebEngineWidgets import QWebEngineView


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1619, 916)
        Form.setStyleSheet(u"QPushButton:hover { color: red }\n"
"QCheckBox:hover:checked { color: red }")
        self.tl_bar_Box = QComboBox(Form)
        self.tl_bar_Box.setObjectName(u"tl_bar_Box")
        self.tl_bar_Box.setGeometry(QRect(440, 30, 171, 51))
        self.tl_bar_Box.setStyleSheet(u"border-radius: 7px;\n"
"background-color: white;\n"
"border: 2px solid #4CAF50;\n"
"font-size: 19px;")
        self.map_Button = QPushButton(Form)
        self.map_Button.setObjectName(u"map_Button")
        self.map_Button.setGeometry(QRect(230, 30, 171, 51))
        self.map_Button.setStyleSheet(u"border-radius: 7px;\n"
"background-color: white;\n"
"border: 2px solid #4CAF50;\n"
"font-size: 19px;\n"
"\n"
"")
        self.webview = QWebEngineView(Form)
        self.webview.setObjectName(u"webview")
        self.webview.setGeometry(QRect(30, 120, 1521, 771))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(self.webview.sizePolicy().hasHeightForWidth())
        self.webview.setSizePolicy(sizePolicy)
        self.province_Box = QComboBox(Form)
        self.province_Box.setObjectName(u"province_Box")
        self.province_Box.setGeometry(QRect(740, 30, 171, 51))
        self.province_Box.setStyleSheet(u"border-radius: 7px;\n"
"background-color: white;\n"
"border: 2px solid #4CAF50;\n"
"font-size: 19px;")
        self.wordcloud_line_Box = QComboBox(Form)
        self.wordcloud_line_Box.setObjectName(u"wordcloud_line_Box")
        self.wordcloud_line_Box.setGeometry(QRect(950, 30, 171, 51))
        self.wordcloud_line_Box.setStyleSheet(u"border-radius: 7px;\n"
"background-color: white;\n"
"border: 2px solid #4CAF50;\n"
"font-size: 19px;")
        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(50, 100, 1521, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.map_Button.setText(QCoreApplication.translate("Form", u"PushButton", None))
    # retranslateUi

