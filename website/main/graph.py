from cv2 import HOUGH_STANDARD
import mysql.connector

try:
    connection = mysql.connector.connect(
        host = '5qu.me',
        database = "qume_iot_db",
        user = 'qume_iot_user',
        password = 'dasQuLHW8pC6CR8'
    )

    cursor = connection.cursor()

    query = 'select reset_counter from device_info'

    cursor.execute(query)

    records = cursor.fetchall()

    for record in records:
        print(record)

except Exception as e:
    print("[error fetching data]")
    print(e)

finally:
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")