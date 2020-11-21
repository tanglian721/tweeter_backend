import mariadb
import dbcreds

def getFollows(user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT uf.following_id , u.email ,u.username , u.bio ,u.birthdate ,u.url FROM users u INNER JOIN user_follows uf ON u.id = uf.following_id WHERE uf.user_id=?", [user_id])
        rows = cursor.fetchall()
        users = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            users.append(dict(zip(headers,row)))   
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
def getFollowers(user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT uf.user_id , u.email ,u.username , u.bio ,u.birthdate ,u.url FROM users u INNER JOIN user_follows uf ON u.id = uf.user_id WHERE uf.following_id=?", [user_id])
        rows = cursor.fetchall()
        users = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            users.append(dict(zip(headers,row)))   
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
def follows(token, follow_id):
    conn = None
    cursor = None
    row = None
    user_id = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("INSERT INTO user_follows(user_id, following_id) VALUES (?,?)", [user_id, follow_id])
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
def unFollows(token, follow_id):
    conn = None
    cursor = None
    row = None
    user_id = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        print(user_id)
        if user_id != None:
            cursor.execute("DELETE FROM user_follows WHERE user_id=? AND following_id=?", [user_id, follow_id])
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
            