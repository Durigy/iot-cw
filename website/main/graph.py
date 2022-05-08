import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

def intrusions_vs_time():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            database = "qume_iot_db",
            user = 'qume_iot_user',
            password = 'dasQuLHW8pC6CR8'
        )

        cursor = connection.cursor()

        query_intruder = 'select time from device_info where is_intruder="1"'

        cursor.execute(query_intruder)

        records_intruder = cursor.fetchall()

        # print(records)

        times = {int(i): 0 for i in range(24)}

        for record in records_intruder:
            times[(record[0].hour + 1) % 24] += 1
            # print(record[0].hour + 1) # +1 for uk time

        # for key in times:
        #     print(f'{key}: {times[key]}')

        hours = list(times.keys())
        intruder_values = list(times.values())
        plt.figure(figsize=(9, 6))

        plt.xlabel('Time')#, labelpad=7)
        plt.ylabel('# of intrusions')

        plt.yticks([int(i) for i in intruder_values])

        ax = plt.gca()

        ax.tick_params(axis='x', labelrotation = 45)

        plt.title("Regional intrusions recorded at different times of day")

        plt.bar(hours, intruder_values, tick_label=[f'{i}:00' for i in hours])

        # plt.gcf().set_size_inches(50, plt.gcf().get_size_inches()[1])
        # plt.gcf().set_size_inches(50)

        plt.savefig("main/static/graph.png")

        return "graph.png"

    except Exception as e:
        print("[error fetching data]")
        print(e)

    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


# def intrusions_vs_light_night():
#     try:
#         connection = mysql.connector.connect(
#             host = '5qu.me',
#             database = "qume_iot_db",
#             user = 'qume_iot_user',
#             password = 'dasQuLHW8pC6CR8'
#         )

#         cursor = connection.cursor()

#         query_intruder = 'select * from device_info where is_intruder="1"'

#         cursor.execute(query_intruder)

#         records = cursor.fetchall()

#         # print(records)

#         data = [0, 0] # data: index 0: light off, index 1: light on
        
#         for record in records:
#             if record[1].hour in [i for i in range(6, 21)]:
#                 if not record[2]: #record[2] is light status
#                     data[0] += 1
#                 else:
#                     data[1] += 1
        

#         print(data)

#         plt.figure(figsize=(9, 6))

#         plt.xlabel('Light status')#, labelpad=7)
#         plt.ylabel('# of intrusions')
#         plt.yticks([int(i) for i in data])

#         plt.title("Intrusions ")

#         '''




#         plt.bar(hours, intruder_values, tick_label=[f'{i}:00' for i in hours])

#         # plt.gcf().set_size_inches(50, plt.gcf().get_size_inches()[1])
#         # plt.gcf().set_size_inches(50)

#         plt.savefig("static/graph.png")

#         # ax = plt.gca()
#         # ax.tick_params(axis='x', labelrotation = 45)
#         '''

#     except Exception as e:
#         print("[error fetching data]")
#         print(e)

#     finally:
#         if connection.is_connected():
#             connection.close()
#             cursor.close()
#             print("MySQL connection is closed")



# def intrusions_vs_light_night():
#     pass


# def vision_accuracy():
#     pass

# intrusions_vs_light_day()