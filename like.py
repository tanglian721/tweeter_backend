import mariadb
import dbcreds

def getTweetLikes(tweet_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT tl.tweet_id ,tl.user_id ,u.username FROM users u INNER JOIN tweet_like tl ON u.id = tl.user_id WHERE tl.tweet_id=?", [tweet_id])
        rows = cursor.fetchall()
        likes = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            likes.append(dict(zip(headers,row)))   
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
        return likes

def postTweetLike(token, tweet_id):
    conn = None
    cursor = None
    row = None
    user_id = None
    amount = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("INSERT INTO tweet_like(tweet_id, user_id) VALUES (?,?)", [tweet_id, user_id])
            conn.commit()
            print("1")            
            cursor.execute("SELECT COUNT(*) FROM tweet_like tl WHERE tl.tweet_id=?", [tweet_id,])
            amount = cursor.fetchone()[0]
            print(amount)
            if amount != None:
                cursor.execute("UPDATE tweets SET like_amount=? WHERE id=?", [amount,tweet_id])
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
        
def deleteTweetLike(token, tweet_id):
    conn = None
    cursor = None
    row = None
    user_id = None
    amount = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("DELETE FROM tweet_like WHERE tweet_id=? AND user_id=?", [tweet_id, user_id])
            conn.commit()
            print("1")            
            cursor.execute("SELECT COUNT(*) FROM tweet_like tl WHERE tl.tweet_id=?", [tweet_id,])
            amount = cursor.fetchone()[0]
            print(amount)
            if amount != None:
                cursor.execute("UPDATE tweets SET like_amount=? WHERE id=?", [amount,tweet_id])
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