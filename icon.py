from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon

class Icon:
    def __init__(self, parent, icon_path, app_name="My App"):
        self.parent = parent
        self.parent.setWindowIcon(QIcon(icon_path))
        self.parent.setWindowTitle(app_name)

        # إنشاء الأيقونة في شريط النظام
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), parent)
        self.tray_icon.setToolTip(app_name)

        # إنشاء القائمة المنبثقة
        self.tray_menu = QMenu()
        self.create_menu()

        # عرض الأيقونة في شريط النظام
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def create_menu(self):
        open_action = QAction("Open", self.tray_icon)
        open_action.triggered.connect(self.open_application)
        self.tray_menu.addAction(open_action)

        hide_action = QAction("Hide", self.tray_icon)
        hide_action.triggered.connect(self.hide_application)
        self.tray_menu.addAction(hide_action)

        notify_action = QAction("Show Notification", self.tray_icon)
        notify_action.triggered.connect(self.show_notification)
        self.tray_menu.addAction(notify_action)

        settings_action = QAction("Settings", self.tray_icon)
        settings_action.triggered.connect(self.open_settings)
        self.tray_menu.addAction(settings_action)

        exit_action = QAction("Exit", self.tray_icon)
        exit_action.triggered.connect(self.exit_application)
        self.tray_menu.addAction(exit_action)

    def open_application(self):
        self.parent.show()  # فتح التطبيق إذا كان مخفيًا

    def hide_application(self):
        self.parent.hide()  # إخفاء نافذة التطبيق

    def show_notification(self):
        self.tray_icon.showMessage("Notification", "This is a notification message", QIcon(self.icon_path), 3000)

    def open_settings(self):
        # فتح نافذة الإعدادات
        pass  # استبدل هذه بالدالة التي تعرض نافذة الإعدادات

    def exit_application(self):
        QApplication.quit()  # إغلاق التطبيق
