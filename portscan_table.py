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

# Clear the screen
subprocess.call('clear', shell=True)

Test_List = [
    {"Server IP": "192.168.11.20", "Ports": [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]},
    {"Server IP": "192.168.11.20", "Ports": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]}]

for server in Test_List:
    for port in server["Ports"]:
        print(server["Server IP"], port)

# Ask for input
#remoteServer = input("Enter a remote host to scan: ")

remoteServer = Test_list()
remoteServerIP = socket.gethostbyname(remoteServer)

result_table_header = ["Server IP", "TCP Port", "Telnet Test Result","Test Time"]
result_table = []

# Start Time
starttime = datetime.utcnow()

# Using the range function to specify ports (here it will scans all ports between 1 and 1024)
try:
    for port in range(1, 23):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((remoteServerIP,port))
            result_table.append([remoteServerIP, port, "Telnet Success",aslocaltimestr(datetime.utcnow())])
            sock.close()
        except:
            result_table.append([remoteServerIP, port, "Telnet Failed",aslocaltimestr(datetime.utcnow())])
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

# End Time
#endtime = timezone.localize(datetime.now())
# Calculates the difference of time, to see how long it took to run the script
endtime = datetime.utcnow()
total = endtime - starttime

timetable = []
timetable.append(["Testing Start Time", aslocaltimestr(starttime)])
timetable.append(["Testing End Time", aslocaltimestr(endtime)])
timetable.append(["Completed in",str(total)])

print(tabulate(timetable, tablefmt="fancy_grid"))
print(tabulate(result_table, result_table_header, tablefmt="fancy_grid"))
