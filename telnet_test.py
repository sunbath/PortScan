
import socket
import subprocess
import sys
import csv

from datetime import datetime,timezone
from tabulate import tabulate

def func_clear_screen():
    # Clear the screen
    subprocess.call('clear', shell=True)

def func_convert_utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def func_display_local_time(utc_dt):
    return func_convert_utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z')

def func_generate_filename(filename, filetype):
    #generate filename based on the given prefix and the timestamp
    now = datetime.now()
    now = now.strftime('%Y%m%d_%H%M%S%Z')

    if filetype == "text":
        filename = filename + "_" + now + ".txt"
    elif filetype == "csv":
        filename = filename + "_" + now + ".csv"
    return filename

def func_list_process(original_list):
    #function to process a list to remove duplicates and expands port range.
    #return the processed list
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
    #print(temp_list)
    return temp_list

def func_telnet_test_cli(Destination_IP, Destination_Port):
    
    #Color Codes for Text Format
    W = '\033[0m'   # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    C = '\033[36m'  # cyan
    
    result_list = []
    
    remoteServerIP = socket.gethostbyname(Destination_IP)
    try:
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((remoteServerIP, Destination_Port))
            result_list.append([" ", G+str(Destination_Port)+W, G+"Telnet Succeeded"+W, G+str(func_display_local_time(datetime.utcnow()))+W])
            return result_list
            sock.close()
        except:
            result_list.append(
                [" ", R+str(Destination_Port)+W, R+"Telnet Failed"+W, R+str(func_display_local_time(datetime.utcnow()))+W])
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

def func_telnet_test_file(Destination_IP, Destination_Port):

    result_list = []

    remoteServerIP = socket.gethostbyname(Destination_IP)
    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((remoteServerIP, Destination_Port))
            result_list.append([remoteServerIP, Destination_Port, "Telnet Succeeded", func_display_local_time(datetime.utcnow())])
            return result_list
            sock.close()
        except:
            result_list.append([remoteServerIP, Destination_Port, "Telnet Failed", func_display_local_time(datetime.utcnow())])
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

def func_print_table_to_cli(input_table, input_table_header, format):
    print(tabulate(input_table, input_table_header, tablefmt=format))

def func_print_table_to_textfile(filename, time_table, result_table_header, result_table, format):
    f = open(filename, "w")
    f.write(tabulate(time_table, "", tablefmt=format))
    f.write("\n")
    f.write(tabulate(result_table, result_table_header, tablefmt=format))
    f.close()

def func_print_table_to_csvfile(filename, time_table, result_table_header, result_table):
    with open(filename, "w", newline="") as f:
        cw = csv.writer(f,delimiter=",")
        cw.writerows("\n")
        cw.writerows(r + [""] for r in time_table)
        cw.writerows("\n")
        cw.writerow(result_table_header)
        cw.writerows(r + [""] for r in result_table)

def func_export_to_cli(Test_List):
    result_table_header = ["Destination IP", "Destination TCP Port","Telnet Test Result", "Test Time"]
    result_table = []

    # Start Time
    starttime = datetime.utcnow()

    for server in Test_List:
        server["Destination TCP Port"] = func_list_process(server["Destination TCP Port"])
        result_table.append([server["Destination IP"], " ", " ", " "])
        for port in server["Destination TCP Port"]:
            result_table.extend(func_telnet_test_cli(server["Destination IP"], port))
        result_table.append(["---", "---", "---", "---"])

    # End Time
    # Calculates the difference of time, to see how long it took to run the script
    endtime = datetime.utcnow()
    total = endtime - starttime

    time_table = []
    time_table.append(["Source IP:", socket.gethostbyname(socket.gethostname())])
    time_table.append(["Testing Start Time", func_display_local_time(starttime)])
    time_table.append(["Testing End Time", func_display_local_time(endtime)])
    time_table.append(["Completed in",str(total)])

    func_print_table_to_cli(time_table, "", "fancy_grid")
    func_print_table_to_cli(result_table, result_table_header, "fancy_grid")

def func_export_to_textfile(Test_List, filename):
    result_table_header = ["Destination IP", "Destination TCP Port", "Telnet Test Result", "Test Time"]
    result_table = []

    # Start Time
    starttime = datetime.utcnow()

    for server in Test_List:
        server["Destination TCP Port"] = func_list_process(server["Destination TCP Port"])
        for port in server["Destination TCP Port"]:
            result_table.extend(func_telnet_test_file(server["Destination IP"], port))
        result_table.append(["---", "---", "---", "---"])

    # End Time
    # Calculates the difference of time, to see how long it took to run the script
    endtime = datetime.utcnow()
    total = endtime - starttime

    time_table = []
    time_table.append(["Source IP:", socket.gethostbyname(socket.gethostname())])
    time_table.append(["Testing Start Time", func_display_local_time(starttime)])
    time_table.append(["Testing End Time", func_display_local_time(endtime)])
    time_table.append(["Completed in", str(total)])

    func_print_table_to_textfile(filename, time_table, result_table_header, result_table, "grid")

def func_export_to_csvfile(Test_List, filename):
    result_table_header = ["Destination IP", "Destination TCP Port", "Telnet Test Result", "Test Time"]
    result_table = []
    # Start Time
    starttime = datetime.utcnow()

    for server in Test_List:
        server["Destination TCP Port"] = func_list_process(server["Destination TCP Port"])
        for port in server["Destination TCP Port"]:
            result_table.extend(func_telnet_test_file(server["Destination IP"], port))

    # End Time
    # Calculates the difference of time, to see how long it took to run the script
    endtime = datetime.utcnow()
    total = endtime - starttime

    time_table = []
    time_table.append(["Source IP:", socket.gethostbyname(socket.gethostname())])
    time_table.append(["Testing Start Time", func_display_local_time(starttime)])
    time_table.append(["Testing End Time", func_display_local_time(endtime)])
    time_table.append(["Completed in", str(total)])

    func_print_table_to_csvfile(filename, time_table, result_table_header, result_table)

def main():
    
    func_clear_screen()

    Test_List = [
        {"Destination IP": "192.168.11.1", "Destination TCP Port": ["20:20","138","21:23","139","80","443"]},
        {"Destination IP": "192.168.11.21", "Destination TCP Port": ["19-19","20-24","21:23","139","139"]}
    ]
    
    func_export_to_cli(Test_List)
    #func_export_to_textfile(Test_List,func_generate_filename("txtfilename","text"))
    #func_export_to_csvfile(Test_List, func_generate_filename("csvfilename","csv"))

if __name__ == '__main__':
    main()
