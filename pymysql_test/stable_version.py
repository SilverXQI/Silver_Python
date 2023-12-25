from pymysql import Connection
import pandas as pd


def import_init_data():
    try:
        conn = Connection(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            autocommit=True  # 自动提交事务，不然无法保存新建或者修改的数据
        )
        DataBase = 'StudentSystemNew'
        cursor = conn.cursor()
        conn.select_db(DataBase)
        # 读取 xlsx 文件到 DataFrame
        df = pd.read_excel('DataNew.xlsx', sheet_name='Course')
        for i in range(len(df)):
            sql = "insert into Course values ('%s','%s','%s','%s')" % (
                df['Cid'][i], df['Cname'][i], df['Ccredit'][i], df['Ctype'][i])
            # print(sql)
            cursor.execute(sql)
        df = pd.read_excel('DataNew.xlsx', sheet_name='Department')
        for i in range(len(df)):
            sql = "insert into Department values ('%s','%s','%s')" % (df['Did'][i], df['Dname'][i],df['Doffice'][i])
            # print(sql)
            cursor.execute(sql)
        df = pd.read_excel('DataNew.xlsx', sheet_name='Student')
        for i in range(len(df)):
            sql = "insert into Student values ('%s','%s','%s','%s','%s')" % (
                df['Sid'][i], df['Sname'][i], df['Ssex'][i], df['Sbirth'][i], df['Sdept'][i])
            # print(sql)
            cursor.execute(sql)
        df = pd.read_excel('DataNew.xlsx', sheet_name='Teacher')
        for i in range(len(df)):
            sql = "insert into Teacher values ('%s','%s','%s')" % (df['Tid'][i], df['Tname'][i],df['Tage'][i])
            # print(sql)
            cursor.execute(sql)
        df = pd.read_excel('DataNew.xlsx', sheet_name='SC')
        # print(df)
        for i in range(len(df)):
            sql = "insert into SC values ('%s','%s','%s','%s','%s')" % (
                df['Sid'][i], df['Cid'][i], df['Tid'][i], df['Grade'][i], df['IsPassed'][i])
            # print(sql)
            cursor.execute(sql)
    except Exception as e:
        print("error:", e, '初始数据已导入')


def Did_to_Dname(cursor, Did):
    try:
        sql = 'select Dname from Department where Did="%s"' % Did
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print("error:", e, '该专业不存在')
        return None


def Sid_to_Sname(cursor, Sid):
    try:
        sql = 'select Sname from Student where Sid="%s"' % Sid
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print("error:", e, '该生不存在')
        return None

def Sname_to_Sid(cursor,Sname):
    try:
        sql = 'select Sid from Student where Sname="%s"' % Sname
        cursor.execute(sql)
        result = cursor.fetchall()
        return result[0][0]
    except Exception as e:
        print("error:", e, '该生不存在')
        return None


# 1.录入一位学生，应包含学号、姓名、性别、出生年月、班级等信息
def add_student(cursor):
    print("录入一位学生，应包含学号、姓名、性别、生日、专业等信息")
    print("请输入学生信息：")
    Sid = input("学号：")
    Sname = input("姓名：")
    Ssex = input("性别：")
    Sbirth = input("生日：")
    Sdept = input("学院：")
    try:
        sql = "insert into Student values ('%s','%s','%s','%s','%s')" % (Sid, Sname, Ssex, Sbirth, Sdept)
        cursor.execute(sql)
        print("录入成功")
    except Exception as e:
        print("error:", e, '该生已存在')


# 2.按学号、姓名、专业三种方式查询学生基本信息
def query_student(cursor):
    print("按学号、姓名、专业三种方式查询学生基本信息")
    print("请输入查询方式：")
    print("1.按学号查询")
    print("2.按姓名查询")
    print("3.按专业查询")
    user_input = input("请输入您的选择：")
    if user_input == '1':
        Sid = input("请输入学号：")
        try:
            sql = "select * from Student where Sid='%s'" % Sid
            cursor.execute(sql)
            result = cursor.fetchall()
            dname = Did_to_Dname(cursor, result[0][4])
            print('学号：', result[0][0], '姓名：', result[0][1], '性别：', result[0][2], '生日：', result[0][3], '学院：',
                  dname)
        except Exception as e:
            print("error:", e, '该生不存在')
    elif user_input == '2':
        Sname = input("请输入姓名：")
        try:
            sql = "select * from Student where Sname='%s'" % Sname
            cursor.execute(sql)
            result = cursor.fetchall()
            dname = Did_to_Dname(cursor, result[0][4])
            print('学号：', result[0][0], '姓名：', result[0][1], '性别：', result[0][2], '生日：', result[0][3], '专业：',
                  dname)
        except Exception as e:
            print("error:", e, '该生不存在')
    elif user_input == '3':
        print("1.CS  2.AI  3.CE  4.NS 5.EIE 6.PH")
        dept = ['CS', 'AI', 'CE', 'NS', 'EIE', 'PH']
        SdeptIndex = input("请输入专业：")
        Sdept = dept[int(SdeptIndex) - 1]
        dname = Did_to_Dname(cursor, Sdept)
        try:
            sql = "select * from Student where Sdept='%s'" % Sdept
            cursor.execute(sql)
            result = cursor.fetchall()
            print(dname, ':', end='\n')
            for r in result:
                print('学号：', r[0], '姓名：', r[1], '性别：', r[2], '生日：', r[3])
        except Exception as e:
            print("error:", e, '该生不存在')
    else:
        print("输入错误")


# 3.录入一位学生一门课的成绩
def add_grade(cursor):
    print("录入一位学生一门课的成绩")
    print("请输入学生信息：")
    Sid = input("学号：")
    Cid = input("课程号：")
    Tid = input("教师号：")
    Grade = input("成绩：")
    IsPassed = 1 if int(Grade) >= 60 else 0
    try:
        sql = "insert into SC values ('%s','%s','%s','%s','%s')" % (Sid, Cid, Tid, Grade, IsPassed)
        cursor.execute(sql)
        print("录入成功")
    except Exception as e:
        print("error:", e, '该生已有该课程成绩')


# 4.查询一位学生所修的课程、性质（必修或选修）、学分及成绩；
def query_student_grade(cursor):
    print("查询一位学生所修的课程、性质（必修或选修）、学分及成绩；"
          "查询他的必修课平均成绩、所有课程平均成绩（平均成绩应按学分加权）")
    print("请输入学生信息：")
    print('1.按学号查询  2.按姓名查询')
    user_input = input("请输入您的选择：")
    if user_input == '1':
        Sid = input("学号：")
    elif user_input == '2':
        Sname = input("姓名：")
        Sid = Sname_to_Sid(cursor, Sname)
    try:
        sql = "select Sid,Cname,Ctype,Ccredit,Grade from SC,course where Sid='%s' and SC.Cid=course.Cid" % Sid
        cursor.execute(sql)
        result = cursor.fetchall()
        required_course_grade = 0
        required_course_credit = 0
        all_course_grade = 0
        all_course_credit = 0
        for r in result:
            print('课程名：', r[1], '性质：', '必修' if r[2] == 1 else '选修', '学分：', r[3], '成绩：', r[4])
            if r[2] == 1:
                required_course_grade += r[3] * r[4]
                required_course_credit += r[3]
            all_course_grade += r[3] * r[4]
            all_course_credit += r[3]
        print('必修课平均成绩：%.2f' % (required_course_grade / required_course_credit))
        print('所有课程平均成绩：%.2f' % (all_course_grade / all_course_credit))
    except Exception as e:
        print("error:", e, '该生成绩异常')


# 5.查询一位学生被哪些教师教过课
def query_student_teacher(cursor):
    print("查询一位学生被哪些教师教过课")
    print("请输入学生信息：")
    Sid = input("学号：")
    try:
        sql = "select Tname ,Cname from SC,Teacher,course where Sid='%s' and SC.Tid=Teacher.Tid and SC.Cid=course.Cid" % Sid
        cursor.execute(sql)
        result = cursor.fetchall()
        for r in result:
            # print('教师名：%-*s' % r[0], '课程名：%s'% r[1])
            print("教师名：%-*s 课程名：%s" % (12 - len(r[0]), r[0], r[1]))
    except Exception as e:
        print("error:", e, '该生数据异常')


# 6.查询快要被开除的学生（距被开除差3学分之内）学生达到如下条件之一的被开除：不及格必修课累计达10学分、或不及格选修课累计达15学分
def query_all_student_is_expelled(cursor):
    print("查询快要被开除的学生（距被开除差3学分之内）")
    try:
        sql = 'select Student.Sid,Student.Sname,' \
              'sum(case when course.Ctype=0 and sc.IsPassed=0 then course.Ccredit else 0 end) as failing_elective_course_credit,' \
              'sum(case when course.Ctype=1 and sc.IsPassed=0 then course.Ccredit else 0 end) as failing_required_course_credit ' \
              'from SC,course,Student where SC.Cid=course.Cid and SC.Sid=Student.Sid group by Sid '
        cursor.execute(sql)
        result = cursor.fetchall()
        for r in result:
            if r[3] > 10 or r[2] > 15:
                print('学号：', r[0], '姓名：', r[1], end=' ')
                print("已开除")
            elif 10 >= r[3] >= 7 or 15 >= r[2] >= 12:
                print('学号：', r[0], '姓名：', r[1], end=' ')
                print("快要被开除")
            else:
                pass
                # print('学号：', r[0], '姓名：', r[1], end=' ')
                # print("没有被开除")
    except Exception as e:
        print("error:", e, '该生成绩异常')


# 7.查询一位学生是否被开除；
def query_student_is_expelled(cursor):
    print("请输入学生信息：")
    print('1.按学号查询  2.按姓名查询')
    user_input = input("请输入您的选择：")
    if user_input == '1':
        Sid = input("学号：")
    elif user_input == '2':
        Sname = input("姓名：")
        Sid = Sid_to_Sname(cursor, Sname)
    else:
        print("输入错误")
        return
    try:
        sql = "select Sid,Cname,Ctype,Ccredit,Grade from SC,course where Sid='%s' and SC.Cid=course.Cid" % Sid
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
            print("该生已被开除")
        elif 10 >= failing_required_course_credit >= 7 or 15 >= failing_elective_course_credit >= 12:
            print("该生快要被开除")
        else:
            print("该生没有被开除")
    except Exception as e:
        print("error:", e, '该生成绩异常')


# 界面
def UI():
    print("---------------------------------")
    print("欢迎使用学生管理系统")
    print("1.录入一位学生，应包含学号、姓名、性别、出生年月、班级等信息")
    print("2.按学号、姓名、专业三种方式查询学生基本信息")
    print("3.录入一位学生一门课的成绩")
    print("4.查询一位学生所修的课程、性质（必修或选修）、学期、学分及成绩；"
          "查询他的必修课平均成绩、所有课程平均成绩（平均成绩应按学分加权）")
    print("5.查询一位学生被哪些教师教过课")
    print("6.查询快要被开除的学生（距被开除差3学分之内）")
    print("7.查询一位学生是否被开除；")
    print('0.退出')
    print("----------------------------------")


if __name__ == '__main__':
    import_init_data()
    conn = Connection(
        host='localhost',  # 用户
        port=3306,  # 端口号
        user='root',  # 用户名
        password='123456',  # 密码
        autocommit=True  # 自动提交事务，不然无法保存新建或者修改的数据
    )
    DataBase = 'StudentSystemNew'
    cursor = conn.cursor()
    conn.select_db(DataBase)
    while True:
        UI()
        user_input = input("请输入您的选择：")
        if user_input == '1':
            add_student(cursor)
        elif user_input == '2':
            query_student(cursor)
        elif user_input == '3':
            add_grade(cursor)
        elif user_input == '4':
            query_student_grade(cursor)
        elif user_input == '5':
            query_student_teacher(cursor)
        elif user_input == '6':
            query_all_student_is_expelled(cursor)
        elif user_input == '7':
            query_student_is_expelled(cursor)
        elif user_input == '0':
            break
        else:
            print("输入错误")
    conn.close()
