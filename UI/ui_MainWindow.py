# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)
import UI.resources.resource_rc as res_file_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1040, 610)
        MainWindow.setMinimumSize(QSize(1040, 610))
        MainWindow.setMaximumSize(QSize(1040, 610))
        icon = QIcon()
        icon.addFile(u":/ui_img/icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"\n"
"background-color: rgb(31,31,31);\n"
"font: 12pt \"Arial\";")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(70, 10, 891, 461))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Tokenlabel = QLabel(self.verticalLayoutWidget)
        self.Tokenlabel.setObjectName(u"Tokenlabel")

        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tokenlabel.sizePolicy().hasHeightForWidth())

        self.Tokenlabel.setSizePolicy(sizePolicy)
        self.Tokenlabel.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_2.addWidget(self.Tokenlabel)

        self.TokenlineEdit = QLineEdit(self.verticalLayoutWidget)
        self.TokenlineEdit.setObjectName(u"TokenlineEdit")
        self.TokenlineEdit.setEnabled(True)
        self.TokenlineEdit.setSizeIncrement(QSize(0, 0))
        self.TokenlineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.TokenlineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_2.addWidget(self.TokenlineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.startBotBtn = QPushButton(self.verticalLayoutWidget)
        self.startBotBtn.setObjectName(u"startBotBtn")
        self.startBotBtn.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(110, 197, 118);\n"
"font: 700")

        self.horizontalLayout.addWidget(self.startBotBtn)

        self.stopBotBtn = QPushButton(self.verticalLayoutWidget)
        self.stopBotBtn.setObjectName(u"stopBotBtn")
        self.stopBotBtn.setEnabled(True)
        self.stopBotBtn.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(207, 75, 77);\n"
"font: 700;")

        self.horizontalLayout.addWidget(self.stopBotBtn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.editLogoBtn = QPushButton(self.verticalLayoutWidget)
        self.editLogoBtn.setObjectName(u"editLogoBtn")
 
        self.editLogoBtn.setStyleSheet(u"color: rgb(255, 255, 255);\nbackground-color:rgb(12,129,213);\nfont: 700 Arial;")


        self.verticalLayout_2.addWidget(self.editLogoBtn)

        self.loggingLabel = QLabel(self.verticalLayoutWidget)
        self.loggingLabel.setObjectName(u"loggingLabel")
        self.loggingLabel.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_2.addWidget(self.loggingLabel)

        self.LoggingTextWig = QPlainTextEdit(self.verticalLayoutWidget)
        self.LoggingTextWig.setObjectName(u"LoggingTextWig")
        self.LoggingTextWig.setStyleSheet(u"color: rbg(255,255,255);\nbackground-color: rgb(149, 149, 149);\n font: 10pt Arial")

        self.verticalLayout_2.addWidget(self.LoggingTextWig)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(90, 480, 351, 51))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.LSSettingBtn = QPushButton(self.horizontalLayoutWidget)
        self.LSSettingBtn.setObjectName(u"LSSettingBtn")
        self.LSSettingBtn
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.LSSettingBtn.sizePolicy().hasHeightForWidth())
        self.LSSettingBtn.setSizePolicy(sizePolicy1)
        self.LSSettingBtn.setStyleSheet(u"\n"
"image: url(:/ui_img/settings_.png);")

        self.horizontalLayout_3.addWidget(self.LSSettingBtn)

        self.startLSbtn = QPushButton(self.horizontalLayoutWidget)
    
        self.startLSbtn.setObjectName(u"startLSbtn")
        self.startLSbtn.setCheckable(True)
        self.startLSbtn.setChecked(False)
        self.startLSbtn.setAutoDefault(False)
        self.startLSbtn.setFlat(False)
        self.startLSbtn.setStyleSheet(u"color: rgb(255, 255, 255);\nbackground-color: rgb(12,129,213);\nfont: 700 Arial;\nborder-radius: 10px;\npadding: 5px 15px;")
       

        self.horizontalLayout_3.addWidget(self.startLSbtn)
        self.Dev_Label = QLabel(self.centralwidget)
        self.Dev_Label.setObjectName(u"Dev_Label")
        self.Dev_Label.setGeometry(QRect(384, 550, 271, 21))
        self.Dev_Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Dev_Label.setStyleSheet(u"color: gray;\nfont: 700 10px Arial")
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)

        self.startLSbtn.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("Telegram Logo Bot", u"Telegram Logo Bot", None))
        self.Tokenlabel.setText(QCoreApplication.translate("MainWindow", u"Token", None))
        self.startBotBtn.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stopBotBtn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.editLogoBtn.setText(QCoreApplication.translate("MainWindow", u"Edit Logo", None))
        self.loggingLabel.setText(QCoreApplication.translate("MainWindow", u"Logging:", None))
        self.LSSettingBtn.setText("")
        self.startLSbtn.setText(QCoreApplication.translate("MainWindow", u"Start Local Server", u"Running.."))
        self.Dev_Label.setText(QCoreApplication.translate("MainWindow", u"Developed By Ron Vaknin", None))
    # retranslateUi


