import pymysql
from pymysql import Connection

User = "root"
Password = "123456"
DataBase = "StudentManageSystem"

# 数据库连接配置
# config = {
#     'host': 'localhost',  # 你的数据库地址
#     'port': 3306,  # 你的数据库端口号
#     'user': 'root',
#     'passwd': '123456',
#     'db': 'StudentManageSystem',
#     'charset': 'utf8mb4'
# }

# 创建连接
# conn = pymysql.connect(**config)
# print(conn.get_server_info())


conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    autocommit=True  # 自动提交事务，不然无法保存新建或者修改的数据
)

# 创建 cursor 对象
cursor = conn.cursor()
conn.select_db(DataBase)
cursor.execute("create database if not exists StudentManageSystem")
cursor.execute("select * from student")
result = cursor.fetchall()
for r in result:
    print(r)
conn.close()


# 执行 SQL 语句
# try:
#     # 创建表
#     cursor.execute("CREATE TABLE depart (de_cl_Num char(30), de_Name char(30), PRIMARY KEY (de_cl_Num));")
#     cursor.execute("CREATE TABLE teacher (teacherNum char(30) PRIMARY KEY, teacherName char(30));")
#     # ... 更多的 CREATE TABLE 语句 ...
#     cursor.execute(
#         "CREATE TABLE student(stuNum char(30) primary key,stuName char(30),stuSex enum ('M','F'),de_cl_Num char(30),foreign key (de_cl_Num) references depart (de_cl_Num));")
#
#     # 插入数据
#     cursor.execute("INSERT INTO depart VALUES ('0301058', 'computer_depart');")
#     # ... 更多的 INSERT INTO 语句 ...
#
#     # 提交事务
#     conn.commit()
# except pymysql.Error as e:
#     print("数据库错误:", e)
# except Exception as e:
#     print("错误:", e)
# finally:
#     # 关闭 cursor 和连接
#     cursor.close()
#     conn.close()


def QuerySQL(sql):
    coon = pymysql.connect(host="localhost", user=User, password=Password, database=DataBase)
    cursor = coon.cursor()
    result = ()
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        coon.rollback()
    finally:
        coon.close()
    return result


# 链接并执行MYSQL语句 #查询选修均分
def QueryScore0(stuNum):
    coon = pymysql.connect(host="localhost", user=User, password=Password, database=DataBase)
    cursor = coon.cursor()

    sql = "select avg(score) from teach left join course on teach.courseNum = course.courseNum where stuNum = '%s' and type = 0" % (
        stuNum)
    grade = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            gra = row[0]
            grade.append(gra)
            print(gra)
    except:
        print("发生错误")
        coon.close()
    return grade


# 查询必修成绩
def QueryScore1(stuNum):
    coon = pymysql.connect(host="localhost", user=User, password=Password, database=DataBase)
    cursor = coon.cursor()

    sql = "select avg(score) from teach left join course on teach.courseNum = course.courseNum where stuNum = '%s' and type = 1" % (
        stuNum)

    grade = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            gra = row[0]
            grade.append(gra)
            print(gra)
    except:
        print("发生错误")
        coon.close()
    return grade


# 查询授课教师
def Queryteacher(stuNum):
    coon = pymysql.connect(host="localhost", user=User, password=Password, database=DataBase)
    cursor = coon.cursor()

    sql = "select teacherName from teach left join course on teach.courseNum = course.courseNum where stuNum = '%s' " % (
        stuNum)

    teachers = []

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            teacher = row[0]
            teachers.append(teacher)
            print(teacher)
    except:
        print("发生错误")
        coon.close()
        return teachers


def QueryExpulsion(stuNum):
    coon = pymysql.connect(host="localhost", user=User, password=Password, database=DataBase)
    cursor = coon.cursor()

    sql1 = "select count(degree) as fail_require from teach left join course on teach.courseNum = course.courseNum where stuNum ='%s' and type =1 and score<60 " % (
        stuNum)
    sql2 = "select count(degree) as fail_require from teach left join course on teach.courseNum = course.courseNum where stuNum ='%s' and type =0 and score<60 " % (
        stuNum)

    failure = []

    try:
        cursor.execute(sql1)
        result = cursor.fetchall()
        for row in result:
            fail1 = row[0]
            failure.append(fail1)
            print("该生挂必修课总学分：")
            print(fail1)

        cursor.execute(sql2)
        result = cursor.fetchall()
        for row in result:
            fail2 = row[0]
            failure.append(fail2)
            print("该生挂选修课总学分：")
            print(fail2)

        if fail1 > 10:
            print("该生已被退学")
        elif fail2 > 20:
            print("该生已被退学")
        else:
            print("该生没有退学")
    except:
        print("发生错误")
        coon.close()
    return failure


def test():
    while True:
        choice = input("请选择要执行的操作:1、查询成绩 2、查询授课教师 3、查询退学")
        if choice == "1":
            ch = input("请输入查分选择：1、必修 0、选修")
            if ch == "1":
                stuNum = input("请输入学号：")
                QueryScore1(stuNum)
            else:
                stuNum = input("请输入学号：")
                QueryScore0(stuNum)
        elif choice == "2":
            stuNum = input("请输入学号以查询授课教师")
            Queryteacher(stuNum)
        else:
            stuNum = input("请输入学号查询是否退学")
            QueryExpulsion(stuNum)

# if __name__ == '__main__':
#     test()
