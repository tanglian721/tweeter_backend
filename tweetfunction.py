import mariadb
import dbcreds
from datetime import datetime


def getTweet(user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.com_amount ,t.like_amount FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id=? ORDER BY t.created_at DESC", [user_id])
        rows = cursor.fetchall()
        tweets = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            tweets.append(dict(zip(headers,row)))   
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
        return tweets
    
def postTweet(token, content, image):
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
            date = str(datetime.now())[0:10]
            cursor.execute("INSERT INTO tweets(user_id, content, created_at, image) VALUES (?,?,?,?)", [user_id, content, date, image])
            conn.commit()
            row = cursor.rowcount
            if row == 1:
                cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.com_amount ,t.like_amount FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id=? and t.content=?", [user_id, content])
                rows = cursor.fetchone()
                headers = [ i[0] for i in cursor.description]
                tweet = dict(zip(headers,rows))              
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
        return tweet
    
def editTweet(token, content, image, tweet_id):
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
                cursor.execute("UPDATE tweets SET content=? WHERE user_id=? AND id=?", [content, user_id, tweet_id])
            if image != None and image != "":
                cursor.execute("UPDATE tweets SET image=? WHERE user_id=? AND id=?", [image, user_id, tweet_id])
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
            tweet = {
                "tweet_id" : tweet_id,
                "content" : content,
                "image" : image
            }
            return tweet

def deleteTweet(token, tweet_id):
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
            cursor.execute("DELETE FROM tweets WHERE user_id=? AND id=?", [user_id, tweet_id])
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
        