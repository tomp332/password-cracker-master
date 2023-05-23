# Master Password Cracker Server

# Description

<p> Password brute forcer that uses lightweight minion server in order to preform a brute force on a set of MD5 passwords.</p>

**[Master Server](https://github.com/tomp332/password-cracker-master)** - the main server that manages all minion connections for brute forcing</p>
**[Minion Server](https://github.com/tomp332/password-cracker-minion)** - the leightweight servers used for cracking</p>

# Tutorial

## Master Server

1. Run the following script which generates 05xxxxxxxx phone number dirlist (can also be found in the directory example_data inside the repo):
```python
prefix = "05"
numbers = []

for i in range(100000000):
    number = prefix + str(i).zfill(8)
    numbers.append(number)

# Write the generated phone numbers to a file
with open("./phone_numbers.txt", "w") as file:
    for number in numbers:
        file.write(number + "\n")
```

```
python3 ./generate_numbers.py
```
*Notice: the script will reproduce a phone_numbers.txt file in the current directory*

2. Copy the following docker-compose file and save it in the current working directory:

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
      - ./phone_numbers.txt:/data/dictionary.txt

volumes:
  cracker-db:

```

3. Run the following docker-compose file that you have just copied

```bash
docker-compose up -d
```
4. Your up and running, this will load the dockerized services for the master server
  - On startup, the master server loads the dirlist a process which might take a while on the first run.
  - You can start interaction with the server, but no brute force process will start until the dirlist has been loaded properly.

## Minion Server

Like explained ealier, a **minion server** is a leightweight service that connects to the master server,
and obtains tasks for brute forcing.</p>
All tasks are managed through the **master server** and are uploaded via API, which will be explained in the next section.

### Run

*Make sure the master server is up and running for this, otherwise the minion will not start.*


```
docker run -p <LOCAL_EXPOSED_PORT>:5000 --env MASTER_HOSTNAME=<MASTER_SERVER_IP> ghcr.io/tomp332/password-cracker/minion
```
A valid example for launching 3 minion servers:

```
docker run -p 5001:5000 --env MASTER_HOSTNAME=192.168.1.160 ghcr.io/tomp332/password-cracker/minion
docker run -p 5002:5000 --env MASTER_HOSTNAME=192.168.1.160 ghcr.io/tomp332/password-cracker/minion
docker run -p 5003:5000 --env MASTER_HOSTNAME=192.168.1.160 ghcr.io/tomp332/password-cracker/minion
```

*Notice: localhost will probably not work since the docker-compose is running a different adapter*


## Begin Brute Force

1. Using the OpenAPI management page: ( available at http://localhost:5000/docs) 

<p> Upload a valid file containing a list of md5 hashes to be cracked ( an example is in the repo under example_data directory).</p>

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/11e570e8-a11f-4581-8595-ef6ce68ffaac)

2. Save the *crack_task_id* returned from the request, if everything went well, you will need that ID for keeping track of your passwords.

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/34bb52bb-3f4d-4511-a83c-d85214915616)

3. At this point, you can see that your minion servers have received tasks for brute forcing the passwords that have been uploaded.

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/60e1f278-5505-40de-9d9f-2cc4703085f2)

4. You can check the status of all your uploaded hashes in the current file using the api:

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/b43d0ca1-37c3-46cb-aa19-c74e2d707eee)

