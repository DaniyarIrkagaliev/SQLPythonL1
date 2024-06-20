import os

import mysql.connector
from mysql.connector import Error

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
script_dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(script_dir, "static/")), name="static")

myconn = mysql.connector.connect(host='localhost', user='root', passwd='root', db='test', charset='utf8',
                                 use_unicode=True)
cur = myconn.cursor()
cur.execute("SET NAMES utf8;")

templates = Jinja2Templates(directory=os.path.join(script_dir, "templates/"))


# cur.execute("select * FROM students")
# print(cur.fetchall())

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"students": getStudents()}
    )


@app.get("/delete", response_class=HTMLResponse)
async def delete_student(request: Request, student_id: int):
    deleteStudent(student_id)
    return await index(request)


@app.get("/update", response_class=HTMLResponse)
async def update_student(request: Request, textId: int, textEd1: str, textEd2: str, textEd3: str):
    updateStudent(
        id=textId,
        text=textEd1,
        description=textEd2,
        keywords=textEd3
    )
    return await index(request)


# скрипт создания и заполнения бд в виде питоновского метода
def create():
    try:
        create_db_query = "CREATE DATABASE IF NOT EXISTS test;"
        cur.execute(create_db_query)

        create_files = ('CREATE IF NOT EXISTS TABLE `files` ('
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
            "(16, 131, 'исследовательский проект', 'БПЛА в Сельском хозяйстве. Проблемы внедрения в АПК РФ.pdf', "
            "'files/БПЛА в Сельском хозяйстве. Проблемы внедрения в АПК РФ.pdf', '16-03-2024  18:42:12');")

        cur.execute(insert_val)

        create_students = ("CREATE TABLE `students` ("
                           "`id` int(11) NOT NULL,"
                           "`text` text NOT NULL,"
                           "`description` text NOT NULL,"
                           "`keywords` text NOT NULL)"
                           " ENGINE=InnoDB DEFAULT CHARSET=cp1251;")

        cur.execute(create_students)

        insert_val = ("INSERT INTO students (id, text, description, keywords) VALUES "
                      "(131, 'Boldyrev', 'Engeneer', 'Java'),"
                      "(132, 'Smirnikh', 'Student', 'Voronezh State University'),"
                      " (133, 'Krikunov', 'full-stack developer', 'python'),"
                      " (134, 'Malishev', 'Poet', 'Filmmaker'), (136, 'Medvedev',"
                      " 'Student', 'Volgograd State University'), (137, 'Artemiev',"
                      " 'Musician', 'Last Summer Day indie-rock band')"
                      ";")

        cur.execute(insert_val)

        alter_table = "ALTER TABLE `files` ADD PRIMARY KEY (`id_file`), ADD KEY `id_my` (`id_my`);"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `students` ADD PRIMARY KEY (`id`);"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `files` MODIFY `id_file` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `students` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;"
        cur.execute(alter_table)

        alter_table = "ALTER TABLE `files`ADD CONSTRAINT `files_ibfk_1` FOREIGN KEY (`id_my`) REFERENCES `students` (`id`);"
        cur.execute(alter_table)
        myconn.commit()

    except Error as e:
        print(e)


create()


# получение студентов
def getStudents():
    cur.execute("USE test;")
    cur.execute("SELECT * FROM students")
    result = cur.fetchall()
    students = []
    for student in result:
        students.append(Student(student[0], student[1], student[2], student[3]))

    return students


class Student:

    def __init__(self, id, text, description, keywords):
        self.id = id
        self.text = text
        self.description = description
        self.keywords = keywords


# создание списка студентов через экземпляр класса для работы с ними на фронте
students = getStudents()


# удаление
def deleteStudent(id):
    cur.execute("DELETE FROM files WHERE id_my = " + str(id))
    cur.execute("DELETE FROM students WHERE id = " + str(id))
    myconn.commit()


# обновление
def updateStudent(id, text, description, keywords):
    cur.execute(
        "UPDATE students SET text='" + text + "', description='" + description + "', keywords='" + keywords + "' WHERE id = " + str(
            id))
    myconn.commit()


# Генерит запрос на удаление
def get_sql_delete(id):
    return f'DELETE FROM students WHERE id = {id};'


# Генерит запрос на обновление
def get_sql_update(id, text, description, keywords):
    return f'''UPDATE students 
               SET text = {text}, description = {description}, keywords = {keywords}
               WHERE id = {id}'''
