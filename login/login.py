
users = {}

def is_null(username, password):
    if (username == '' or password == ''):
        return True
    else:
        return False


def is_existed(username, password):
    sql = 'SELECT * FROM users WHERE username ="%s" and password ="%s"' % (username, password)
    cur.execute(sql)
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True


def exist_user(username):
    sql = 'SELECT * FROM users WHERE username ="%s"' % (username)
    cur.execute(sql)
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True