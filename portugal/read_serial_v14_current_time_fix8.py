##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed
# !/usr/bin/python3

from influxdb import InfluxDBClient
import datetime
import serial
import time
import os
import sys
import re
import threading
import queue
import os.path
from os import path

import timeit


class InfluxDB:
    def __init__(self, host, port, username, pssw):
        self.host = host
        self.port = port
        self.username = username
        self.pssw = pssw
        self.client = None

    def getConnection(self):
        self.client = InfluxDBClient(self.host, self.port, self.username, self.pssw)
        return self.client

    def getDbList(self):
        print(self.client.get_list_database())

    def selectDB(self, dbname):
        return self.client.switch_database(dbname)

    def checkTable(self):
        print(self.client.get_list_measurements())

    def createDB(self, dbname):
        self.client.create_database(dbname)

    def insertData(self, jsonData):
        self.client.write_points(jsonData)

    def fetchData(self, q):
        return self.client.query(q)


def sendDataToInOracle(data):
    pass


def sendDataToInfluxDb(data):
    obj = InfluxDB('95.216.144.254', 8086, 'sensor1', 'itss2020')  # make an object of InfluxDB class
    obj.getConnection()  # Get connection to the influxdb server
    # obj.getDbList() # Get List of database stored in influxdb
    # obj.createDB('DBname') # By passing dbname you can create database
    obj.selectDB('sensor1')  # input the name of db you want to select
    #  obj.checkTable()  # it will fetch all the tables stored in the selected database
    # obj.fetchData('') # input a sql query in the function and get the results eg. "select * from table name"
    if obj.insertData(data):
        print("record enter successfully")


# bug in memoria
# duplicada -> Garbage Collector
# maybe we need to use del command


def checkIfLineInFile(string_to_search):
    with open('sensor_output.txt', 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
        return False


def isOK(line):
    if len(line) > 40:
        pattern = "^[0-9]*$"
        match = re.match(pattern, line)
        if match != None:
            return True
        else:
            print("Message contains invalid characters")
            print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
            sys.stdout.flush()
            return False
    else:
        print("Invalid Message length {}".format(len(line)))
        print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
        sys.stdout.flush()


def isConnected():
    import socket
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("www.google.com", 80))
        if sock is not None:
            sock.close
        return True
    except OSError:
        pass
    return False


def openTheOuputFile():
    write_to_file_path = "sensor_output.txt"
    file_obj = open(write_to_file_path, "a")
    return file_obj


current_time = str(int(round(time.time() * 1000)))  # Global variable current_time


def beforeDBProcessing(line):

    sensor_id = line[0:3]
    print("Valid Message received. Sending OK to sensor {}".format(sensor_id))
    print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
    ok_line = "#," + sensor_id + "OK,*"
    # serial_port.write(ok_line.encode("utf-8"))

    json_body = [
        {
            "measurement": "sensor",
            "tags": {
                "host": 'hostname',
                "sensor": sensor_id,
            },
            "fields": {
                "battery3": int(line[3:6]) / 100,
                "battery4": int(line[3:6]) / 100,
                "sensor1": int(line[6:10]) / 1000,
                "sensor2": int(line[10:14]) / 1000,
                "sensor3": int(line[14:18]) / 1000,
                "sensor4": int(line[18:22]) / 1000,
                "sensor5": int(line[22:26]) / 1000,
                "sensor6": int(line[26:30]) / 1000,
                "sensor7": int(line[30:34]) / 1000,
                "sensor8": int(line[34:38]) / 1000,
                "sensor9": int(line[38:42]) / 1000,
                "count1": int(int(line[42:44]) / 2),
                "count2": int(int(line[44:47]) / 2),

                # "sensor9":  int(2500) /1000,
            }
        }
    ]
    send_to_influxDB = sendDataToInfluxDb(json_body)
    send_to_influxDB()
    sys.stdout.flush()

    # ========================================================================================================
    # Dict to handle output data
    # ========================================================================================================

    dict_one = {
        "battery3": (line[10:14]),
        "battery4": (line[6:10]),
        "sensor1": (line[14:18]),
        "sensor2": (line[23:27]),
        "sensor3": (line[14:18]),   
        "sensor4": (line[31:35]),
        "sensor5": (line[35:39]),
        "sensor6": (line[39:43]),
        "sensor7": (line[43:47]),
        "sensor8": (line[47:51]),
        "sensor9": (line[51:55]),
        "count1": (line[55:59]),
        "count2": (line[59:63]),
    }



    # ========================================================================================================
    # Test dict to write on file
    # ========================================================================================================

    battery4 = line[6:10]
    battery3 = line[10:14]
    sensor1 = line[14:18]
    sensor2 = line[23:27]
    sensor3 = line[27:31]
    sensor4 = line[18:22]
    sensor5 = line[22:26]
    sensor6 = line[26:30]
    sensor7 = line[30:34]
    sensor8 = line[34:38]
    sensor9 = line[38:42]
    count1 = line[42:44]
    count2 = line[44:47]

    battery4 = int(battery4) / 100
    battery3 = int(battery3) / 100
    sensor1 = int(sensor1) / 1000
    sensor2 = int(sensor2) / 1000
    sensor3 = int(sensor3) / 1000
    sensor4 = int(sensor4) / 1000
    sensor6 = int(sensor6) / 1000
    sensor5 = int(sensor5) / 1000
    sensor7 = int(sensor7) / 1000
    sensor8 = int(sensor8) / 1000
    sensor9 = int(sensor9) / 1000
    count1 = int(count1) / 2
    count2 = int(count2) / 2

    battery4 = str(battery4) + current_time
    battery3 = str(battery3) + current_time
    sensor1 = str(sensor1) + current_time
    sensor2 = str(sensor2) + current_time
    sensor3 = str(sensor3) + current_time
    sensor4 = str(sensor4) + current_time
    sensor5 = str(sensor5) + current_time
    sensor6 = str(sensor6) + current_time
    sensor7 = str(sensor7) + current_time
    sensor8 = str(sensor8) + current_time
    sensor9 = str(sensor9) + current_time
    count1 = str(count1) + current_time
    count2 = str(count2) + current_time

    dict_one["battery4"] = battery4
    dict_one["battery3"] = battery3
    dict_one["sensor1"] = sensor1
    dict_one["sensor2"] = sensor2
    dict_one["sensor3"] = sensor3
    dict_one["sensor4"] = sensor4
    dict_one["sensor5"] = sensor5
    dict_one["sensor6"] = sensor6
    dict_one["sensor7"] = sensor7
    dict_one["sensor8"] = sensor8
    dict_one["sensor9"] = sensor9
    dict_one["count1"] = count1
    dict_one["count2"] = count2

    # ========================================================================================================
    # Uncomment to see the output on terminal
    # ========================================================================================================

    #print('sensor_id = {}'.format(sensor_id))
    #print('battery4 = {}'.format(battery4))
    #print('battery3 = {}'.format(battery3))
    #print('sensor1 = {}'.format(sensor1))
    #print('sensor2 = {}'.format(sensor2))
    #print('sensor3 = {}'.format(sensor3))
    #print('sensor4 = {}'.format(sensor4))
    #print('sensor5 = {}'.format(sensor5))
    #print('sensor6 = {}'.format(sensor6))
    #print('sensor7 = {}'.format(sensor7))
    #print('sensor8 = {}'.format(sensor8))
    #print('sensor9 = {}'.format(sensor9))
    #print('count1 = {}'.format(count1))
    #print('count2 = {}'.format(count2))

    # ========================================================================================================
    # Write line by line on the sensor output file
    # ========================================================================================================

    #with open("sensor_output.txt", 'w') as f:
        #for key, value in dict_one.items():
            #f.write('%s:%s\n' % (key, value))




def notConnected():
    write_to_file_path = "no_internet_output.txt"
    file_obj = open(write_to_file_path, "a")
    return file_obj


def thread_process_data(data_queue, serial_port):
    # Data is placed from sensor into queue

    while True:
        # Fetch the data first element from queue
        line = data_queue.get()

        # Check if Line is Kill
        if line == "KILL":
            break
            # Break While loop
        else:
            # Queue has element then put received Status

            print("Message received is {}".format(line))
            print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

            # Check if received line has valid entries in it
            # If it has invalid line then send NOK to sensor
            # if is has valid line then send OK to sensor
            if not isOK(line):
                sensor_id = line[0:3]
                print("Message is invalid. Sending NOK to sensor {}".format(sensor_id))
                print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
                time.sleep(0.5)
                serial_port.write("#,SendData,*".encode("utf-8"))
                # print("SendData")
                time.sleep(2.0)
                ##serial_port.write("#,SendData,*".encode("utf-8"))
                # print("SendData2")

                sys.stdout.flush()
            else:
                # Logic for internet Connection

                if not isConnected():
                    pass
                    #not_connected = notConnected(line)
                    #for line in not_connected:
                        #not_connected.write(str(line + current_time + "\n"))

                else:
                    import os
                    if path.exists("no_internet_output.txt"):
                        if not os.stat("no_internet_output.txt").st_size == 0:
                            lines = open("no_internet_output.txt", 'r+')
                            for line in lines:
                                beforeDBProcessing(line)
                            lines.truncate(0)
                            lines.close()
                            continue
                    beforeDBProcessing(line)

                # ------------------------------


output_file = " "


def main():
    sys.stdout = open("serial.log", "a")
    baud_rate = 115200
    serial_port = '/dev/ttyS1'
    ##serial_port = 'COM16'
    ser = serial.Serial(serial_port,
                        baud_rate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0.1
                        )

    output_file = openTheOuputFile()

    print("Created Port V13")
    data_rx_queue = queue.Queue()
    # lock =threading.Lock()
    process_thread = threading.Thread(target=thread_process_data, args=(data_rx_queue, ser))
    process_thread.start()

    while True:
        try:
            line = ser.readline()
            response = line.decode("utf-8", "backslashreplace")
            response = response.rstrip()
            if response not in (None, "", " "):
                if response in ("OK") or response.find("datalogPCB") > -1:
                    print("OK received")
                    print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))

                    # ========================================================================================================
                    # Write Serial Log plus timestamp on the sensor output file
                    # line = ser.readline() <-- it is the Log
                    # ========================================================================================================
                    line = str(line + current_time)

                    with open("sensor_output.txt", 'w') as f:
                        f.write("%s\n" % (line))

                    # ========================================================================================================

                    sys.stdout.flush()
                else:
                    if not checkIfLineInFile(response):
                        data_rx_queue.put(response)
                        print("Only send unique and no noise")
                        print('noise {}'.format(line))
                        print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
                        sys.stdout.flush()
                    else:
                        print('Duplicate msg received')
                        print('Duplicated msg is {}'.format(line))
                        print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
                        sys.stdout.flush()


            else:
                pass
                # print ("Serial read timeout.")
        except KeyboardInterrupt:
            print("Keyboard Interrup recvied.  Quitting")
            data_rx_queue.put("KILL")
            time.sleep(0.5)
            try:
                ser.close()
                break
            except:
                pass
        except Exception as e:
            print("Exception is {}".format(e))
    output_file.close()
    sys.stdout.close()


if __name__ == "__main__":
    main()
















