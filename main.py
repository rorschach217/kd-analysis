import sys, subprocess, time, json, threading, pyautogui, os
from subprocess import Popen, PIPE
from datetime import datetime

run_commands=False
t1=None
t2=None
file_name=""
path=""
debug_data = dict()

def read_settings():
    file = open("./configuration/settings.json", "r")
    settings = {}
    tmp = file.read()
    settings = json.loads(tmp)
    print("CURRENT CONFIGURATION")
    for key in settings:
        if isinstance(settings[key], dict):
            print("\r\n" + key)
            for sub_key in settings[key]:
                print(sub_key + " = " + str(settings[key][sub_key]))
        else:
            print("\r\n" + key + " = " + settings[key])
    print("\r\nUPDATE configuration/settings.json TO UPDATE SETTINGS !!")
    file.close()

# def kill_threads():
#     global t1, t2
#     t1.join()
#     t2.join()

def gather_data():
    global path, file_name, debug_data, run_commands
    existing_output = open("./report/"+file_name+".txt", "r")
    ip_count = 3
    stack_count = 2
    for line in existing_output:
        ip_count = ip_count + 1
        stack_count = stack_count + 1
        if line.find("BUGCHECK_P1") != -1:
            tmp = line.split(" ")
            if tmp[1]:
                debug_data["BUGCHECK_P1"] = tmp[1].strip() if len(tmp[1]) > 2 else None
        elif line.find("BUGCHECK_P2") != -1:
            tmp = line.split(" ")
            if tmp[1]:
                debug_data["BUGCHECK_P2"] = tmp[1].strip() if len(tmp[1]) > 2 else None
        elif line.find("BUGCHECK_P3") != -1:
            tmp = line.split(" ")
            if tmp[1]:
                debug_data["BUGCHECK_P3"] = tmp[1].strip() if len(tmp[1]) > 2 else None
        elif line.find("BUGCHECK_P4") != -1:
            tmp = line.split(" ")
            if tmp[1]:
                debug_data["BUGCHECK_P4"] = tmp[1].strip() if len(tmp[1]) > 2 else None
        elif line.find("FAULTING_MODULE") != -1:
            tmp = line.split(" ")
            if tmp[1]:
                debug_data["FAULTING_MODULE"] = tmp[1].strip() if len(tmp[1]) > 2 else None
        elif line.find("FAULTING_IP") != -1:
            ip_count = 0
        elif ip_count == 2:
            tmp = line.split(" ")
            if tmp[0]:
                debug_data["FAULTING_IP"] = tmp[0].strip() if len(tmp[0]) > 2 else None
        elif line.find("STACK_TEXT") != -1:
            stack_count = 0
        elif stack_count == 1 and line.strip() != "":
            stack_count = 0
            tmp = line.split(" ")
            if tmp[0]:
                if "STACK_TEXT" not in debug_data:
                    debug_data["STACK_TEXT"] = [tmp[0].strip()] if len(tmp[0]) > 2 else []
                else:
                    if len(tmp[0]) > 2:
                        debug_data["STACK_TEXT"].append(tmp[0].strip())
    existing_output.close()
    run_commands=False
    t1 = threading.Thread(target=dump_analysis, args=(path,)).start()
    generate_full_report()


def dump_analysis(path):
    global run_commands, file_name
    now = datetime.now()
    file_name = file_name if len(file_name) > 0 else str(now.strftime("%d_%m_%Y_%H_%M"))
    file = open("./configuration/settings.json", "r")
    settings = {}
    tmp = file.read()
    settings = json.loads(tmp)
    subprocess_command = ["kd", "-y", str(settings["SYMBOLPATH"]), "-z", str(path), "-b", "-logo", "./report/"+file_name+".txt"]
    subprocess.Popen(subprocess_command,shell=True,close_fds=True)
    time.sleep(10) #wait for kd to load
    run_commands=True

def generate_full_report():
    global run_commands, file_name, debug_data
    while not run_commands:
        time.sleep(1)
    pyautogui.write("!analyze -v", interval=0.05)
    pyautogui.press("enter")
    time.sleep(2)
    if debug_data["FAULTING_IP"]:
        pyautogui.write("dd " + debug_data["FAULTING_IP"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("u " + debug_data["FAULTING_IP"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
    if debug_data["BUGCHECK_P1"]:
        pyautogui.write("dd " + debug_data["BUGCHECK_P1"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("u " + debug_data["BUGCHECK_P1"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
    if debug_data["BUGCHECK_P2"]:
        pyautogui.write("dd " + debug_data["BUGCHECK_P2"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("u " + debug_data["BUGCHECK_P2"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
    if debug_data["BUGCHECK_P3"]:
        pyautogui.write("dd " + debug_data["BUGCHECK_P3"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("u " + debug_data["BUGCHECK_P3"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
    if debug_data["BUGCHECK_P4"]:
        pyautogui.write("dd " + debug_data["BUGCHECK_P4"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("u " + debug_data["BUGCHECK_P4"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
    if debug_data["FAULTING_MODULE"]:
        pyautogui.write("dd " + debug_data["FAULTING_MODULE"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("u " + debug_data["FAULTING_MODULE"], interval=0.05)
        pyautogui.press("enter")
        time.sleep(1)
    if len(debug_data["STACK_TEXT"]) > 0:
        for item in debug_data["STACK_TEXT"]:
            pyautogui.write("dd " + item, interval=0.05)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.write("u " + item, interval=0.05)
            pyautogui.press("enter")
            time.sleep(1)
    pyautogui.write("!for_each_frame .frame /r @$Frame", interval=0.05)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write("lm", interval=0.05)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write("!process 0 0", interval=0.05)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write("qd", interval=0.05)
    pyautogui.press("enter")
    time.sleep(3)
    os.system('cls||clear')
    print("YOU CAN FIND YOUR REPORT IN FILE report/"+file_name+".txt")
    print("BYE !!!")
    exit()

def get_basic_data_report():
    global run_commands
    while not run_commands:
        time.sleep(1)
    pyautogui.write("!analyze -v", interval=0.05)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write("qd", interval=0.05)
    pyautogui.press("enter")
    time.sleep(3)
    os.system('cls||clear')
    print("PLEASE  WAIT WHILE WE GATHER DATA FOR ANALYSIS !!!")
    gather_data()

def main():
    global run_commands, path, t1, t2
    while True:
        print("\r\n######################## MENU ########################")
        print("1. DUMP ANALYSIS")
        print("2. SHOW SETTINGS")
        print("3. EXIT")
        print("TYPE STOP THIS SCRIPT TYPE 'EXIT' AND PRESS ENTER")
        print("######################################################\r\n")
        choice = input("ENTER YOUR CHOICE : ")
        if isinstance(choice, str) and int(choice) == 3:
            print("BYE !!")
            exit()
            pass
        elif isinstance(choice, str) and int(choice) == 1:
            print("\r\n####################################################################\r\n")
            print("WARNING !!!")
            print("THIS WHOLE PROCESS TAKES ABOUT 7-8 MINUTES !!!")
            print("PLEASE DO NOT LEAVE THIS WINDOW !!!")
            print("\r\n####################################################################\r\n")
            time.sleep(10)
            path = input("ENTER FULL PATH OF DUMP : ")
            run_commands=False
            t1 = threading.Thread(target=dump_analysis, args=(path,)).start()
            get_basic_data_report()
        elif isinstance(choice, str) and int(choice) == 2:
            read_settings()
        else:
            print("INVALID SELECTION !!")

if __name__ == "__main__":
    main()
