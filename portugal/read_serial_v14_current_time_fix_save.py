


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
    obj = InfluxDB('95.xxx.144.254', 8086, 'xxxx', 'xxxx')  # make an object of InfluxDB class
    obj.getConnection()  # Get connection to the influxdb server
    # obj.getDbList() # Get List of database stored in influxdb
    # obj.createDB('DBname') # By passing dbname you can create database
    obj.selectDB('xxxxx')  # input the name of db you want to select
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
        sock = socket.create_connection(("www.abcd.com", 80))
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


# Function to transform the list of 1 string in list chars
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += str(ele)
    return str1

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
                "battery4": int(line[13:16]) / 100,
                "battery3": int(line[16:19]) / 100,
                "sensor1": int(line[19:23]) / 1000,
                "sensor2": int(line[23:27]) / 1000,
                "sensor3": int(line[27:31]) / 1000,
                "sensor4": int(line[31:35]) / 1000,
                "sensor5": int(line[35:39]) / 1000,
                "sensor6": int(line[39:43]) / 1000,
                "sensor7": int(line[43:47]) / 1000,
                "sensor8": int(line[47:51]) / 1000,
                "sensor9": int(line[51:55]) / 1000,
                "count1": int(line[55:59]) / 2,
                "count2": int(line[59:63]) / 2,

                # "sensor9":  int(2500) /1000,
            }
        }
    ]
    sendDataToInfluxDb(json_body)
    sys.stdout.flush()

    new = listToString(json_body)
    li = new.split(',')  # transform chars into  string lines

    field_list = []  # removing unnecessary lines

    for i in li[3:16]:  # slicing
        field_list.append(i)

    # Remove character from Strings list
    # using list comprehension + replace()
    field_list = [ele.replace("'fields': {", '') for ele in field_list]
    field_list = [ele.replace("}", '') for ele in field_list]

    # ========================================================================================================
    # Adding current time
    # ========================================================================================================

    add_time = []
    for i in field_list:
        time_now = i + current_time
        add_time.append(time_now)

    # Transform the string data to int again
    add_time = [ele.replace("': ", "': int(") for ele in add_time]
    add_time = [ele.replace("0'", "0')") for ele in add_time]
    add_time = [ele.replace("/ 2'", "/ 2')") for ele in add_time]

    # ========================================================================================================
    # Write to file "sensor_output.txt"
    # ========================================================================================================

    output_file = openTheOuputFile()

    output_file.write(str("\n".join(add_time) + "\n"))


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

