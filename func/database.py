import mysql.connector


def get_data_from_mysql():
    config = {
        "user": "security",
        "password": "mysql20011005",
        "host": "192.168.1.80",  # my ifconfig ip address: 192.168.1.80
        "database": "myemployees",
    }

    # 建立连接
    cnx = mysql.connector.connect(**config)

    # 创建一个游标对象
    cursor = cnx.cursor()

    # 执行一个查询
    query = "SELECT * FROM employees"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    # 关闭游标和连接
    cursor.close()
    cnx.close()

def main():
    get_data_from_mysql()

if __name__ == '__main__':
    main()