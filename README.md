# trackmania-server

A pre-configured Trackmania 2020 server for the InsaLan tournament.
It uses the [trackmania-server docker image](#trackmania-server-docker), with scipts allowing to configure and manage multiple server instances.

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

Server configurations are stored in `config.json` (check [Official Game Modes Settings](https://wiki.trackmania.io/en/dedicated-server/Usage/OfficialGameModesSettings) for more informations on the available options).
Configurations can be applied to all the servers with the `config.py` script :

```bash
./config.py

# Just follow the instructions, easy af
```

## trackmania-server-docker

Docker image(s) for running a trackmania 2020 dedicated server + pyplanet easily.

The project is divided into 2 images, separated by tags.

* :server
  * This tag is the latest version of the trackmania server image
  * Built from folder ./build-server
* :pyplanet
  * This tag is the latest version of the pyplanet server controller image
  * Built from folder ./build-pyplanet

### compose

The compose directory contains example compose & config files for actually starting & running container(s) with the built image(s).

You're supposed to edit it to your likings if you want to run your own server. Put your maps into the `compose/maps` folder. Download from trackmania exchange.

Example compose command to deploy the stack. The `p` argument specifies project name that you can change to easily deploy multiple server stacks on same machine.

```bash
docker-compose -p tm_server -f docker-compose.yaml up -d
```

You can also easily deploy the stack remotely to a target dedicated server (that has docker running in it)

```bash
DOCKER_HOST="ssh://server@remote.addr" docker-compose -p tm_server -f docker-compose.yaml up -d
```

#### Environment variables

##### SERVER_TITLE

The TitleID for the game the server should be running. By default set to Trackmania 2020. Possible values are:

* Trackmania
* SMStorm
* TMCanyon
* TMStadium
* TMValley
* TMLagoon

##### SERVER_NAME

The visible name for the server.

#### PyPlanet configuration

PyPlanet controller can be configured via `compose/pyplanet/settings/*.yaml` files. For documentation, go to: https://pypla.net/en/latest/intro/configuration.html
