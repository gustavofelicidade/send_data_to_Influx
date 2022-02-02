import time



json_body = [
        {
            "measurement": "sensor",
            "tags": {
                "host": 'hostname',
                "sensor": 'sensor_id',
            },
            "fields": {
                "battery4": 'int(line[13:16]) / 100',
                "battery3": 'int(line[16:19]) / 100',
                "sensor1": 'int(line[19:23]) / 1000',
                "sensor2": 'int(line[23:27]) / 1000',
                "sensor3": 'int(line[27:31]) / 1000',
                "sensor4": 'int(line[31:35]) / 1000',
                "sensor5": 'int(line[35:39]) / 1000',
                "sensor6": 'int(line[39:43]) / 1000',
                "sensor7": 'int(line[43:47]) / 1000',
                "sensor8": 'int(line[47:51]) / 1000',
                "sensor9": 'int(line[51:55]) / 1000',
                "count1": 'int(line[55:59]) / 2',
                "count2": 'int(line[59:63]) / 2',

                # "sensor9":  int(2500) /1000,
            }
        }
    ]

#========================================================================================================
# Converting List
#========================================================================================================

print(type(json_body))

# Function to transform the list of 1 string in list chars
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += str(ele)
    return str1
new = listToString(json_body)  # new list called new

#========================================================================================================

print('--------------------------')


li = new.split(',')  # transform chars into  string lines
print('--------------------------')
print(len(li))
print(type(li))
print("\n".join(li))
print('--------------------------')
#print(len(li))

field_list = []  # removing unnecessary lines

for i in li[3:16]:   # slicing
    field_list.append(i)

print('sliced:')
print("\n".join(field_list))
print('size of field_list')
print(len(field_list))
print('first element:')
print(field_list[0:1])
#print(li[3:16])

# Remove character from Strings list
# using list comprehension + replace()
field_list = [ele.replace("'fields': {", '') for ele in field_list]
field_list = [ele.replace("}", '') for ele in field_list]
#print("\n")
#print("field_list formatted")
#print("\n".join(field_list))
#print(len(field_list))


#========================================================================================================
# Adding current time
#========================================================================================================

current_time = str(int(round(time.time() * 1000)))

add_time = []
for i in field_list:
    time_now = i+current_time
    add_time.append(time_now)

# Transform the string data to int again
add_time = [ele.replace("': ", "': int(") for ele in add_time]
add_time = [ele.replace("0'", "0')") for ele in add_time]
add_time = [ele.replace("/ 2'", "/ 2')") for ele in add_time]
#print('--------------------------')
#print("To add inside the beforeDBProcessing(line) function \n and write to file later:  ")
#print("\n".join(add_time))


#Prepare to keys and values
#field_list_val = [ele.replace("'", '') for ele in field_list]
#field_list_val = [ele.replace("'", '') for ele in add_time]
#========================================================================================================
# Transform to dictionary (if needed)
#========================================================================================================


# Convert String List to Key-Value List dictionary
# Using split() + dictionary comprehension

#res = {sub[0]: sub[1:] for sub in (ele.split(': ') for ele in field_list)}


#res_val = {sub[0]: sub[1:] for sub in (ele.split(': ') for ele in field_list_val)}

print('--------------------------')

#========================================================================================================
# Write to file "sensor_output.txt"
#========================================================================================================

def openTheOuputFile():
    write_to_file_path = "sensor_output.txt"
    file_obj = open(write_to_file_path, "a")
    return file_obj

output_file = openTheOuputFile()

output_file.write(str("\n".join(add_time) + "\n"))

#========================================================================================================
# Test dict to write on file
#========================================================================================================


# Original line for test contains number that cannot be divided.
line = '0113810010001022530004000400030003000400030000'



# Test line value

line = '0113810010001022530004000400030003000400039876'


dict_one = {
"battery4" : (line[13:16]),
"battery3" : (line[16:19]),
"sensor1" : (line[19:23]),
"sensor2" : (line[23:27]),
"sensor3" : (line[27:31]),
"sensor4" : (line[31:35]),
"sensor5" : (line[35:39]),
"sensor6" : (line[39:43]),
"sensor7" : (line[43:47]),
"sensor8" : (line[47:51]),
"sensor9" : (line[51:55]),
"count1" : (line[55:59]),
"count2" : (line[59:63]),
}


# Do the division
# Transform to str to concatenate
# Transform to

sensor_id = line[0:3]


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

print('sensor_id =  {}'.format(sensor_id))
print('battery4 =  {}'.format(battery4))
print('battery3 =  {}'.format(battery3))
print('sensor1=  {}'.format(sensor1))
print('sensor2=  {}'.format(sensor2))
print('sensor3=  {}'.format(sensor3))
print('sensor4=  {}'.format(sensor4))
print('sensor5=  {}'.format(sensor5))
print('sensor6=  {}'.format(sensor6))
print('sensor7=  {}'.format(sensor7))
print('sensor8=  {}'.format(sensor8))
print('sensor9=  {}'.format(sensor9))
print('count1=  {}'.format(count1))
print('count2=  {}'.format(count2))


print('---------------------')

print(dict_one.items())


with open("myfile.txt", 'w') as f:
    for key, value in dict_one.items():
        f.write('%s:%s\n' % (key, value))
