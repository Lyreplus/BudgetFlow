from utils.database_utils import execute_query

def add_user_role(user_id, role_id):
    query = "INSERT INTO Utenti_Ruoli (utente_id, ruolo_id) VALUES (%s, %s)"
    execute_query(query, (user_id, role_id))

def add_role(name):
    query = "INSERT INTO Ruolo (nome) VALUES (%s) RETURNING id_ruolo"
    return execute_query(query, (name,))[0][0]
