# Password Cracker Project
<br>
<br>

## Description

<p> Password brute forcer that uses lightweight minion server in order to preform a brute force on a set of MD5 passwords.</p>

**[Master Server](https://github.com/tomp332/password-cracker-master)** - the main server that manages all minion connections for brute forcing</p>
**[Minion Server](https://github.com/tomp332/password-cracker-minion)** - the leightweight servers used for cracking</p>
<br>
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

<p>A valid dirlist file would be in the following format:</p>

```
0500000000
0500000001
0500000002
0500000003
0500000004
```

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
  - On startup, the master server loads the dirlist, a process which might take a while on the first run.
  - You can start interaction with the server, but no brute force process will start until the dirlist has been loaded properly.

## Minion Server

Like explained ealier, a **minion server** is a leightweight service that connects to the master server,
and obtains tasks for brute forcing.</p>
All tasks are managed through the **master server** and are uploaded via API, which will be explained in the next section.

### Process

<p> Each minion task that is received from the master server, includes a range of passwords to try and crack with, </p> 
<p> along with the hashed password that needs to be cracked. </p>

<p> As soon as the minion finishes or was able to crack a certain password, </p>
<p> it notifies the master server leading to the next password that needs to be cracked or to finish the process </p>


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

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/23fdc217-f9e9-430c-b397-1a039d6e62d2)


*An example of a valid hash list file:*

```bash
b2834d97374c65c9b8e0e10bb2e5afa0
437783d8e13e9d668a89c1654cbb904a
e9d7645ed586bb8973dee3df02318741
```

2. Save the *crack_task_id* returned from the request, if everything went well, you will need that ID for keeping track of your passwords.

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/83af6a51-96b0-4db9-b639-5c8c4059531f)

3. At this point, you can see that your minion servers have received tasks for brute forcing the passwords that have been uploaded.

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/526a36ae-fb2e-4ecc-8d87-e055f1ce6533)

4. You can check the status of all your uploaded hashes in the current file using the api:

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/412741bb-78a1-441b-b9a8-23c02f331c7e)

5. An example of all hashes that are decrypted:

![image](https://github.com/tomp332/password-cracker-master/assets/47506972/ba126dea-b170-4563-9f62-7dc2be677c4d)

