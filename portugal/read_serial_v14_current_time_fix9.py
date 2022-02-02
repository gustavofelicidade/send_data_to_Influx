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
    sendDataToInfluxDb(json_body)
    sys.stdout.flush()

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
    # ========================================================================================================
    # Write Serial Log plus timestamp on the sensor output file
    # line = ser.readline() <-- it is the Log
    # ========================================================================================================
    #if True:
    #    line = ser.readline()
    #    line = line.decode("utf-8", "backslashreplace")
    #    line = str(line + current_time)
    #
    #    with open("sensor_output.txt", 'w') as f:
    #        f.write("%s\n" % line)
    #
    # ========================================================================================================

    while True:
        try:
            line = ser.readline()
            response = line.decode("utf-8", "backslashreplace")
            response = response.rstrip()

            response_line = str(response + current_time)
            with open("sensor_output.txt", 'w') as f:
                f.write("%s\n" % response_line)


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
















