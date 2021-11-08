'''
Create a Python script that connects to a Cisco Router using SSH and Paramiko. The script should execute the show users command in order to display the logged-in users.

Print out the output of the command.
'''

#!/usr/bin/env python

import paramiko, getpass, time, json
from datetime import date

with open('hosts.json', 'r') as f:
    devices = json.load(f)

with open('./commands/show_users.txt', 'r') as f:
    commands = f.readlines()

username = input('Username: ')
password = getpass.getpass('Password: ')
today = date.today()

max_buffer = 10000

def clear_buffer(connection):
    if connection.recv_ready():
        connection.recv(max_buffer)

#Starts the loop to iterate over devices
for device in devices.keys():
    outputFileName = device + f'_output_{today}.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {devices[device]["ip"]}')
    connection.connect(devices[device]['ip'], username=username, password=password, look_for_keys=False, allow_agent=False)
    new_connection = connection.invoke_shell()
    # output = clear_buffer(new_connection)
    time.sleep(2)
    new_connection.send('terminal length 0\n')
    output = clear_buffer(new_connection)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            new_connection.send(f'{command}\n')
            time.sleep(2)
            output = new_connection.recv(max_buffer)
            output.decode('utf-8')
            print(output)
            f.write(output)
    
    print(f'Closing connection to {devices[device]["ip"]}')
    new_connection.close()