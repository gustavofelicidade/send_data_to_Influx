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


def sendDataToInfluxDb(data):
    obj = InfluxDB('95.216.144.254', 8086, 'sensor02', 'itss2020')  # make an object of InfluxDB class
    obj.getConnection()  # Get connection to the influxdb server
    # obj.getDbList() # Get List of database stored in influxdb
    # obj.createDB('DBname') # By passing dbname you can create database
    obj.selectDB('sensor02')  # input the name of db you want to select
    ##obj.checkTable()  # it will fetch all the tables stored in the selected database
    # obj.fetchData('') # input a sql query in the function and get the results eg. "select * from table name"
    if obj.insertData(data):
        print("record enter successfully")


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


def thread_process_data(data_queue, serial_port):
    while True:
        line = data_queue.get()

        if line == "KILL":
            break
        else:
            print("Message received is {}".format(line))
            print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
            if not isOK(line):
                sensor_id = line[0:3]
                print("Message is invalid. Sending NOK to sensor {}".format(sensor_id))
                print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
                time.sleep(0.3)
                serial_port.write("#,SendData,*".encode("utf-8"))
                print("SendData")
                time.sleep(2.0)
                serial_port.write("#,SendData,*".encode("utf-8"))
                print("SendData2")

                sys.stdout.flush()
            else:
                output_file = openTheOuputFile()
                output_file.write(str(line + "\n"))
                output_file.flush()
                sensor_id = line[0:3]
                print("Valid Message received. Sending OK to sensor {}".format(sensor_id))
                print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
                ok_line = "#," + sensor_id + "OK,*"
                #serial_port.write(ok_line.encode("utf-8"))
                json_body = [
                    {
                        "measurement": "sensor",
                        "tags": {
                            "host": 'hostname',
                            "sensor": sensor_id,
                        },
                        "fields": {
                            "battery4": int(line[13:16]) /100,
                            "battery3": int(line[16:19]) /100,
                            "sensor1":  int(line[19:23]) /1000,
                            "sensor2":  int(line[23:27]) /1000,
                            "sensor3":  int(line[27:31]) /1000,
                            "sensor4":  int(line[31:35]) /1000,
                            "sensor5":  int(line[35:39]) /1000,
                            "sensor6":  int(line[39:43]) /1000,
                            "sensor7":  int(line[43:47]) /1000,
                            "sensor8":  int(line[47:51]) /1000,
                            "sensor9":  int(line[51:55]) /1000,
                            #"sensor9":  int(2500) /1000,
                        }
                    }
                ]
                sendDataToInfluxDb(json_body)
                sys.stdout.flush() 


def openTheOuputFile():
    write_to_file_path = "sensor_output.txt"
    file_obj = open(write_to_file_path, "a")
    return file_obj

output_file = " "
def main():
    sys.stdout=open("serial.log","a")
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

    print("Created Port")
    data_rx_queue = queue.Queue()
    #lock =threading.Lock()
    process_thread = threading.Thread(target=thread_process_data, args=(data_rx_queue, ser))
    process_thread.start()
    
    while True:
        try:
            line = ser.readline()
            response = line.decode("utf-8","backslashreplace")
            response = response.rstrip()
            if response not in (None, "", " "):
                if response in ("OK") or  response.find("datalogPCB") > -1:
                    print("OK received")
                    print("DATE: ", datetime.datetime.now().strftime("%y-%m-%d %H:%M"))
                    sys.stdout.flush()
                else:
                    if not checkIfLineInFile(response):
                        data_rx_queue.put(response) 
                        print("Only send unique and no noise")
                        sys.stdout.flush()
                    else:
                        print('Duplicate msg received')
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






