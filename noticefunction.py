import mariadb
import dbcreds

def noticeTweetLike(user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print(user_id)
        cursor.execute("SELECT id FROM tweets WHERE user_id=?", [user_id])
        rows = cursor.fetchall()
        tweets=[]
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id=? AND notice=1", [row[0]])
            count = cursor.fetchall()
            tweet={
                "tweet_id": row[0],
                "newLike": count[0][0]
            }
            tweets.append(tweet)      
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
    
def editTweetLike(tweet_id, likeUser_id):
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
            cursor.execute("UPDATE tweet_like SET notice = 0 WHERE tweet_id=? AND user_id=?", [tweet_id, likeUser_id]) 
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