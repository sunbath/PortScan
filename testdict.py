#!/usr/bin/env python3

#Test_List = [
#    {"Server IP": "192.168.11.20", "Ports": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12]},
#    {"Server IP": "192.168.11.20", "Ports": [11,12,13,14,15,16,17,18,19,20,21,22]}]

#for server in Test_List:
#    for port in server["Ports"]:
#        print(server["Server IP"],port)

#port_list = ["20", "138", "21:23", "139"]

def list_process(original_list):
    temp_list = []

    i = 0

    for i in range(len(original_list)):
        #print("Inside Function -- Current Port: ",original_list[i])
        if ':' in original_list[i]:
            start, end = map(int, original_list[i].split(":"))
            # Swap starting port and ending port if it is input wrongly.
            if start > end:
                start, end = end, start
            temp_list.extend(range(start, end+1))
            #print("Inside Function -- temp_list: ", temp_list)
        elif '-' in original_list[i]:
            start, end = map(int, original_list[i].split("-"))
            # Swap starting port and ending port if it is input wrongly.
            if start > end:
                start, end = end, start
            temp_list.extend(range(start, end+1))
            #print("Inside Function -- temp_list: ", temp_list)
        else:
            temp_list.append(int(original_list[i]))
            #print("Inside Function -- temp_list: ", temp_list)
        i += 1

    temp_list = list(set(temp_list))
    temp_list.sort()
    print(temp_list)
    return temp_list

def main():
    original_list = ["21:30", "138", "20-22"]
    original_list = list_process(original_list)
    print("Main Function -- original_list is: ",original_list)

if __name__ == '__main__':
    main()
