from PySide6.QtWidgets import QWidget, QMessageBox
from widget.ui_administerloginwidget_mode import Ui_AdministerLoginWidget  # 使用新版UI
from lib.share import SI
from database.connector import Connector


class AdministerLoginWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_AdministerLoginWidget()
        self.__ui.setupUi(self)

        # 返回首页
        self.__ui.m_returnButton.clicked.connect(lambda: SI.g_mainWindow.setCurrentIndex(0))
        # “开始人脸验证”按钮：执行“账号密码验证 + 人脸验证”
        self.__ui.m_loginButton.clicked.connect(self.startFaceVerifyLogin)

    def startFaceVerifyLogin(self):
        account = self.__ui.m_accountLineEdit.text().strip()
        password = self.__ui.m_passwordLineEdit.text().strip()

        if account == '' or password == '':
            QMessageBox.information(self, '登录失败', '请输入账号和密码')
            return

        # 1) 先验证账号密码
        cursor = Connector.get_cursor()
        sql = 'SELECT a_id FROM administer WHERE a_name = %s AND password = %s LIMIT 1'
        cursor.execute(sql, (account, password))
        row = cursor.fetchone()
        if row is None:
            QMessageBox.critical(self, '登录失败', '管理员账号或密码错误，请检查')
            return

        # 2) 账号密码正确后，开始人脸验证
        try:
            from lib.face_login_admin import run_admin_face_login, ensure_admin_img_dir
        except Exception:
            QMessageBox.critical(self, '人脸验证', '人脸识别依赖未安装，请先执行:\n\npip install face_recognition opencv-python')
            return

        ensure_admin_img_dir()
        recognized_account = run_admin_face_login(timeout_seconds=10, hold_on_recognition_seconds=1.0)

        if recognized_account is None:
            QMessageBox.information(self, '人脸验证失败', '人脸验证失败，请重试或检查 ./admin_img 下的管理员人脸图片')
            return

        # 人脸识别出的账号必须与输入账号一致，才能通过
        if recognized_account != account:
            QMessageBox.information(self, '人脸验证失败', f'识别到的账号为 {recognized_account}，与输入账号不一致')
            return

        # 双重验证通过，进入管理员界面
        from PySide6.QtWidgets import QWidget as _QW
        admin_widget = SI.g_mainWindow.findChild(_QW, 'm_adminWidget')
        if admin_widget is not None:
            SI.g_mainWindow.setCurrentWidget(admin_widget)
        else:
            # 回退：使用原工程的索引（若与你的工程不一致，请根据实际修改）
            SI.g_mainWindow.setCurrentIndex(5)

        # 如果有管理员界面的数据刷新方法，调用之
        if hasattr(SI.g_mainWindow, 'updateAdminWidget'):
            SI.g_mainWindow.updateAdminWidget()