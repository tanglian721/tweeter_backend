import mariadb
import dbcreds
import random
import string
from datetime import datetime

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str



def getUsers(user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if user_id == None or user_id == "": 
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            users = []
            headers = [ i[0] for i in cursor.description]
            for row in rows:
                users.append(dict(zip(headers,row)))
        else:
            cursor.execute("SELECT * FROM users WHERE id=?", [user_id])
            rows = cursor.fetchone()
            users = {}
            headers = [ i[0] for i in cursor.description]
            users = dict(zip(headers,rows))    
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
        return users
    
def signUp(email, username, password, birthdate, bio, date, url):
    conn = None
    cursor = None
    row = None
    user = {}
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print("1")
        print(date)
        cursor.execute("INSERT INTO users(username, email, birthdate, bio, password, join_date, url) VALUES (?, ?, ?, ?, ?, ?, ?)", [username, email, birthdate, bio, password, date, url])
        print("b")
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
        
def modifyAccount(email, username, password, birthdate, bio, url, user_id):
    conn = None
    cursor = None
    row = None
    print(username)
    print(email)
    print(password)
    print(birthdate)
    print(bio)
    print(url)
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print("1")
        if email != "" and email != None:           
            cursor.execute("UPDATE users SET email=? WHERE id=?", [email, user_id])
        if username != "" and username != None:           
            cursor.execute("UPDATE users SET username=? WHERE id=?", [username, user_id])
        if password != "" and password != None:           
            cursor.execute("UPDATE users SET password=? WHERE id=?", [password, user_id])
        if birthdate != "" and birthdate != None:           
            cursor.execute("UPDATE users SET birthdate=? WHERE id=?", [birthdate, user_id])
        if bio != "" and bio != None:           
            cursor.execute("UPDATE users SET bio=? WHERE id=?", [bio, user_id])
            print('2')
        if url != "" and url != None:           
            cursor.execute("UPDATE users SET url=? WHERE id=?", [url, user_id])
        print("b")
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
          
def deleteAccount(user_id):
    conn = None
    cursor = None
    row = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", [user_id,])
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
        
def login(username, password):
    conn = None
    cursor = None
    row = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print("a")       
        cursor.execute("SELECT * FROM users WHERE username=? and password=?", [username, password])
        user = cursor.fetchone()
        users = {}
        headers = [ i[0] for i in cursor.description]
        users = dict(zip(headers,user))    
        print(users)
        if users != {}:
            token = get_random_alphanumeric_string(20)
            date = str(datetime.now())[0:10]
            cursor.execute("INSERT INTO token(token, user_id, date) VALUES (?, ?, ?)", [token, users.get("id"), date])
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
            users["loginToken"] = token
            return users    

def logout(token):
    conn = None
    cursor = None
    row = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM token WHERE token=?", [token,])
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

