import mariadb
import dbcreds
from datetime import datetime

def getComment(tweet_id, user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT c.id ,c.tweet_id ,c.user_id ,u.username ,u.url ,c.content ,c.image ,c.created_at, c.notice FROM users u INNER JOIN comments c ON u.id = c.user_id WHERE c.tweet_id=? ORDER BY c.created_at DESC", [tweet_id])
        rows = cursor.fetchall()
        comments = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM com_comment WHERE comment_id = ?", [row[0],])
            com_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM com_comment WHERE comment_id = ? AND notice = 1", [row[0],])
            newcom_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM comment_like WHERE comment_id = ?", [row[0],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM comment_like WHERE comment_id = ? AND user_id = ?", [row[0], user_id])
            iflike = cursor.fetchone()[0]
            comment = dict(zip(headers,row))
            comment['com_amount'] = com_amount   
            comment['newcom_amount'] = newcom_amount   
            comment['like_amount'] = like_amount   
            comment['iflike'] = iflike
            comments.append(comment)   
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
            cursor.execute("SELECT c.id ,c.tweet_id ,c.user_id ,u.username ,u.url ,c.content ,c.image ,c.created_at  FROM users u INNER JOIN comments c ON u.id = c.user_id WHERE c.tweet_id=? AND c.created_at=?", [tweet_id, date])
            rows = cursor.fetchone()
            headers = [ i[0] for i in cursor.description]
            comment = dict(zip(headers,rows))
            comment['com-amount'] = 0              
            comment['like-amount'] = 0              
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
            cursor.execute("SELECT content , image  FROM comments WHERE id = ?", [comment_id,] )
            rows = cursor.fetchone()
            print(rows)
            if content != None and content != "" and content != rows[0]:
                cursor.execute("UPDATE comments SET content=? WHERE user_id=? AND id=?", [content, user_id, comment_id])
            if image != None and image != "" and image != rows[1]:
                cursor.execute("UPDATE comments SET image=? WHERE user_id=? AND id=?", [image, user_id, comment_id])
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
            comment = {
                "comment_id" : comment_id,
                "content" : content,
                "image" : image
            }
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
        
def getCom_comment(comment_id, user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT cc.id ,cc.comment_id ,cc.content ,cc.created_at , cc.user_id ,u.username,u.url, cc.notice FROM com_comment cc INNER JOIN users u ON cc.user_id =u.id WHERE cc.comment_id=? ORDER BY cc.created_at DESC" , [comment_id])
        rows = cursor.fetchall()
        comments = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            print(row[0])
            print(user_id)
            cursor.execute("SELECT COUNT(*) FROM com_comment_like WHERE com_comment_id = ?", [row[0],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM com_comment_like WHERE com_comment_id = ? AND user_id = ?", [row[0], user_id])
            iflike = cursor.fetchone()[0]
            comment = dict(zip(headers,row))
            comment['like_amount'] = like_amount   
            comment['iflike'] = iflike
            comments.append(comment)   
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
    
def postCom_comment(token, comment_id, content):
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
            cursor.execute("INSERT INTO com_comment(user_id, content, created_at, comment_id) VALUES (?,?,?,?)", [user_id, content, date, comment_id])
            conn.commit()
            cursor.execute("SELECT cc.id ,cc.comment_id ,cc.content ,cc.created_at ,cc.like_amount ,cc.user_id ,u.username,u.url FROM com_comment cc INNER JOIN users u ON cc.user_id =u.id WHERE cc.comment_id=? AND cc.created_at=?", [comment_id, date])
            rows = cursor.fetchone()
            headers = [ i[0] for i in cursor.description]
            comment = dict(zip(headers,rows))
            comment['like-amount'] = 0              
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

def editCom_comment(token, com_comment_id, content):
    conn = None
    cursor = None
    row = None
    user_id = None
    comment = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("SELECT content FROM com_comment WHERE id = ?", [com_comment_id,] )
            rows = cursor.fetchone()
            if content != None and content != "" and content != rows[0]:
                cursor.execute("UPDATE com_comment SET content=? WHERE user_id=? AND id=?", [content, user_id, com_comment_id])
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
            comment = {
                "com_comment_id" : com_comment_id,
                "content" : content,
            }
            return comment

def deleteCom_comment(token, com_comment_id):
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
            print(com_comment_id)
            cursor.execute("DELETE FROM com_comment WHERE user_id=? AND id=?", [user_id, com_comment_id])
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
