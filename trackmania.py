#!/bin/python3

"""
Run ./trackmania.py <action> <ports>

<action> can be 'down', 'up', 'status'.
<ports> is numbers concatenated referencing the server to affect. 'status' does not required any port.

ex : './trackmania.py up 12' -> starts cup1 and cup2
"""

import subprocess
import shlex
import sys
import os


def upServer(id: str) -> None:
    """
    It runs a docker-compose command in a specific directory

    :param id: the id of the server
    """
    name = "tm_server_" + id
    path = "./compose/cup" + id + "/"
    if (id == "t") :
        name = "tm_server_time"
        path = "./compose/time"
    p = subprocess.Popen(["docker", "compose", "-p", name,
                          "-f", "docker-compose.yaml", "up", "-d"], cwd=path)
    print(p.communicate())


def downServer(id: str) -> None:
    """
    It takes an id as a parameter, and then it runs a docker-compose command to bring down the server
    with that id

    :param id: the id of the server
    """
    name = "tm_server_" + id
    path = "./compose/cup" + id + "/"
    if (id == "t") :
        name = "tm_server_time"
        path = "./compose/time/"
    p = subprocess.Popen(["docker", "compose", "-p", name,
                          "-f", "docker-compose.yaml", "down", "-v"], cwd=path)
    print(p.communicate())

def restartServer(id: str) -> None:
    """
    It takes an id as a parameter, and then restarts the server with that id
    :param id: the id of the server
    """
    downServer(id)
    upServer(id)


def status() -> None:
    """
    Display the status of the Trackmania servers, showing the ID, Uptime, and Name of the running dockers.
    """
    p = subprocess.Popen(
        shlex.split("docker ps --format \"table {{.ID}}\t{{.Status}}\t{{.Names}}\""))
    print(p.communicate())


def main(args: list[str]) -> None:
    """
    It starts or closes the servers in the list of servers passed as an argument.
    If no server is passed, it starts or closes all the servers.

    :param args: the list of arguments passed to the script
    """
    if (args[1] == "status"):
        status()
        exit(0)
    try:
        listServer: list = args[2:]
        if (len(listServer) == 0):
            for cup in os.listdir("compose"):
                if "cup" in cup:
                    listServer.append(cup.replace("cup", ""))
        if (args[1] == "up"):
            for i in range(len(listServer)):
                upServer(listServer[i])
        elif (args[1] == "down"):
            for i in range(len(listServer)):
                downServer(listServer[i])
        elif (args[1] == "restart"):
            for i in range(len(listServer)):
                restartServer(listServer[i])
        else:
            print("[ERROR] Wrong argument : '{0}' is not regonized as a valid argument.".format(
                args[1]))
            exit(1)
    except IndexError:
        sys.stderr.write("[ERROR] Wrong number of arguments : '{0}' requires a list of int separated by commas.\n".format(
            args[1]))
        exit(1)
    except FileNotFoundError as e:
        sys.stderr.write(str(e.args))
        sys.stderr.write(
            "[ERROR] Index out of bound : specified server does not exist, no directory found with that index.\n")
        exit(1)


if __name__ == "__main__":
    main(sys.argv)
