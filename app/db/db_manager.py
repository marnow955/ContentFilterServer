import MySQLdb as mysql
from app.db.connection import *


def connect():
    conn = mysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB)
    conn.autocommit(False)
    return conn


def disconnect(conn):
    conn.close()


def get_post_by_id(id):
    query = "SELECT * FROM posts WHERE ID=" + str(id)
    result = execute_query(query)
    return result[0]


def update_post_flag(id, flag):
    query = "UPDATE posts SET flag=" + str(flag) + " WHERE ID=" + str(id)
    execute_query(query)


def execute_query(query):
    result = None
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(query)
        conn.commit()
        result = cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(e)
    disconnect(cur)
    disconnect(conn)
    return result
