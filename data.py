import datetime
import sqlite3
from typing import List


c = sqlite3.connect("kanban.db")
database = c.cursor()


def create_board():
    """
    Create 3 tables (do, doing, done) in database file
    """
    database.execute("""CREATE TABLE IF NOT EXISTS do (
        ID INTEGER PRIMARY KEY,
        Do TEXT
        )""")
    database.execute("""CREATE TABLE IF NOT EXISTS doing (
        ID INTEGER PRIMARY KEY,
        Doing TEXT
        )""")
    database.execute("""CREATE TABLE IF NOT EXISTS done (
        ID INTEGER PRIMARY KEY,
        Done TEXT
        )""")


create_board()


def get_do() -> List[str]:
    """
    Get the tasks from 'do' table
    """
    database.execute("SELECT * FROM do")
    return database.fetchall()


def get_doing() -> List[str]:
    """
    Get the tasks from 'doing' table
    """
    database.execute("SELECT * FROM doing")
    return database.fetchall()


def get_done() -> List[str]:
    """
    Get the tasks from 'done' table
    """
    database.execute("SELECT * FROM done")
    return database.fetchall()


def add_task(task: str):
    """
    Add a task into the 'do' table
    """
    with c:
        database.execute("INSERT INTO do (Do) VALUES (?)", (task,))


def delete_task(task: str, column: str):
    """
    Delete a task from the specify table (do, doing, done)
    """
    with c:
        database.execute("DELETE from {} WHERE {} = ?".format(column, column.title()), (task,))


def move_task(task: str, doing=False, done=False):
    """
    Move a task to the next table in database
    From 'do' -> 'doing' or 'doing' -> 'done'
    """
    if doing:
        with c:
            database.execute("INSERT INTO doing (Doing) VALUES (?)", (task,))
            database.execute("DELETE from do WHERE Do = (?)", (task,))

    if done:
        with c:
            database.execute("INSERT INTO done (Done) VALUES (?)", (task,))
            database.execute("DELETE from doing WHERE Doing = (?)", (task,))


def move_task_back(task: str, doing=False, done=False):
    """
    Move a task to the previous table in database
    From 'done' -> 'doing' or 'doing' -> 'do'
    """
    if done:
        with c:
            database.execute("INSERT INTO doing (Doing) VALUES (?)", (task,))
            database.execute("DELETE from done WHERE Done = (?)", (task,))

    if doing:
        with c:
            database.execute("INSERT INTO do (Do) VALUES (?)", (task,))
            database.execute("DELETE from doing WHERE Doing = (?)", (task,))


def clear_board():
    """
    Delete all tables and re-create the board
    """
    with c:
        database.execute("DROP TABLE IF EXISTS do")
        database.execute("DROP TABLE IF EXISTS doing")
        database.execute("DROP TABLE IF EXISTS done")

    create_board()

