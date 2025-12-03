import mysql.connector

def get_connection():
    """
    Returns a connection to the SFILS MySQL database.
    """
    return mysql.connector.connect(
        host="127.0.0.1",
        user="sfils_user",     # <-- change if needed
        password="sfils_pw",   # <-- change if needed
        database="sfils"
    )
  
