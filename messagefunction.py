import mariadb
import dbcreds
from datetime import datetime

def getmessages(user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT m.id ,m.content ,m.sender_id ,u.username ,m.receiver_id ,m.sent_time FROM message m INNER JOIN users u ON m.sender_id = u.id WHERE m.receiver_id=?", [user_id])
        rows = cursor.fetchall()
        messages = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            messages.append(dict(zip(headers,row)))
        print(messages)
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError:
        print("Data error...")
    except mariadb.DatabaseError:
        print("Database error...")
    except mariadb.OperationalError:
        print("connect error...")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        return messages

def postMessage(token, receiver_id, content):   
    conn = None
    cursor = None
    row = None
    user_id = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        print(receiver_id)
        print(content)
        if user_id != None:
            print(user_id)
            date = str(datetime.now())[0:18]
            cursor.execute("INSERT INTO message(content, sender_id, receiver_id, sent_time) VALUES (?,?,?,?)", [content, user_id, receiver_id, date])
            conn.commit()
            row = cursor.rowcount           
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError:
        print("Data error...")
    except mariadb.DatabaseError:
        print("Database error...")
    except mariadb.OperationalError:
        print("connect error...")
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.rollback()
            conn.close()
        if row == 1:
            return True
        else:
            return False
        
