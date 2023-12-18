import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from pymysql import Connection


def add_student(cursor, Sid, Sname, Ssex, Sage, Sdept):
    try:
        sql = "insert into Student values ('%s','%s','%s','%s','%s')" % (Sid, Sname, Ssex, Sage, Sdept)
        cursor.execute(sql)
        print("录入成功")
    except Exception as e:
        print("error:", e, '该生已存在')


class StudentSystemApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        self.snameInput = QLineEdit(self)
        self.ssexInput = QLineEdit(self)
        self.sageInput = QLineEdit(self)
        self.sdeptInput = QLineEdit(self)
        submitButton = QPushButton('录入学生信息', self)

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

        submitButton.clicked.connect(self.addStudent)

        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        self.show()

    def addStudent(self):
        conn = Connection(
            host='localhost',  # 用户
            port=3306,  # 端口号
            user='root',  # 用户名
            password='123456',  # 密码
            autocommit=True  # 自动提交事务，不然无法保存新建或者修改的数据
        )
        DataBase = 'StudentSystemTest'
        cursor = conn.cursor()
        conn.select_db(DataBase)

        print("录入一位学生，应包含学号、姓名、性别、年龄、专业等信息")
        sid = self.sidInput.text()
        sname = self.snameInput.text()
        ssex = self.ssexInput.text()
        sage = self.sageInput.text()
        sdept = self.sdeptInput.text()
        # 这里调用您原始脚本中的 add_student 函数
        add_student(cursor,sid, sname, ssex, sage, sdept)
        conn.close()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = StudentSystemApp()
    sys.exit(app.exec_())
