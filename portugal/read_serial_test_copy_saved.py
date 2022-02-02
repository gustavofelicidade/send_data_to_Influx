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

#print(json_body)
#print('--------------------------')
print(type(json_body))

# Function to transform the list of 1 string in list chars
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += str(ele)
    return str1
new = listToString(json_body)  # new list called new

#========================================================================================================

#print(new)
#print('--------------------------')
#print(type(new))
#print('--------------------------')
#print(len(new))


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
print("\n")
print("field_list formatted")
print("\n".join(field_list))
print(len(field_list))


#========================================================================================================
# Adding current time
#========================================================================================================

current_time = str(int(round(time.time() * 1000)))

add_time = []
for i in field_list:
    time_now = i+current_time
    add_time.append(time_now)


#Prepare to keys and values
#field_list_val = [ele.replace("'", '') for ele in field_list]
field_list_val = [ele.replace("'", '') for ele in add_time]
#========================================================================================================
# Transform to dictionary
#========================================================================================================
print('--------------------------')
current_time = str(int(round(time.time() * 1000)))
# Python3 code to demonstrate working of
# Convert String List to Key-Value List dictionary
# Using split() + dictionary comprehension

# initializing list
#test_list = ["gfg is best for geeks", "I love gfg", "CS is best subject"]

# printing string
#print("The original list : " + str(field_list))

# using dictionary comprehension to solve this problem
res = {sub[0]: sub[1:] for sub in (ele.split(': ') for ele in field_list)}
#print(type(res))
#print(res)
# printing results

#for key, value in res.items():  #accessing values
    #print(value, end="\n")
#print('\n')
#print("The key values List dictionary : " + str(res))


print('--------------------------')
print("less ' ")
#print('\n')
res_val = {sub[0]: sub[1:] for sub in (ele.split(': ') for ele in field_list_val)}
#print(type(res))
#print(res)
for key, value in res_val.items():  #accessing values
    print(value, end="\n")
#print('\n')
print('--------------------------')
#print('Separating keys and values')
#field_to_dict = [word for line in field_list for word in line.split(': ')]



#print(len(field_to_dict))
#print("\n".join(field_to_dict))




#print('--------------------------')
#========================================================================================================
# Adding current time
#========================================================================================================

current_time = str(int(round(time.time() * 1000)))

add_time = []
for i in li:
    time_now = i+current_time
    add_time.append(time_now)


#print("\n".join(add_time))
print('--------------------------')
#print(new[78:88])  # fields

'''
final = new[91:]
final = final.replace("}", "").replace(",","").split()
print(final)
print('--------------------------')
print(len(final))
#print(final.split(','))
print('--------------------------')
print(type(final))
print('--------------------------')
print("\n".join(final))'''


#========================================================================================================
# Write to file "sensor_output.txt"
#========================================================================================================

def openTheOuputFile():
    write_to_file_path = "sensor_output.txt"
    file_obj = open(write_to_file_path, "a")
    return file_obj

write_file = openTheOuputFile()

