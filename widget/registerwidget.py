from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog
from PySide6.QtCore import Qt
from widget.ui_registerwidget_mode import Ui_RegisterWidget  # 使用新版UI
from lib.share import SI
from database.connector import Connector

import os
import shutil


class RegisterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_RegisterWidget()
        self.__ui.setupUi(self)

        self.__ui.m_returnButton.clicked.connect(self.returnLogin)
        self.__ui.m_registerButton.clicked.connect(self.register)

        # 人脸图片选择（新版 UI 中，“选择”按钮对象名为 m_returnButton_2）
        self._selected_face_path = None  # 本次注册选择的人脸图片绝对路径
        if hasattr(self.__ui, 'm_returnButton_2'):
            self.__ui.m_returnButton_2.clicked.connect(self.selectFaceImage)

    def selectFaceImage(self):
        """
        打开文件选择对话框，只允许选择 .jpg 图片。
        选中后把路径保存到 self._selected_face_path。
        """
        file_path, _ = QFileDialog.getOpenFileName(self, '选择人脸图片', '', 'JPEG 图片 (*.jpg)')
        if not file_path:
            return
        if not file_path.lower().endswith('.jpg'):
            QMessageBox.information(self, '选择失败', '仅支持 .jpg 格式的人脸图片')
            return

        self._selected_face_path = file_path

    def returnLogin(self):
        # 优先按对象名跳转，避免硬编码索引错误
        from PySide6.QtWidgets import QWidget as _QW
        reader_login_widget = SI.g_mainWindow.findChild(_QW, 'm_readerLoginWidget')
        if reader_login_widget is not None:
            SI.g_mainWindow.setCurrentWidget(reader_login_widget)
        else:
            # 回退到首页（原工程 index=0 通常是首页）
            SI.g_mainWindow.setCurrentIndex(0)

    def register(self):
        name = self.__ui.m_nameLlineEdit.text().strip()
        phone = self.__ui.m_mobileLineEdit_2.text().strip()   # 手机号（主键）
        email = self.__ui.m_mobileLineEdit.text().strip()      # email（UI命名如此）
        category = self.__ui.m_roleComboBox.currentText().strip()
        password = self.__ui.m_passwordLineEdit.text().strip()
        password_confirm = self.__ui.m_passwordConfirmLineEdit.text().strip()

        if name == '' or phone == '' or password == '':
            QMessageBox.information(self, '注册失败', '姓名、手机号、密码不能为空')
            return

        if password != password_confirm:
            QMessageBox.information(self, '注册失败', '两次输入的密码不一致')
            return

        # 如果选择了头像，强制校验扩展名为 .jpg
        if self._selected_face_path is not None and (not self._selected_face_path.lower().endswith('.jpg')):
            QMessageBox.information(self, '注册失败', '仅支持 .jpg 格式的人脸图片')
            return

        cursor = Connector.get_cursor()

        # 检查手机号是否已存在
        sql_check = 'SELECT 1 FROM user WHERE phone_number = %s LIMIT 1'
        cursor.execute(sql_check, (phone,))
        if cursor.fetchone() is not None:
            QMessageBox.information(self, '注册失败', '该手机号已注册')
            return

        # 插入用户：face_id 为空；sex/unit 暂时占位
        sql_insert = '''
            INSERT INTO user (phone_number, u_name, email, category, password, face_id, balance, sex, unit)
            VALUES (%s, %s, %s, %s, %s, %s, 0.00, %s, %s)
        '''
        cursor.execute(sql_insert, (phone, name, email, category, password, None, '未知', ''))
        Connector.get_connection()

        # 保存头像：复制到 ./reader_img/<phone>.jpg
        if self._selected_face_path is not None:
            try:
                from lib.face_login import ensure_reader_img_dir, READER_IMG_DIR
                ensure_reader_img_dir()
                dest_path = os.path.join(READER_IMG_DIR, f'{phone}.jpg')
                shutil.copyfile(self._selected_face_path, dest_path)
            except Exception as e:
                # 头像保存失败不影响账号创建，但提示无法使用人脸登录
                QMessageBox.warning(self, '提示', f'账号创建成功，但人脸图片保存失败：{e}\n'
                                                  f'你可以稍后手动将 .jpg 头像文件命名为 {phone}.jpg 放到 ./reader_img 目录中。')

        QMessageBox.information(self, '注册成功', '注册成功，请登录')

        # 跳回“读者登录”页（按对象名查找，避免索引错乱）
        from PySide6.QtWidgets import QWidget as _QW
        reader_login_widget = SI.g_mainWindow.findChild(_QW, 'm_readerLoginWidget')
        if reader_login_widget is not None:
            SI.g_mainWindow.setCurrentWidget(reader_login_widget)
        else:
            # 回退方案：若未找到对象名，退回首页或你原先约定的读者登录索引
            SI.g_mainWindow.setCurrentIndex(0)