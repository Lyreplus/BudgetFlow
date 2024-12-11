import psycopg2

def find_progetto_by_id(progetto_id):
    query = "SELECT * FROM Progetto WHERE progetto_id = %s"
    return execute_query(query, (progetto_id,))


def is_user_in_project(user_id, progetto_id):
    query = "SELECT * FROM Progetto_Utenti WHERE progetto_id = %s AND user_id = %s"
    result = execute_query(query, (progetto_id, user_id))
    if len(result) == 0:
        return False
    return True

def execute_query(query, params):
    conn = psycopg2.connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()
    cursor.close()
    return records
