# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DialogLocalServer.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
        Dialog.resize(590, 209)
        Dialog.setStyleSheet(u"\n"
        "background-color: rgb(31,31,31);\n"
        "font: 12pt \"Arial\";")
        
        Dialog.setModal(False)
        self.widget = QWidget(Dialog)

        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 571, 181))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.API_ID_Label = QLabel(self.widget)
        self.API_ID_Label.setObjectName(u"API_ID_Label")
        self.API_ID_Label.setStyleSheet(u"color: rgb(255, 255, 255);\nfont: 700 Arial;")

        self.horizontalLayout.addWidget(self.API_ID_Label)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.API_ID_Edit = QLineEdit(self.widget)
        
        self.API_ID_Edit.setObjectName(u"API_ID_Edit")
        self.API_ID_Edit.setStyleSheet(u"\n"
"background-color: rgb(255, 255, 255);")
        self.API_ID_Edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.API_ID_Edit.setReadOnly(False)

        self.horizontalLayout.addWidget(self.API_ID_Edit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.HASH_Label = QLabel(self.widget)
        self.HASH_Label.setObjectName(u"HASH_Label")
        self.HASH_Label.setStyleSheet(u"color: rgb(255, 255, 255);\nfont: 700 Arial;")

        self.horizontalLayout_2.addWidget(self.HASH_Label)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.HASH_Edit = QLineEdit(self.widget)
        self.HASH_Edit.setObjectName(u"HASH_Edit")
        self.HASH_Edit.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.HASH_Edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.horizontalLayout_2.addWidget(self.HASH_Edit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setStyleSheet(u"color: rgb(255, 255, 255);\nbackground-color:rgb(12,129,213);\nfont: 700 Arial;")
        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Local Server Settings", u"Local Server Settings", None))
        self.API_ID_Label.setText(QCoreApplication.translate(" ", u"App api_id:", None))
        self.API_ID_Edit.setText("")
        self.API_ID_Edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter Your API_ID", None))
        self.HASH_Label.setText(QCoreApplication.translate("Dialog", u"App api_hash:", None))
        self.HASH_Edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter Your API_HASH", None))
    # retranslateUi

