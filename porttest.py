#!/usr/bin/env python3
import socket
import subprocess
import sys

from datetime import datetime,timezone
from tabulate import tabulate

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

def telnet_test(Server_IP, Target_Port):
    result_list = []
    remoteServerIP = socket.gethostbyname(Server_IP)
    try:
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((remoteServerIP, Target_Port))
            result_list.append([" ", Target_Port, "Telnet Succeeded", aslocaltimestr(datetime.utcnow())])
            return result_list
            sock.close()
        except:
            result_list.append([" ", Target_Port, "Telnet Failed", aslocaltimestr(datetime.utcnow())])
            return result_list
            sock.close()

    except KeyboardInterrupt:
        print("You pressed Ctrl+C")
        sys.exit()
    
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

def print_table(table, header, format):
    print(tabulate(table, header, tablefmt=format))

def clear_screen():
    # Clear the screen
    subprocess.call('clear', shell=True)

def list_resequence(original_list):

    temp_list = []
    
    i = 0

    for i in range(len(original_list)):
        print("Current Port: ", original_list[i])
        if ':' in original_list[i]:
            start, end = map(int, original_list[i].split(":"))
            # Swap starting port and ending port if it is input wrongly.
            if start > end:
                start, end = end, start
            temp_list.extend(range(start, end))
        else:
            temp_list.append(int(original_list[i]))
        i += 1

    temp_list.sort()
    return set(temp_list)

def main():
    
    clear_screen()

    Test_List = [
        {"Server IP": "192.168.11.20", "Ports": ["20", "138","21:23","139"]},
        {"Server IP": "192.168.11.21", "Ports": ["25:23"]}
    ]
    
    result_table_header = ["Server IP", "TCP Port","Telnet Test Result", "Test Time"]
    result_table = []

    # Start Time
    starttime = datetime.utcnow()

    for server in Test_List:
        result_table.append([server["Server IP"], " "," "," "])
        for port in server["Ports"]:
            if "-" in port:
                port_start, port_end = map(int, port.split("-"))
                # Swap starting port and ending port if it is input wrongly.
                if port_start > port_end:
                    port_start, port_end = port_end, port_start
                for port in range(port_start, port_end + 1):
                    result_table.extend(telnet_test(server["Server IP"], int(port)))
            elif ":" in port:
                port_start, port_end = map(int, port.split(":"))
                # Swap starting port and ending port if it is input wrongly.
                if port_start > port_end:
                    port_start, port_end = port_end, port_start
                for port in range(port_start, port_end + 1):
                    result_table.extend(telnet_test(
                        server["Server IP"], int(port)))
            else:
                result_table.extend(telnet_test(server["Server IP"], int(port)))
        result_table.append(["---", "---", "---", "---"])

    # End Time
    # Calculates the difference of time, to see how long it took to run the script
    endtime = datetime.utcnow()
    total = endtime - starttime

    timetable = []
    timetable.append(["Testing Start Time", aslocaltimestr(starttime)])
    timetable.append(["Testing End Time", aslocaltimestr(endtime)])
    timetable.append(["Completed in",str(total)])

    print_table(timetable, "", "fancy_grid")
    print_table(result_table, result_table_header, "fancy_grid")

if __name__ == '__main__':
    main()
