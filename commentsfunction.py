import mariadb
import dbcreds
from datetime import datetime

def getComment(tweet_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT c.id ,c.tweet_id ,c.user_id ,u.username ,c.content ,c.image ,c.created_at,c.com_amount ,c.like_amount  FROM users u INNER JOIN comments c ON u.id = c.user_id WHERE c.tweet_id=? ORDER BY c.created_at DESC", [tweet_id])
        rows = cursor.fetchall()
        comments = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            comments.append(dict(zip(headers,row)))   
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
        return comments
    
def postComment(token, tweet_id, content, image):
    conn = None
    cursor = None
    row = None
    user_id = None
    comment = {}
    amount = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            print(user_id)
            date = str(datetime.now())[0:18]
            cursor.execute("INSERT INTO comments(user_id, content, created_at, image, tweet_id) VALUES (?,?,?,?,?)", [user_id, content, date, image,tweet_id])
            conn.commit()
            print('a')
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE c.tweet_id=?", [tweet_id,])
            amount = cursor.fetchone()[0]
            print(amount)
            if amount != None:
                cursor.execute("UPDATE tweets SET com_amount=? WHERE id=?", [amount,tweet_id])
                conn.commit()            
                row = cursor.rowcount
                if row == 1: 
                    cursor.execute("SELECT c.id ,c.tweet_id ,c.user_id ,u.username ,c.content ,c.image ,c.created_at,c.com_amount ,c.like_amount  FROM users u INNER JOIN comments c ON u.id = c.user_id WHERE c.tweet_id=? AND c.created_at=?", [tweet_id, date])
                    rows = cursor.fetchone()
                    headers = [ i[0] for i in cursor.description]
                    comment = dict(zip(headers,rows))              
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
        return comment

def editComment(token, comment_id, content, image):
    conn = None
    cursor = None
    row = None
    user_id = None
    tweet = {}
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            if content != None and content != "":
                cursor.execute("UPDATE comments SET content=? WHERE user_id=? AND id=?", [content, user_id, comment_id])
            if image != None and image != "":
                cursor.execute("UPDATE comments SET image=? WHERE user_id=? AND id=?", [image, user_id, comment_id])
            conn.commit()
            cursor.execute("SELECT c.id ,c.tweet_id ,c.user_id ,u.username ,c.content ,c.image ,c.created_at,c.com_amount ,c.like_amount  FROM users u INNER JOIN comments c ON u.id = c.user_id WHERE c.id=?", [comment_id])
            rows = cursor.fetchone()
            headers = [ i[0] for i in cursor.description]
            comment = dict(zip(headers,rows))           
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
        return comment

def deleteComment(token, comment_id):
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
            cursor.execute("DELETE FROM comments WHERE user_id=? AND id=?", [user_id, comment_id])
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
