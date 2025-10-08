# trackmania-server

A pre-configured Trackmania 2020 server for the InsaLan tournament.
It uses an updated version of the [trackmania-server docker image](https://hub.docker.com/r/harha/trackmania-server-docker), with scripts allowing to configure and manage multiple server instances.

## Installation

Clone this repository on your machine :

```bash
git clone https://github.com/InsaLan/trackmania-server.git
```

Install python script dependencies :

```bash
cd trackmania-server
pip install -r requirements.txt

# As most linux distributions directly manage python modules, you may need to create a venv to use pip, or install the modules with your distro's package manager.
```

Use the `deploy.py` to create the cups :

```bash
./deploy.py <number_of_cups>

# Where number_of_cups is a number between 1 and 9.
# You can modify the script to override the 9 limit, but it could lead to unexpected behavior, as the port range allocated to Trackmania servers is 2351-2359.
```

> Don't forget to [configure the cups](#server-configuration), a server cant' start without a config file.

## Server management

Trackmania servers can be started / stopped / restarted using the `trackmania.py` script :

```bash
./trackmania.py <up|down|restart> <server>

# Where <server> is the list of the instances' number separated by spaces
# If no list is passed, the script will affect all the servers

./trackmania.py status

# Prints the status of all the instances
```

## Server configuration

Server configurations are stored in `config.json` (check [Official Game Modes Settings](https://wiki.trackmania.io/en/dedicated-server/Usage/OfficialGameModesSettings) for more informations on the available options, and use the default config as an example).
Configurations can be applied to all the servers with the `config.py` script :

```bash
./config.py

# Just follow the instructions, easy af
```
