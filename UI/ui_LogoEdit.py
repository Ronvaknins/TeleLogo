# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit-logoWidgetAzWEBF.ui'
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
    QFrame, QSizePolicy, QWidget,QPushButton,QCheckBox)

class Ui_LogoEditWindow(object):
    def setupUi(self, LogoEditWindow):
        if not LogoEditWindow.objectName():
            LogoEditWindow.setObjectName(u"LogoEditWindow")
        LogoEditWindow.resize(1100, 630)
        LogoEditWindow.setMaximumSize(QSize(1100, 630))
        LogoEditWindow.setMinimumSize(QSize(1100, 630))
        LogoEditWindow.setStyleSheet(u"\n"
        "background-color: rgb(31,31,31);\n"
        "font: 12pt \"Arial\";")
        LogoEditWindow.setWindowFlags(Qt.WindowType.WindowTitleHint | Qt.WindowType.CustomizeWindowHint)
        self.buttonBox = QDialogButtonBox(LogoEditWindow)
        self.discard_button = self.buttonBox.addButton(QDialogButtonBox.StandardButton.Discard)
        self.save_button = self.buttonBox.addButton(QDialogButtonBox.StandardButton.Save) # Optional Cancel Button
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(390, 580, 621, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStyleSheet(u"color: rgb(255, 255, 255);\nbackground-color:rgb(12,129,213);\nfont: 700 Arial;")
        self.select_file_button = QPushButton("Select File")
        self.select_file_button.setGeometry(100,590,100,24)
        self.select_file_button.setStyleSheet(u"color: rgb(255, 255, 255);\nbackground-color:rgb(12,129,213);\nfont: 700 Arial;")
        self.video_frame = QFrame(LogoEditWindow)
        self.video_frame.setObjectName(u"video_frame")
        self.video_frame.setGeometry(QRect(70, 30, 960, 540))
        self.video_frame.setStyleSheet(u"background-color: lightgray;")
        self.video_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.video_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.safeMargCB = QCheckBox(self.video_frame)
        self.safeMargCB.setObjectName(u"safeMargCB")
        self.safeMargCB.setGeometry(QRect(70, 0, 151, 31))
        self.safeMargCB.setChecked(True)
        self.safeMargCB.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.retranslateUi(LogoEditWindow)
        # self.buttonBox.accepted.connect()
        # self.buttonBox.rejected.connect()

        QMetaObject.connectSlotsByName(LogoEditWindow)
    # setupUi

    def retranslateUi(self, LogoEditWindow):
        LogoEditWindow.setWindowTitle(QCoreApplication.translate("LogoEditWindow", u"Logo Editing", None))
        self.safeMargCB.setText(QCoreApplication.translate("LogoEditWindow", u"Safe Margins",None))
    # retranslateUi

