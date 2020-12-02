import mariadb
import dbcreds
from datetime import datetime

def getmessages(user_id, chatwith_id):
    conn = None
    cursor = None
    row = []
    try:
        conn = mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
        cursor = conn.cursor()
        
        if chatwith_id == None:
            cursor.execute("SELECT u.username, u.id, u.url FROM message m INNER JOIN users u ON u.id = m.sender_id WHERE receiver_id = ?", [user_id,]) 
            messages=[]
            row1 = cursor.fetchall()
            cursor.execute("SELECT u.username, u.id, u.url FROM message m INNER JOIN users u ON u.id = m.receiver_id WHERE m.sender_id = ?", [user_id,]) 
            row2 = cursor.fetchall()
            rows = row1 + row2
            rows = list(dict.fromkeys(rows))
            for row in rows:
                cursor.execute("SELECT COUNT(*) FROM message WHERE sender_id = ? AND notice = 1 AND receiver_id =? ", [row[1], user_id])
                count = cursor.fetchone()[0]
                chat={}
                chat["chatwith"] = row[0]
                chat["chatId"] = row[1]
                chat["chatUrl"] = row[2]
                chat["new"] = count
                messages.append(chat)
                    
                        
            
            # cursor.execute("SELECT m.sender_id ,m.receiver_id FROM message m WHERE receiver_id = ? or sender_id = ?", [user_id, user_id])
            # rows = cursor.fetchall()
            # datas = []
            # messages=[]
            # for row in rows:
            #     if [row[0], row[1]] not in datas and [row[1], row[0]] not in datas:
            #         datas.append([row[0], row[1]])
            # for data in datas:
            #     chat = {}
            #     if user_id == str(data[0]):
            #         print('a')
            #         cursor.execute("SELECT COUNT(*) FROM message WHERE sender_id = ? AND notice = 1 AND receiver_id =? ", [data[1], user_id])
            #         count = cursor.fetchone()[0]
            #         chat["user"] = user_id
            #         chat["chatwith"] = data[1]
            #         chat["new"] = count
            #         print(chat)
            #     else:
            #         print("b")
            #         cursor.execute("SELECT COUNT(*) FROM message WHERE sender_id = ? AND notice = 1 AND receiver_id =? ", [data[0], user_id])
            #         count = cursor.fetchone()[0]
            #         chat["user"] = user_id
            #         chat["chatwith"] = data[0]
            #         chat["new"] = count
            #         print(chat)
            #     messages.append(chat)        
        else:
            cursor.execute("SELECT m.id ,m.content ,m.sender_id ,u.username ,u.url, m.receiver_id , u2.username , u2.url , m.sent_time, m.notice FROM message m INNER JOIN users u ON m.sender_id = u.id INNER JOIN  users u2 ON u2.id = m.receiver_id WHERE m.receiver_id=? AND m.sender_id=? OR m.receiver_id = ? AND m.sender_id = ? ORDER BY m.sent_time DESC ", [user_id, chatwith_id, chatwith_id, user_id])
            rows = cursor.fetchall()
            messages = []
            headers = [ i[0] for i in cursor.description]
            headers[3]="senderName"
            headers[4]="senderUrl"
            headers[6]="receiverName"
            headers[7]="receiverUrl"
            for row in rows:
                messages.append(dict(zip(headers,row)))
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
        if user_id != None:
            date = str(datetime.now())[0:18]
            cursor.execute("INSERT INTO message(content, sender_id, receiver_id, sent_time) VALUES (?,?,?,?)", [content, user_id, receiver_id, date])
            conn.commit()
            row = cursor.rowcount
            print(row)
            if row == 1:
                cursor.execute("SELECT m.id ,m.content ,m.sender_id ,u.username ,u.url, m.receiver_id , u2.username , u2.url , m.sent_time, m.notice FROM message m INNER JOIN users u ON m.sender_id = u.id INNER JOIN  users u2 ON u2.id = m.receiver_id WHERE m.sender_id=? AND sent_time=? ", [user_id, date])
                rows = cursor.fetchone()
                message = {}
                headers = [ i[0] for i in cursor.description]
                headers[3]="senderName"
                headers[4]="senderUrl"
                headers[6]="receiverName"
                headers[7]="receiverUrl"
                message = dict(zip(headers,rows))   
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
            return message
        else:
            return False
        
def editMessage(token, message_id):   
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
            cursor.execute("UPDATE message SET notice=0 WHERE id=? AND receiver_id=?", [message_id, user_id])
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
        
