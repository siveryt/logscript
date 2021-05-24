#!/usr/bin/python3
import sys
import os
import json
print("██       ██████   ██████  ██ ███    ██ \n██      ██    ██ ██       ██ ████   ██ \n██      ██    ██ ██   ███ ██ ██ ██  ██ \n██      ██    ██ ██    ██ ██ ██  ██ ██ \n███████  ██████   ██████  ██ ██   ████")

action = True
chooser = True
f = open('.con.json',)
connections = json.load(f)
f.close()


def selectAction():
    global action
    print("\nSelect what you want: ")
    if(len(connections) != 0):
        print("1) Login via SSH")
        print("2) Open SFTP Session")
    print("3) Add Remote")
    if(len(connections) != 0):
        print("4) Remove Remote")
    action = input("Select a option: ")


def printRemotes():
    print("All remotes:")
    for con in connections:
        print("   "+con)


def ssh(remote):
    remote = connections[remote]
    if(remote["keyfile"] != ""):
        addendum = " -i "+remote["keyfile"]
    else:
        addendum = ""
    con = open(".connect.sh", "w")
    con.write("ssh %s@%s -p %s" %
              (remote["user"], remote["hostname"], remote["port"])+addendum)
    con.close()


def sftp(remote):
    remote = connections[remote]
    if(remote["keyfile"] != ""):
        addendum = " -i "+remote["keyfile"]
    else:
        addendum = ""
    con = open(".connect.sh", "w")
    con.write("sftp %s@%s -p %s" %
              (remote["user"], remote["hostname"], remote["port"])+addendum)
    con.close()


def add():
    print("Adding new remote")
    name = input("Name: ")
    host = input("Hostname: ")
    port = input("Port: ")
    user = input("User: ")
    key = input("Keyfile (Leave clear for none): ")
    connections[name] = {"name": name, "port": port,
                         "hostname": host, "user": user, "keyfile": key}
    with open('.con.json', 'w') as connections_dumped:
        json.dump(connections, connections_dumped)
    print("Written new remote to database! Rerun the script, to use it.")


def remove():
    print("Removing remote")
    chooser = True
    while chooser:
        printRemotes()
        remote = input("Remote to remove: ")
        if remote in connections:
            chooser = False
            connections.pop(remote)
            with open('.con.json', 'w') as connections_dumped:
                json.dump(connections, connections_dumped)
            print("Removed the remote from the database! Rerun the script.")
        else:
            print("Please enter a remote that exists!")
            print("------------")


if __name__ == '__main__':
    try:
        while(action):

            selectAction()

            if(action.startswith("1")):
                action = False
                while chooser:
                    printRemotes()
                    remote = input("Remote: ")
                    if remote in connections:
                        chooser = False
                        ssh(remote)
                    else:
                        print("Please enter a remote that exists!")
                        print("------------")

            elif(action.startswith("2")):
                action = False
                action = False
                while chooser:
                    printRemotes()
                    remote = input("Remote: ")
                    if remote in connections:
                        chooser = False
                        sftp(remote)
                    else:
                        print("Please enter a remote that exists!")
                        print("------------")
            elif(action.startswith("3")):
                action = False
                add()
            elif(action.startswith("4")):
                action = False
                remove()
            else:
                print("----------\nThis didn't work! Try again")
                action = True
    except KeyboardInterrupt:
        print('\nBye!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
