import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMainWindow
from pymysql import Connection




def add_student(cursor, Sid, Sname, Ssex, Sage, Sdept):
    try:
        sql = "insert into Student values ('%s','%s','%s','%s','%s')" % (Sid, Sname, Ssex, Sage, Sdept)
        cursor.execute(sql)
        print("录入成功")
    except Exception as e:
        print("error:", e, '该生已存在')


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建一个按钮，用于打开功能界面
        self.open_button = QPushButton('Open Student System', self)
        self.open_button.clicked.connect(self.open_student_system)

        # 初始化 StudentSystemApp 窗口但不显示
        self.student_system_app = StudentSystemApp()

        layout.addWidget(self.open_button)
        self.setLayout(layout)
        # self.setWindowTitle("主界面")
        # self.setGeometry(100, 100, 300, 200)
        #
        # self.open_button = QPushButton('Open Student System', self)
        # self.open_button.clicked.connect(self.open_student_system)
        # self.open_button.resize(self.open_button.sizeHint())
        # self.open_button.move(100, 80)
        #
        # self.student_system_app = StudentSystemApp()

    def open_student_system(self):
        print("打开学生系统")  # 调试输出
        # 显示功能界面，隐藏主界面
        self.student_system_app.show()
        self.hide()

    def show_main_window(self):
        self.show()


class StudentSystemApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.main_window = None

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        self.snameInput = QLineEdit(self)
        self.ssexInput = QLineEdit(self)
        self.sageInput = QLineEdit(self)
        self.sdeptInput = QLineEdit(self)
        submitButton = QPushButton('录入学生信息', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(QLabel('学号'))
        layout.addWidget(self.sidInput)
        layout.addWidget(QLabel('姓名'))
        layout.addWidget(self.snameInput)
        layout.addWidget(QLabel('性别'))
        layout.addWidget(self.ssexInput)
        layout.addWidget(QLabel('年龄'))
        layout.addWidget(self.sageInput)
        layout.addWidget(QLabel('专业'))
        layout.addWidget(self.sdeptInput)
        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)

        submitButton.clicked.connect(self.addStudent)
        self.back_button.clicked.connect(self.back_to_main)

        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        # 使用 self.parent() 显示主窗口
        if self.main_window:
            self.main_window.show_main_window()
        self.hide()

    def set_main_window(self, main_window):
        self.main_window = main_window

    def addStudent(self):
        conn = Connection(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            autocommit=True
        )
        DataBase = 'StudentSystemTest'
        cursor = conn.cursor()
        conn.select_db(DataBase)

        sid = self.sidInput.text()
        sname = self.snameInput.text()
        ssex = self.ssexInput.text()
        sage = self.sageInput.text()
        sdept = self.sdeptInput.text()

        try:
            add_student(cursor, sid, sname, ssex, sage, sdept)
            # self.hide()  # 隐藏当前窗口
        except Exception as e:
            print("录入失败:", e)
        finally:
            conn.close()
        print("添加学生")  # 调试输出


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    student_system_app = StudentSystemApp()
    student_system_app.set_main_window(main_app)  # 设置对主窗口的引用
    main_app.student_system_app = student_system_app  # 设置对子窗口的引用

    main_app.show()
    sys.exit(app.exec_())
