import mariadb
import dbcreds

def getTweets(user_id, checkuser_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        print(user_id)
        cursor.execute("SELECT t.id ,t.user_id ,u2.username ,u2.url ,t.content ,t.image ,t.created_at, u.notice FROM tweets t INNER JOIN `@_users` u ON u.tweet_id = t.id INNER JOIN users u2 ON t.user_id = u2.id WHERE u.user_id=? ORDER BY t.created_at DESC", [user_id])
        rows = cursor.fetchall()
        tweets = []
        headers = [ i[0] for i in cursor.description]
        headers[7]="atNotice"
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ?", [row[0],])
            com_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ?", [row[0],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND user_id = ?", [row[0], checkuser_id])
            iflike = cursor.fetchone()[0]
            tweet = dict(zip(headers,row))
            tweet['com_amount'] = com_amount   
            tweet['like_amount'] = like_amount   
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
    
def postAuser(token, tweet_id, at_id):
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
            cursor.execute("INSERT INTO `@_users`(tweet_id, user_id) VALUES (?,?)", [tweet_id, at_id])
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
        
def editAuser(token, tweet_id):
    conn = None
    cursor = None
    row = None
    user_id = None
    try:
        print(tweet_id)
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        print(user_id)
        if user_id != None:
            cursor.execute("UPDATE `@_users` SET notice=0 WHERE tweet_id=? AND user_id=?", [tweet_id, user_id])
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

def getHash():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT h.hashTag , COUNT(*) FROM hash h GROUP BY h.hashTag ORDER BY 2 DESC")
        rows = cursor.fetchall()
        hash = []
        headers = [ i[0] for i in cursor.description]
        for row in rows:
            hash.append(dict(zip(headers,row)))   
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
        return hash
    
def getHashTweet(hashTag, user_id):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT h.hashTag , t.content ,t.id ,t.created_at ,t.image ,t.user_id ,u.username, u.url  FROM tweets t INNER JOIN users u ON u.id = t.user_id INNER JOIN hash h ON t.id = h.tweet_id WHERE h.hashTag=? ORDER BY t.created_at DESC", [hashTag,])
        rows = cursor.fetchall()
        hash = []
        headers = [ i[0] for i in cursor.description]
        print(rows)
        for row in rows:
            cursor.execute("SELECT COUNT(*) FROM comments c WHERE tweet_id = ?", [row[2],])
            com_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ?", [row[2],])
            like_amount = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM tweet_like WHERE tweet_id = ? AND user_id = ?", [row[2], user_id])
            iflike = cursor.fetchone()[0]
            tweet = dict(zip(headers,row))
            tweet['com_amount'] = com_amount   
            tweet['like_amount'] = like_amount   
            tweet['iflike'] = iflike
            hash.append(tweet)     
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
        return hash
    
def editHash(token, tweet_id, oldhash, newhash):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("UPDATE hash SET hashTag=? WHERE hashTag=? AND tweet_id=?", [newhash, oldhash, tweet_id])
            conn.commit()
            print("1")
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
        
def postHash(token, tweet_id, hashtag):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            cursor.execute("INSERT hash (hashTag, tweet_id) VALUES (?,?)", [hashtag, tweet_id])
            conn.commit()
            print("1")
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
        
def deleteHash(token, tweet_id, oldhash):
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM token WHERE token=?", [token,])
        user_id = cursor.fetchone()[0]
        if user_id != None:
            print(tweet_id)
            cursor.execute("DELETE FROM hash WHERE hashTag=? AND tweet_id=?", [oldhash, tweet_id])
            conn.commit()
            print("1")
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
