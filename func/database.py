import mysql.connector
import pandas as pd


def get_data_from_mysql():
    # config = {
    #     "user": "security",
    #     "password": "mysql20011005",
    #     "host": "192.168.1.80",  # my ifconfig ip address: 192.168.1.80
    #     "database": "myemployees",
    # }
    config = {
        "user": "root",
        "password": "mysql20011005",
        "host": "127.0.0.1",  # my ifconfig ip address: 192.168.1.80
        "database": "myemployees",
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    table_names = ["employees", "checkIn", "salary", "holidays"]
    dataframes = {}

    for table_name in table_names:
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()
        # print(rows[:5])
        column_names = [i[0] for i in cursor.description]
        dataframes[table_name] = pd.DataFrame(rows, columns=column_names).to_dict(
            orient="records"
        )
    cursor.close()
    cnx.close()
    # print(dataframes["employees"].info())
    return (
        dataframes["employees"],
        dataframes["checkIn"],
        dataframes["salary"],
        dataframes["holidays"],
    )


def main():
    get_data_from_mysql()


if __name__ == "__main__":
    main()
