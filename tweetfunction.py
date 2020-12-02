import mariadb
import dbcreds
from datetime import datetime


def getTweet(user_id, index, checkuser_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        if user_id == None:
            if index == None:
                cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM tweets t INNER JOIN users u ON t.user_id = u.id ORDER BY id DESC LIMIT 5")
            else:
                print(index)
                cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.id<? ORDER BY id DESC LIMIT 5", [index])
            rows = cursor.fetchall()
        else:
            cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id=? ORDER BY t.created_at DESC LIMIT ?,5", [user_id,index])
            rows = cursor.fetchall()
        tweets = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ?", [row[0],])
            com_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ? AND notice = 1", [row[0],])
            newcom_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ?", [row[0],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND user_id = ?", [row[0], checkuser_id])
            iflike = cursor.fetchone()[0]
            tweet = dict(zip(headers,row))
            tweet['com_amount'] = com_amount   
            tweet['newcom_amount'] = newcom_amount   
            tweet['like_amount'] = like_amount   
            # tweet['newlike_amount'] = newlike_amount   
            tweet['iflike'] = iflike
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
    
def followTweets(user_id, checkuser_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print(user_id)    
        cursor.execute("SELECT  t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM user_follows uf INNER JOIN tweets t ON uf.following_id = t.user_id INNER JOIN users u ON t.user_id = u.id WHERE uf.user_id=? ORDER BY t.id DESC", [user_id])
        rows = cursor.fetchall()
        print(rows)
        tweets = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ?", [row[0],])
            com_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ? AND notice = 1", [row[0],])
            newcom_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ?", [row[0],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND user_id = ?", [row[0], checkuser_id])
            iflike = cursor.fetchone()[0]
            tweet = dict(zip(headers,row))
            tweet['com_amount'] = com_amount   
            tweet['newcom_amount'] = newcom_amount   
            tweet['like_amount'] = like_amount   
            # tweet['newlike_amount'] = newlike_amount   
            tweet['iflike'] = iflike
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
    
def getOneTweet(tweet_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.id=?", [tweet_id])
        rows = cursor.fetchall()
        tweets = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            # print(row)
            # cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ?", [row[0],])
            # com_amount = cursor.fetchone()[0]
            # cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ? AND notice = 1", [row[0],])
            # newcom_amount = cursor.fetchone()[0]
            # cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ?", [row[0],])
            # like_amount = cursor.fetchone()[0]
            # cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND notice = 1", [row[0],])
            # newlike_amount = cursor.fetchone()[0]
            # print(com_amount)
            # cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND user_id = ?", [row[0], checkuser_id])
            # iflike = cursor.fetchone()[0]
            # print(iflike)
            tweet = dict(zip(headers,row))
            # print(tweet)
            # tweet['com_amount'] = com_amount   
            # tweet['newcom_amount'] = newcom_amount   
            # tweet['like_amount'] = like_amount   
            # tweet['newlike_amount'] = newlike_amount   
            # tweet['iflike'] = iflike
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
    
def postTweet(token, content, image, retweet_id):
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
            date = str(datetime.now())[0:18]
            cursor.execute("INSERT INTO tweets(user_id, content, created_at, image, retweet) VALUES (?,?,?,?,?)", [user_id, content, date, image, retweet_id])
            conn.commit()
            row = cursor.rowcount
            if row == 1:
                cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id=? and t.content=?", [user_id, content])
                rows = cursor.fetchone()
                headers = [ i[0] for i in cursor.description]
                tweet = dict(zip(headers,rows)) 
                tweet['com-amount'] = 0
                tweet['like-amount'] = 0                       
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
            cursor.execute("SELECT t.content , t.image  FROM tweets t WHERE t.id = ?", [tweet_id,] )
            rows = cursor.fetchone()
            print(rows)
            if content != None and content != "" and content != rows[0]:
                cursor.execute("UPDATE tweets SET content=? WHERE user_id=? AND id=?", [content, user_id, tweet_id])
            if image != None and image != "" and image != rows[1]:
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
        
def search(searchContent, checkuser_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print(searchContent)  
        word = "%" + searchContent + "%"
        print(checkuser_id)  
        cursor.execute("SELECT t.id ,t.user_id ,u.username ,u.url ,t.content ,t.created_at ,t.image, t.retweet FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE u.username LIKE ? OR u.email LIKE ? OR t.content LIKE ?", [word, word, word])
        rows = cursor.fetchall()
        print(rows)
        tweets = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ?", [row[0],])
            com_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ? AND notice = 1", [row[0],])
            newcom_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ?", [row[0],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND user_id = ?", [row[0], checkuser_id])
            iflike = cursor.fetchone()[0]
            tweet = dict(zip(headers,row))
            tweet['com_amount'] = com_amount   
            tweet['newcom_amount'] = newcom_amount   
            tweet['like_amount'] = like_amount   
            # tweet['newlike_amount'] = newlike_amount   
            tweet['iflike'] = iflike
            tweets.append(tweet)   
    except mariadb.ProgrammingError:
        print("program error...")
    except mariadb.DataError as error:
        print("Data error...")
        print(error)
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
        