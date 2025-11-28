# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'administerloginwidget_mode.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_AdministerLoginWidget(object):
    def setupUi(self, AdministerLoginWidget):
        if not AdministerLoginWidget.objectName():
            AdministerLoginWidget.setObjectName(u"AdministerLoginWidget")
        AdministerLoginWidget.resize(796, 568)
        self.label = QLabel(AdministerLoginWidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(340, 90, 105, 26))
        font = QFont()
        font.setFamilies([u"\u9ed1\u4f53"])
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.m_loginButton = QPushButton(AdministerLoginWidget)
        self.m_loginButton.setObjectName(u"m_loginButton")
        self.m_loginButton.setGeometry(QRect(263, 410, 81, 24))
        self.m_returnButton = QPushButton(AdministerLoginWidget)
        self.m_returnButton.setObjectName(u"m_returnButton")
        self.m_returnButton.setGeometry(QRect(390, 410, 75, 24))
        self.label_3 = QLabel(AdministerLoginWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(280, 306, 36, 16))
        self.m_passwordLineEdit = QLineEdit(AdministerLoginWidget)
        self.m_passwordLineEdit.setObjectName(u"m_passwordLineEdit")
        self.m_passwordLineEdit.setGeometry(QRect(322, 306, 132, 20))
        self.m_passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.m_accountLineEdit = QLineEdit(AdministerLoginWidget)
        self.m_accountLineEdit.setObjectName(u"m_accountLineEdit")
        self.m_accountLineEdit.setGeometry(QRect(322, 190, 132, 20))
        self.label_2 = QLabel(AdministerLoginWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 190, 36, 16))

        self.retranslateUi(AdministerLoginWidget)

        QMetaObject.connectSlotsByName(AdministerLoginWidget)
    # setupUi

    def retranslateUi(self, AdministerLoginWidget):
        AdministerLoginWidget.setWindowTitle(QCoreApplication.translate("AdministerLoginWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("AdministerLoginWidget", u"\u7ba1\u7406\u5458\u767b\u5f55", None))
        self.m_loginButton.setText(QCoreApplication.translate("AdministerLoginWidget", u"\u5f00\u59cb\u4eba\u8138\u9a8c\u8bc1", None))
        self.m_returnButton.setText(QCoreApplication.translate("AdministerLoginWidget", u"\u8fd4\u56de", None))
        self.label_3.setText(QCoreApplication.translate("AdministerLoginWidget", u"\u5bc6\u7801\uff1a", None))
        self.m_passwordLineEdit.setText("")
        self.m_accountLineEdit.setText("")
        self.label_2.setText(QCoreApplication.translate("AdministerLoginWidget", u"\u5e10\u53f7\uff1a", None))
    # retranslateUi

