import mysql.connector
from mysql.connector import Error

myconn = mysql.connector.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8',
                                 use_unicode=True)
cur = myconn.cursor()
cur.execute("SET NAMES utf8;")


def startDB():
    create()
    # getStudents()


def create():
    try:
        create_db_query = "CREATE DATABASE IF NOT EXISTS test;"
        cur.execute(create_db_query)

        create_files = ('CREATE TABLE `files` ('
                        '`id_file` int(11) NOT NULL,'
                        '`id_my` int(11) NOT NULL,'
                        '`description` text NOT NULL,'
                        '`name_origin` text NOT NULL,'
                        '`path` text NOT NULL,'
                        '`date_upload` text NOT NULL) ENGINE=InnoDB '
                        'DEFAULT CHARSET=cp1251;')
        cur.execute(create_files)

        insert_val = (
            "INSERT INTO `files` (`id_file`, `id_my`, `description`, `name_origin`, `path`, `date_upload`) VALUES "
            "(16, 17, 'Закачка из менеджера', 'Стратегии в виртуальном футболе.pdf', "
            "'files/Стратегии в виртуальном футболе.pdf', '16-03-2022  08:41:22');")

        cur.execute(insert_val)

        create_myarttable = ("CREATE TABLE `myarttable` ("
                             "`id` int(11) NOT NULL,"
                             "`text` text NOT NULL,"
                             "`description` text NOT NULL,"
                             "`keywords` text NOT NULL)"
                             " ENGINE=InnoDB DEFAULT CHARSET=cp1251;")

        cur.execute(create_myarttable)

        insert_val = ("INSERT INTO `myarttable` (`id`, `text`, `description`, `keywords`) VALUES "
                      "(17, 'Baranov', 'Engeneer', 'Ivanov'), "
                      "(20, 'Fedorov', 'Cpp, Delphi, PHP, JS', '3t'), "
                      "(92, 'Daniel', 'Artist', 'Theater Saturday'), "
                      "(93, 'Andrew', 'Poet', 'First Electrotechnical University'), "
                      "(94, 'Nikita', 'Student', 'Technological Institute'), "
                      "(95, 'Ilya', 'Salesman', 'Hypermarket'), "
                      "(96, 'Matvey', 'Programmer', 'Metropolitan College'), "
                      "(97, 'Fedor', 'Loader', 'St. Petersburg State University'), "
                      "(98, 'Ivan', 'Student', 'LETI'), (99, 'Alexey', 'Engineer', 'ITMO');")

        cur.execute(insert_val)

        alter_table = "ALTER TABLE `files` ADD PRIMARY KEY (`id_file`), ADD KEY `id_my` (`id_my`);"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `myarttable` ADD PRIMARY KEY (`id`);"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `files` MODIFY `id_file` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `myarttable` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `files`ADD CONSTRAINT `files_ibfk_1` FOREIGN KEY (`id_my`) REFERENCES `myarttable` (`id`);"
        cur.execute(alter_table)
        myconn.commit()

    except Error as e:
        print(e)


class Student:

    def __init__(self, id, text, description, keywords):
        self.id = id
        self.text = text
        self.description = description
        self.keywords = keywords


def getStudents():
    cur.execute("USE test;")
    cur.execute("SELECT * FROM myarttable")
    result = cur.fetchall()
    students = []
    for student in result:
        students.append(Student(student[0], student[1], student[2], student[3]))

    return students


def deleteStudent(id):
    idx = None
    for i, student in enumerate(students):
        if id == student.id:
            idx = i
            break

    if idx is None:
        return

    cur.execute("DELETE FROM files WHERE id_my = " + str(idx))
    cur.execute("DELETE FROM myarttable WHERE id = " + str(idx))
    myconn.commit()
    del students[idx]
    for var in students:
        print(var.id)


def updateStudent(id, text, description, keywords):
    idx = None
    for i, student in enumerate(students):
        if id == student.id:
            idx = i
            break

    if idx is None:
        return

    cur.execute(
        "UPDATE myarttable SET text='" + text + "', description='" + description + "', keywords='" + keywords + "' WHERE id = " + str(idx))
    myconn.commit()
    students[idx] = Student(id, text, description, keywords)


# Генерит запрос на удаление
def get_sql_delete(id):
    return f'DELETE FROM myarttable WHERE id = {id};'


# Генерит запрос на обновление
def get_sql_update(id, text, description, keywords):
    return f'''UPDATE myarttable 
               SET text = {text}, description = {description}, keywords = {keywords}
               WHERE id = {id}'''


students = getStudents()
