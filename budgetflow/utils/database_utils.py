import psycopg2
from typing import List, Tuple

def find_progetto_by_id(progetto_id: str) -> List[Tuple]:
    query = "SELECT * FROM Progetto WHERE progetto_id = %s"
    return execute_query(query, (progetto_id,))


def is_user_in_project(user_id, progetto_id):
    query = "SELECT * FROM Progetto_Utenti WHERE progetto_id = %s AND user_id = %s"
    result: List[Tuple] = execute_query(query, (progetto_id, user_id))
    if len(result) == 0:
        return False
    return True

def execute_query(query : str, *args) -> List[Tuple]:
    conn = psycopg2.connect()
    cursor = conn.cursor()
    cursor.execute(query, args)
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return records
