import os, subprocess, time, json
from subprocess import Popen, PIPE

def com_connection(debug_type):
    file = open("./configuration/settings.json", "r")
    settings = {}
    tmp = file.read()
    settings = json.loads(tmp)
    if debug_type == "com":
        # kd -k com:port=\\.\pipe\serialpipe,baud=115200,pipe,reconnect
        subprocess_command = ["kd", "-k", "com:port="+str(settings["COM"]["PIPE"])+",baud="+str(settings["COM"]["BAUDRATE"])+",pipe,reconnect"]
        p = Popen(subprocess_command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, env=os.environ)
        stdout_value = p.communicate()[0]
        print(stdout_value.decode("utf-8"))
    elif debug_type == "com":
        subprocess_command = ["kd", "-K", "net:port="+str(settings["NET"]["PORT"])+",key="+str(settings["NET"]["KEY"])+",name="+str(settings["NET"]["NAME"])]
        p = Popen(subprocess_command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, env=os.environ)
        stdout_value = p.communicate()[0]
        print(stdout_value.decode("utf-8"))

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

def main():
    choice = ""
    while(choice != "EXIT"):
        print("\r\n######################## MENU ########################")
        print("1. DEBUG USING SERIAL COM PORT.")
        print("2. DEBUG SUING NET SETTINGS.")
        print("3. SHOW SETTINGS")
        print("TYPE STOP THIS SCRIPT TYPE 'EXIT' AND PRESS ENTER")
        print("######################################################\r\n")
        choice = input("ENTER YOUR CHOICE : ")
        if choice == "EXIT":
            print("BYE !!")
            continue
        elif int(choice) == 1:
            com_connection("com")
        elif int(choice) == 2:
            com_connection("serial")
        elif int(choice) == 3:
            read_settings()
        else:
            print("INVALID SELECTION !!")

if __name__ == "__main__":
    main()
