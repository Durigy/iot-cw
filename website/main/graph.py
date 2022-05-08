import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt

image_location = 'main/static/img/'

def intrusions_vs_time(device_id=''):
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

        plt.savefig(f"{image_location}{device_id}_intrusions_vs_time_graph.png")

        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

        return f"{device_id}_intrusions_vs_time_graph.png"

    except Exception as e:
        print("[error fetching data]")
        print(e)


def intrusions_vs_light_night(device_id=''):
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            database = "qume_iot_db",
            user = 'qume_iot_user',
            password = 'dasQuLHW8pC6CR8'
        )

        cursor = connection.cursor()

        query_intruder = 'select * from device_info where is_intruder="1"'

        cursor.execute(query_intruder)

        records = cursor.fetchall()

        # print(records)

        data = [0, 0] # data: index 0: light off, index 1: light on
        
        night_range = list(range(20, 24)) + list(range(0, 7)) # nighttime is 8pm to 6am
        print(night_range)

        for record in records:
            if record[1].hour in night_range:
                if not record[2]: #record[2] is light status
                    data[0] += 1
                else:
                    data[1] += 1
        

        print(data)

        plt.figure(figsize=(9, 6))

        plt.xlabel('Light status')#, labelpad=7)
        plt.ylabel('# of intrusions')
        plt.yticks([int(i) for i in data])

        plt.title("Intrusions during night time with different lighting conditions")

        plt.bar([0, 1], data, tick_label=['Off', 'On'])

        plt.savefig(f"{image_location}{device_id}_intrusions_vs_light_night_graph.png")

        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

        return f"{device_id}_intrusions_vs_light_night_graph.png"

    except Exception as e:
        print("[error fetching data]")
        print(e)


def vision_accuracy(device_id=''):
    # graph that displays how effective computer vision software updates have been
    # over time -> x axis one day, y axis average number of reset counter at that day
    # - the graph is supposed to decline to show that average reset_counter is reduced
    # over time  
    
    if not device_id:
        print('no device id; exiting...')
        return

    average_records = ''

    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            database = "qume_iot_db",
            user = 'qume_iot_user',
            password = 'dasQuLHW8pC6CR8'
        )
        
        cursor = connection.cursor()

        query = f'select time, reset_counter from device_info where device_id="{device_id}" order by time'

        cursor.execute(query)

        records = cursor.fetchall()

        # print([i[0] for i in records])

        # append 0 in front day and month
        dates = set([f'{i[0].year}/{i[0].month if len(str(i[0].month)) == 2 else f"0{i[0].month}"}/{i[0].day if len(str(i[0].day)) == 2 else f"0{i[0].day}"}' for i in records if i[1] is not None]) # dates for which we have data
        dates = {i: list() for i in dates} # convert to dictionary

        # print('dates' + str(dates)) # this works

        for record in records:
            if record[1] is not None:
                # append 0 in front day and month
                d = f'{record[0].day}' if len(str(record[0].day)) == 2 else f'0{record[0].day}'
                m = f'{record[0].month}' if len(str(record[0].month)) == 2 else f'0{record[0].month}'

                # dates[f'{d}/{m}/{record[0].year}'].append(record[1])
                dates[f'{record[0].year}/{m}/{d}'].append(record[1])
                # print(f'{record[0].day}/{record[0].month}/{record[0].year}' + ' - ' + f"{dates[f'{record[0].day}/{record[0].month}/{record[0].year}']}")
                # print(dates)

        # print('testing')

        # average number of resets per day - we use the average instead of the total number of attempts per day
        # because this way we take into account how many times the device has been called to check the password (i.e.
        # the user might use the device more in one day which means it might record more resets in total for that day without,
        # but we correct that by finding the average for that day)
        
        # check if data exists
        if len(dates) != 0:
            average_records = {i: round(sum(dates[i])/len(dates[i]), 3) for i in dates}
            #sort by date
            temp_sorted = sorted(average_records.items(), key = lambda x: int(''.join([i for i in x[0] if i.isnumeric()])))
            average_records = {i[0]:i[1] for i in temp_sorted}
            # print('testing')
            # print(average_records) # works

        # else:
        #     print('no data; exiting...')
        #     return

        plt.figure(figsize=(9, 6))
        
        plt.xlabel('Date')
        plt.ylabel('Average password resets per day')
        # plt.yticks([int(i) for i in records])

        plt.title("Computer vision accuracy (the lower the better)")
        
        if len(average_records) == 0:
            plt.savefig(f"{image_location}{device_id}_vision_accuracy_graph.png")
            return f'{device_id}_vision_accuracy_graph.png'
        elif len(average_records) == 1:
            plt.bar([i for i in average_records], [average_records[i] for i in average_records])#, tick_label=['Off', 'On'])
        else:
            plt.plot([i for i in average_records], [average_records[i] for i in average_records])#, tick_label=['Off', 'On'])

        plt.savefig(f"{image_location}{device_id}_vision_accuracy_graph.png")

        # print(average_records)

        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
        
        return f"{device_id}_vision_accuracy_graph.png"

    except Exception as e:
        print("[error fetching data]")
        print(e)


# vision_accuracy('5e5f65adc0d84b62317c')
