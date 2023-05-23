# Master Password Cracker Server

## Description

<p> Password brute forcer that uses lightweight minion server in order to preform a brute force on a set of MD5 passwords.</p>

**[Master Server](https://github.com/tomp332/password-cracker-master)** - the main server that manages all minion connections for brute forcing</p>
**[Minion Server](https://github.com/tomp332/password-cracker-minion)** - the leightweight servers used for cracking</p>

# Tutorial

## Master Server

Master server compose file:
- MongoDB
- MongoExpress for some UI management
- Master crack server

These services are all required in order to run the master server properly.
Copy the following to a docker-compose.yml file:

```yml
version: '3.9'

services:

  db-ui:
    image: mongo-express
    restart: always
    ports:
      - 8081:8081
    environment:
      - ME_CONFIG_MONGODB_ADMINUSERNAME=root
      - ME_CONFIG_MONGODB_ADMINPASSWORD=root
      - ME_CONFIG_MONGODB_URL=mongodb://root:root@cracker-db:27017/
    depends_on:
      - cracker-db

  cracker-db:
    image: mongo
    restart: unless-stopped
    environment:
      - MONGO_INITDB_ROOT_USERNAME=root
      - MONGO_INITDB_ROOT_PASSWORD=root
      - MONGO_INITDB_DATABASE=password_cracker
    volumes:
      - cracker-db:/data/db

  cracker-master:
    image: ghcr.io/tomp332/password-cracker/master
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./example_data/phone_numbers.txt:/data/dictionary.txt

volumes:
  cracker-db:

```
# Run

Using the docker-compose file from the previous section run:

```bash
docker-compose up -d
```
This will load the dockerized services for the master server

## Minion Server

Like explained ealier, a **minion server** is a leightweight service that connects to the master server,
and obtains tasks for brute forcing.</p>
All tasks are managed through the **master server** and are uploaded via API, which will be explained in the next section.

# Run

*Make sure the master server is up and running for this, otherwise the minion will not start.*


```
docker run --env MASTER_HOSTNAME=<MASTER_SERVER_IP> ghcr.io/tomp332/password-cracker/minion
```
A valid example:

```
docker run --env MASTER_HOSTNAME=192.168.1.160 ghcr.io/tomp332/password-cracker/minion
```
*Notice: localhost will probably not work since the docker-compose is running a different adapter*


## API



## Running

