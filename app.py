from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request
from datetime import datetime, timezone
import psycopg2
from psycopg2 import sql
import os
from sqlcommands import *
import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    ascii_chars = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(ascii_chars) for i in range(length))
    return result_str

url = os.environ.get("DATABASE_URL")
connection = psycopg2.connect(url)
app = Flask(__name__)

# Test
@app.get("/hello")
def home():
    return "Hello, world"

# Drop tables
@app.post("/api/drop_table")
def drop_table():
    data = request.get_json()
    table_name = data["table"] 
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(DROP_TABLE)
            query = query.format(table=sql.Identifier(table_name))
            cursor.execute(query)
    return {"status": 'OK'}, 201

# Create empty tables in DB
@app.post("/api/create_db_tables")
def add_tables():
    data = request.get_json()
    user_table = data["user_table"]
    todo_table = data["todo_table"] 
    study_table = data["study_table"]  
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(CREATE_USER_TABLE)
            query = query.format(table=sql.Identifier(user_table))
            cursor.execute(query)
            query = sql.SQL(CREATE_TODO_TABLE)
            query = query.format(table=sql.Identifier(todo_table))
            cursor.execute(query)
            query = sql.SQL(CREATE_STUDY_TABLE)
            query = query.format(table=sql.Identifier(study_table))
            cursor.execute(query)
    return {"status": "OK"}, 201

# Create new user
@app.post("/api/create_user")
def add_user():
    data = request.get_json()
    user_name = data["user_name"]
    password = data["password"]
    active_pw = ""
    alias = data["alias"]
    school = data["school"]
    program = data["program"]
    birth = datetime.strptime(data["birth"], "%m-%d-%Y")
    points = data["points"]
    achievments = []  
    created = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (user_name, password, active_pw, alias, school, program, birth, points, achievments, created))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "message": f"User {user_name} with id {user_id} was created."}, 201

# Login to get active_pw
@app.post("/api/login")
def login():
    data = request.get_json()
    user_name = data["user_name"]
    password = data["password"]
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("password"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == password:
                active_pw = get_random_string(10)
                query = sql.SQL(UPDATE_VALUE)
                query = query.format(table=sql.Identifier("user_table"), variable=sql.Identifier("active_pw"))
                cursor.execute(query, (active_pw, user_name))
                data = cursor.fetchone()
                id = data[0]
                active_pw = data[3]
                return {"message": f"User {user_name} is logged in", "user_name": user_name, "id": id, "active_pw": active_pw}, 201
            else: 
                return {"message": f"User {user_name} gave wrong password"}, 400
                        
# Create todo task
@app.post("/api/create_todo")
def add_todo():
    data = request.get_json()
    user_name = data["user_name"]
    active_pw = data["active_pw"]
    todo = data["todo"]
    type_of_excersice = data["type_of_excersice"]
    priority = data["priority"]
    deadline = datetime.strptime(data["deadline"], "%m-%d-%Y")
    est_time = data["est_time"]
    calender = data["calender"]
    created = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                cursor.execute(INSERT_TODO, (user_name, todo, type_of_excersice, priority, deadline, est_time, calender, created))
                return {"message": f"User {user_name} added TODO {todo}."}, 201
            else:
                return {"message": f"User {user_name} gave wrong active password."}, 400

# Create study task
@app.post("/api/create_study")
def add_study():
    data = request.get_json()
    user_name = data["user_name"]
    active_pw = data["active_pw"]
    subject = data["subject"]
    study_time = data["study_time"]
    memo_text = data["memo_text"]
    effectivity = data["effectivity"]
    created = datetime.now(timezone.utc)
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                cursor.execute(INSERT_STUDY, (user_name, subject, study_time, memo_text, effectivity, created))
                return {"message": f"User {user_name} added {study_time} min of {subject}."}, 201
            else:
                return {"message": f"User {user_name} gave wrong active password."}, 400

# Get username data 
@app.get("/api/user/<string:user_name>")
def get_user(user_name):
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_ALL)
            query = query.format(table=sql.Identifier("user_table"), variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            data = cursor.fetchone()
            return {"id": data[0], 
                    "user_name": data[1], 
                    "alias": data[4], 
                    "school": data[5], 
                    "program": data[6] , 
                    "points": data[8],
                    "achievments": data[9]}, 200

# Get todo-list from user
@app.get("/api/user/todos/<string:user_name>/<string:active_pw>")
def get_todo(user_name, active_pw):
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                query = sql.SQL(GET_ALL)
                query = query.format(table=sql.Identifier("todo_table"), variable=sql.Identifier("user_name"))
                cursor.execute(query, (user_name,))
                data = cursor.fetchall()
                return {"message": f'Todo-list delieved',
                        "todos": data}, 200
            else:
                return {"message": f'wrong active password',
                        "user_name": user_name,
                        "active_pw": active_pw}, 200

# Get study-list from user
@app.get("/api/user/studies/<string:user_name>/<string:active_pw>")
def get_study(user_name, active_pw):
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                query = sql.SQL(GET_ALL)
                query = query.format(table=sql.Identifier("study_table"), variable=sql.Identifier("user_name"))
                cursor.execute(query, (user_name,))
                data = cursor.fetchall()
                return {"message": f'Study-list delieved',
                        "todos": data}, 200
            else:
                return {"message": f'wrong active password',
                        "user_name": user_name,
                        "active_pw": active_pw}, 200

# Add points to user
@app.post("/api/add_points")
def add_points():
    data = request.get_json()
    user_name = data["user_name"]
    active_pw = data["active_pw"]
    points = data["points"]
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                query = sql.SQL(GET_ALL)
                query = query.format(table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
                cursor.execute(query, (user_name,))
                data = cursor.fetchone()
                old_points = data[8]
                points += old_points 
                query = sql.SQL(UPDATE_VALUE)
                query = query.format(table=sql.Identifier("user_table"), variable=sql.Identifier("points"))
                cursor.execute(query, (points, user_name))
                data = cursor.fetchone()
                points = data[8]
                return {"message": f"User {user_name} updated points to {points}"}, 201
            else: 
                return {"message": f"User {user_name} gave wrong active password"}, 400

# Add achievments to user
@app.post("/api/add_achievments")
def add_achievmentss():
    data = request.get_json()
    user_name = data["user_name"]
    active_pw = data["active_pw"]
    achievment = data["achievment"]
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                query = sql.SQL(GET_ALL)
                query = query.format(table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
                cursor.execute(query, (user_name,))
                data = cursor.fetchone()
                achievments = data[9]
                achievments.append(achievment) 
                query = sql.SQL(UPDATE_VALUE)
                query = query.format(table=sql.Identifier("user_table"), variable=sql.Identifier("achievments"))
                cursor.execute(query, (achievments, user_name))
                data = cursor.fetchone()
                achievments = data[9]
                return {"message": f"User {user_name} updated achievment to {achievment}"}, 201
            else: 
                return {"message": f"User {user_name} gave wrong active password"}, 400
                        
# Delete todo from list
@app.post("/api/delete_todo")
def delete_todo():
    data = request.get_json()
    todo_id = data["todo_id"]
    user_name = data["user_name"]
    active_pw = data["active_pw"]
    with connection:
        with connection.cursor() as cursor:
            query = sql.SQL(GET_VALUE)
            query = query.format(data=sql.Identifier("active_pw"), table=sql.Identifier("user_table"),variable=sql.Identifier("user_name"))
            cursor.execute(query, (user_name,))
            pw = cursor.fetchone()[0]
            if pw == active_pw:
                query = sql.SQL(GET_ALL)
                query = query.format(table=sql.Identifier("todo_table"),variable=sql.Identifier("id"))
                cursor.execute(query, (todo_id,))
                user = cursor.fetchone()[1]
                if user == user_name:
                    query = sql.SQL(DELETE_VALUE)
                    query = query.format(table=sql.Identifier("todo_table"),variable=sql.Identifier("id"))
                    cursor.execute(query, (todo_id,))
                    return {"message": f"User deleted id {todo_id} from todolist."}, 201
                else:
                    return {"message": f"Provided id don not belong to {user_name}"}, 400
            else:
                return {"message": f"User {user_name} gave wrong active password."}, 400