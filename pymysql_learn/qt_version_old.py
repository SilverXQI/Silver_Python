import sys

from PyQt5.QtWidgets import *
from pymysql import Connection

Did_to_Dname = {'CS_SE': '软件与理论方向', 'CS_AI': '数据智能方向', 'CS_ES': '嵌入式方向',
                'CS_NS': '网络与信息安全方向'}


def Tid_to_Tname(cursor, Tid):
    try:
        sql = "select Tname from Teacher where Tid = '%s'" % Tid
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)R
        return result[0][0]
    except Exception as e:
        print("error:", e, '该教师不存在')
        return None


def Cid_to_Cname(cursor, Cid):
    try:
        sql = "select Cname from Course where Cid = '%s'" % Cid
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print("error:", e, '该课不存在')
        return None


def Sname_to_Sid(cursor, Sname):
    try:
        sql = 'select Sid from Student where Sname="%s"' % Sname
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print("error:", e, '该生不存在')
        return None


class StudentSystemApp():
    def __init__(self):
        super().__init__()

    def add_student(self, cursor, Sid, Sname, Ssex, Sage, Sdept):
        try:
            sql = "insert into Student values ('%s','%s','%s','%s','%s')" % (Sid, Sname, Ssex, Sage, Sdept)
            cursor.execute(sql)
            print("录入成功")
            return True
        except Exception as e:
            print("error:", e, '该生已存在')
            return False


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.close_app = False  # 添加一个标志以确定是否应该关闭应用程序

    def initUI(self):
        # 主界面布局
        layout = QVBoxLayout()

        # 功能按钮列表
        buttons = [
            ('录入学生信息', self.enter_student_info),
            ('查询学生信息', self.search_student_info),
            ('录入学生成绩', self.enter_student_grade),
            ('查询学生课程和成绩', self.query_student_courses),
            ('查询学生的教师', self.query_student_teachers),
            ('查询快要被开除的学生', self.query_students_near_expulsion),
            ('查询学生是否被开除', self.query_student_expulsion),
            ('退出', self.exit_app)
        ]

        # 为每个功能创建按钮并添加到布局
        for btn_text, btn_slot in buttons:
            button = QPushButton(btn_text, self)
            button.clicked.connect(btn_slot)
            layout.addWidget(button)

        # 设置布局
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 设置窗口标题和大小
        self.setWindowTitle('学生管理系统')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    # 下面定义所有功能按钮的槽函数
    def enter_student_info(self):
        self.function_window = EnterStudentInfoWindow(self)
        self.function_window.show()
        self.hide()

    def search_student_info(self):
        self.function_window = SearchStudentInfoWindow(self)
        self.function_window.show()
        self.hide()

    def enter_student_grade(self):
        self.function_window = EnterStudentGradeWindow(self)
        self.function_window.show()
        self.hide()

    def query_student_courses(self):
        self.function_window = QueryStudentCoursesWindow(self)
        self.function_window.show()
        self.hide()

    def query_student_teachers(self):
        self.function_window = QueryStudentTeachersWindow(self)
        self.function_window.show()
        self.hide()

    def query_students_near_expulsion(self):
        self.function_window = QueryStudentsNearExpulsionWindow(self)
        self.function_window.show()
        self.hide()

    def query_student_expulsion(self):
        self.function_window = QueryStudentExpulsionWindow(self)
        self.function_window.show()
        self.hide()

    # 用于正常退出应用程序的方法
    def exit_app(self):
        self.close_app = True  # 设置标志为 True
        self.close()  # 尝试关闭窗口，这将触发 closeEvent

    def closeEvent(self, event):
        # 如果 self.close_app 为 True，则退出应用程序
        if self.close_app:
            event.accept()  # 接受关闭事件，将关闭应用程序
        else:
            event.ignore()  # 忽略关闭事件，仅隐藏窗口
            self.hide()  # 隐藏窗口


# 功能窗口类的定义
# 1. 录入学生信息
class EnterStudentInfoWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window
        self.ssa = StudentSystemApp()

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
        # 添加一个标签用于显示操作结果
        self.resultLabel = QLabel('')
        layout.addWidget(self.resultLabel)

        submitButton.clicked.connect(self.addStudent)
        self.back_button.clicked.connect(self.back_to_main)

        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

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

        res_flag = self.ssa.add_student(cursor, sid, sname, ssex, sage, sdept)
        if res_flag:
            self.resultLabel.setText("录入成功")  # 设置标签文本为“录入成功”
            # 清空输入框以便下一次录入
            self.sidInput.clear()
            self.snameInput.clear()
            self.ssexInput.clear()
            self.sageInput.clear()
            self.sdeptInput.clear()
        else:
            self.resultLabel.setText("录入失败: 该生已存在")  # 设置标签文本为“录入失败”

        conn.close()
        print("添加学生")  # 调试输出


# 2. 查询学生信息
class SearchStudentInfoWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        submitButton = QPushButton('查询学生信息', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(QLabel('学号'))
        layout.addWidget(self.sidInput)
        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)

        submitButton.clicked.connect(self.searchStudent)
        self.back_button.clicked.connect(self.back_to_main)
        # 创建文本编辑器
        self.resultsTextEdit = QTextEdit(self)
        self.resultsTextEdit.setReadOnly(True)  # 设置为只读，不允许用户编辑

        layout.addWidget(self.resultsTextEdit)  # 将文本编辑器添加到布局中
        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

    def set_main_window(self, main_window):
        self.main_window = main_window

    def searchStudent(self):
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

        try:
            # 使用参数化查询来提高安全性
            sql = "select * from Student where Sid = '%s'" % sid
            cursor.execute(sql)
            result = cursor.fetchall()
            self.displayResults(result)
            print(result)
        except Exception as e:
            print("查询失败:", e)
        finally:
            conn.close()
        print("查询学生信息")  # 调试输出

    def displayResults(self, results):
        # 清空当前内容
        self.resultsTextEdit.clear()
        res_data = results[0]
        res = '学号: ' + res_data[0] + '\n' + '姓名: ' + res_data[1] + '\n' + '性别: ' + res_data[
            2] + '\n' + '年龄: ' + str(
            res_data[3]) + '\n' + '专业: 计算机科学与技术' + '\n' + '方向:' + Did_to_Dname[res_data[4]]
        self.resultsTextEdit.append(res)


# 3. 录入学生成绩
class EnterStudentGradeWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        self.cidInput = QLineEdit(self)
        self.tidInput = QLineEdit(self)
        self.gradeInput = QLineEdit(self)
        # self.isPassedInput = QLineEdit(self)
        submitButton = QPushButton('录入学生成绩', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(QLabel('学号'))
        layout.addWidget(self.sidInput)
        layout.addWidget(QLabel('课程号'))
        layout.addWidget(self.cidInput)
        layout.addWidget(QLabel('教师号'))
        layout.addWidget(self.tidInput)
        layout.addWidget(QLabel('成绩'))
        layout.addWidget(self.gradeInput)
        # layout.addWidget(QLabel('是否及格'))
        # layout.addWidget(self.isPassedInput)
        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)
        self.resultLabel = QLabel('')
        layout.addWidget(self.resultLabel)

        submitButton.clicked.connect(self.addStudent)
        self.back_button.clicked.connect(self.back_to_main)

        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        # 使用 self.parent() 显示主窗口
        # if self.main_window:
        #     self.main_window.show_main_window()
        # self.hide()
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

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
        cid = self.cidInput.text()
        tid = self.tidInput.text()
        grade = self.gradeInput.text()
        # isPassed = self.isPassedInput.text()
        isPassed = 1 if int(grade) >= 60 else 0
        try:
            # 使用参数化查询来提高安全性
            sql = "insert into SC values ('%s','%s','%s','%s','%s')" % (sid, cid, tid, grade, isPassed)
            cursor.execute(sql)
            self.resultLabel.setText("录入成功")  # 设置标签文本为“录入成功”
            print("录入成功")
        except Exception as e:
            self.resultLabel.setText("录入失败，该生成绩已存在")  # 设置标签文本为“录入失败”
            print("录入失败:", e)
        finally:
            conn.close()
        print("添加学生")  # 调试输出


# 4. 查询学生课程和成绩
class QueryStudentCoursesWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        submitButton = QPushButton('查询学生课程和成绩', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(QLabel('学号'))
        layout.addWidget(self.sidInput)
        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)

        submitButton.clicked.connect(self.searchStudent)
        self.back_button.clicked.connect(self.back_to_main)
        # 创建表格
        self.resultsTable = QTableWidget(self)
        self.resultsTable.setColumnCount(5)  # 假设有5列数据：学号、姓名、性别、出生年月、班级
        self.resultsTable.setHorizontalHeaderLabels(['学号', '课程名', '教师', '成绩', '是否通过'])

        layout.addWidget(self.resultsTable)  # 将表格添加到布局中
        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

    def set_main_window(self, main_window):
        self.main_window = main_window

    def searchStudent(self):
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

        try:
            # 使用参数化查询来提高安全性
            sql = "select * from SC where Sid = '%s'" % sid
            cursor.execute(sql)
            result = cursor.fetchall()
            list_result = list(result)
            for i in range(len(list_result)):
                list_result[i] = list(list_result[i])
                list_result[i][1] = Cid_to_Cname(cursor, list_result[i][1])
                list_result[i][2] = Tid_to_Tname(cursor, list_result[i][2])
                list_result[i][4] = '是' if list_result[i][4] == 1 else '否'
            if len(list_result) == 0:
                list_result.append(['无', '无', '无', '无', '无'])
            self.displayResults(list_result)
            print(list_result)
        except Exception as e:
            print("查询失败:", e)
        finally:
            conn.close()
        print("查询学生信息")  # 调试输出
    def displayResults(self, results):
        self.resultsTable.setRowCount(len(results))  # 设置行数
        for row_num, row_data in enumerate(results):
            for column_num, data in enumerate(row_data):
                self.resultsTable.setItem(row_num, column_num, QTableWidgetItem(str(data)))


# 5. 查询学生的教师
class QueryStudentTeachersWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        submitButton = QPushButton('查询学生的教师', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(QLabel('学号'))
        layout.addWidget(self.sidInput)
        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)

        submitButton.clicked.connect(self.searchStudent)
        self.back_button.clicked.connect(self.back_to_main)
        # 创建表格
        self.resultsTable = QTableWidget(self)
        self.resultsTable.setColumnCount(2)  # 假设有5列数据：学号、姓名、性别、出生年月、班级
        self.resultsTable.setHorizontalHeaderLabels(['教师', '课程名'])

        layout.addWidget(self.resultsTable)  # 将表格添加到布局中
        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        # 使用 self.parent() 显示主窗口
        # if self.main_window:
        #     self.main_window.show_main_window()
        # self.hide()
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

    def set_main_window(self, main_window):
        self.main_window = main_window

    def searchStudent(self):
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

        try:
            sql = "select Tname ,Cname from SC,Teacher,course where Sid='%s' and SC.Tid=Teacher.Tid and SC.Cid=course.Cid" % sid
            cursor.execute(sql)
            result = cursor.fetchall()
            list_result = list(result)
            for i in range(len(list_result)):
                list_result[i] = list(list_result[i])
            if len(list_result) == 0:
                list_result.append(['无', '无'])
            self.displayResults(list_result)
            print(list_result)
            # self.displayResults(result)
            # print(result)
        except Exception as e:
            print("查询失败:", e)
        finally:
            conn.close()
        print("查询学生信息")  # 调试输出

    def displayResults(self, results):
        self.resultsTable.setRowCount(len(results))
        for row_num, row_data in enumerate(results):
            for column_num, data in enumerate(row_data):
                self.resultsTable.setItem(row_num, column_num, QTableWidgetItem(str(data)))


# 6. 查询快要被开除的学生
class QueryStudentsNearExpulsionWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window

    def initUI(self):
        layout = QVBoxLayout()

        submitButton = QPushButton('查询快要被开除的学生', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)

        submitButton.clicked.connect(self.searchStudent)
        self.back_button.clicked.connect(self.back_to_main)
        # 创建表格
        self.resultsTable = QTableWidget(self)
        self.resultsTable.setColumnCount(3)  # 假设有5列数据：学号、姓名、性别、出生年月、班级
        self.resultsTable.setHorizontalHeaderLabels(['学号', '姓名', '状态'])

        layout.addWidget(self.resultsTable)  # 将表格添加到布局中
        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        # 使用 self.parent() 显示主窗口
        # if self.main_window:
        #     self.main_window.show_main_window()
        # self.hide()
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

    def set_main_window(self, main_window):
        self.main_window = main_window

    def searchStudent(self):
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
        try:
            sql = 'select Student.Sid,Student.Sname,' \
                  'sum(case when course.Ctype=0 and sc.IsPassed=0 then course.Ccredit else 0 end) as failing_elective_course_credit,' \
                  'sum(case when course.Ctype=1 and sc.IsPassed=0 then course.Ccredit else 0 end) as failing_required_course_credit ' \
                  'from SC,course,Student where SC.Cid=course.Cid and SC.Sid=Student.Sid group by Sid '
            cursor.execute(sql)
            result = cursor.fetchall()
            list_result = []
            for r in result:
                if r[3] > 10 or r[2] > 15:
                    list_result.append([r[0], r[1], '已经被开除'])
                elif 10 >= r[3] >= 7 or 15 >= r[2] >= 12:
                    list_result.append([r[0], r[1], '快要被开除'])
                else:
                    pass
                    # print('学号：', r[0], '姓名：', r[1], end=' ')
                    # print("没有被开除")
            print(list_result)
            self.displayResults(list_result)
        except Exception as e:
            print("error:", e, '该生成绩异常')

    def displayResults(self, results):
        self.resultsTable.setRowCount(len(results))
        for row_num, row_data in enumerate(results):
            for column_num, data in enumerate(row_data):
                self.resultsTable.setItem(row_num, column_num, QTableWidgetItem(str(data)))


# 7. 查询学生是否被开除
class QueryStudentExpulsionWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.initUI()
        self.main_window = main_window

    def initUI(self):
        layout = QVBoxLayout()

        self.sidInput = QLineEdit(self)
        self.snameInput = QLineEdit(self)
        submitButton = QPushButton('查询学生是否被开除', self)
        self.back_button = QPushButton('Back to Main', self)

        layout.addWidget(QLabel('学号'))
        layout.addWidget(self.sidInput)
        layout.addWidget(QLabel('姓名'))
        layout.addWidget(self.snameInput)
        layout.addWidget(submitButton)
        layout.addWidget(self.back_button)

        submitButton.clicked.connect(self.searchStudent)
        self.back_button.clicked.connect(self.back_to_main)
        # 创建表格
        self.resultsTable = QTableWidget(self)
        self.resultsTable.setColumnCount(1)  # 假设有5列数据：学号、姓名、性别、出生年月、班级
        self.resultsTable.setHorizontalHeaderLabels(['状态'])

        layout.addWidget(self.resultsTable)  # 将表格添加到布局中
        self.setLayout(layout)
        self.setWindowTitle('学生管理系统')
        # self.show()

    def back_to_main(self):
        print("返回主界面")  # 调试输出
        # 使用 self.parent() 显示主窗口
        # if self.main_window:
        #     self.main_window.show_main_window()
        # self.hide()
        self.close()  # 关闭功能窗口
        self.main_window.show()  # 显示主窗口

    def set_main_window(self, main_window):
        self.main_window = main_window

    def searchStudent(self):
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
        # print("请输入学生信息：")
        # print('1.按学号查询  2.按姓名查询')
        # user_input = input("请输入您的选择：")
        sid = self.sidInput.text()
        sname = self.snameInput.text()
        if sid:
            print(sid)
        elif sname:
            print(sname)
            sid = Sname_to_Sid(cursor, sname)
        else:
            print("输入错误")
            return
        try:
            sql = "select Sid,Cname,Ctype,Ccredit,Grade from SC,course where Sid='%s' and SC.Cid=course.Cid" % sid
            cursor.execute(sql)
            result = cursor.fetchall()
            failing_elective_course_credit = 0
            failing_required_course_credit = 0
            for r in result:
                if r[2] == 1 and r[4] < 60:
                    failing_required_course_credit += r[3]
                elif r[2] == 0 and r[4] < 60:
                    failing_elective_course_credit += r[3]
            if failing_required_course_credit > 10 or failing_elective_course_credit > 15:
                res = '已经被开除'
            elif 10 >= failing_required_course_credit >= 7 or 15 >= failing_elective_course_credit >= 12:
                res = '快要被开除'
            else:
                res = '没有被开除'
        except Exception as e:
            print("error:", e, '该生成绩异常')
            res = '该生成绩异常'
        self.displayResults(res)

    def displayResults(self, results):
        self.resultsTable.setRowCount(1)
        self.resultsTable.setItem(0, 0, QTableWidgetItem(results))


# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
