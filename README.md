
# TXT Puller

A client-server application used for listing, removing and updating files in a server using a cli client.

## Tech used
- Python
- Flask web framework
- Docker
- Click

#### Features

- add (Add multiple files to the server) accepts multiple values
- ls (List all files in the server) accepts no value
- rm (Remove a files in the server)  accepts single value
- update (Updare a file in the server) accepts single value
- wc (Count number of words in all the files in the server) accepts no value
- freq-words (Count all most or least n frequent words in all the files combined) accepts no value

#### Steps to run server as a standalone docker container

1. Clone the repo
   ```sh
   git clone https://github.com/Krishnanunni333/txt_puller.git
   ```
2. CD into the txt_puller/server directory
   ```sh
   cd txt_puller/server
   ```
3. Execute the setup_server.sh script
   ```sh
   sh setup_server.sh
   ```
   *Change permission by executing chmod +xsetup_server.sh if execution error comes up*

4. Now run the created image as a container as below.
   ```sh
   docker run -it -d -p 5000:5000 krishnanunni333/store-full-server:v0.1 /bin/bash
   ```
   *krishnanunni333/store-full-server:v0.1 is the image name and tag. You can change image name and tag if u want in the setup_server.sh file*


#### Steps to run the server inside a Kubernetes cluster as a Pod

1. CD into the txt_puller/server directory
   ```sh
   cd txt_puller/server
   ```
2. Execute the below command to deploy the pod.
   ```sh
   kubectl apply -f server-deploy.yaml
   ```
3. Execute the below command to deploy the services.
   ```sh
   kubectl apply -f server-service.yaml
   ```
4. Execute the below command to get hostname/external-ip and port
   ```sh
   kubectl get svc file-server-service
   ```
5. Use the hostname/ip and port together for testing and other operations.
   eg : http://localhost:5000 or http://127.0.0.1:5000 or http:< external-ip >:5000


#### Steps to create an executable client

To get valid response, Please run the server

1. CD into the txt_puller/client directory
   ```sh
   cd txt_puller/client
   ```
2. Set the environment variable equal to the location of your properties file.
   ```sh
   export PROPERTIES_PATH=$(pwd) # pwd can be replaced with path to the directory containing store.properties file
   ```
   Print it to see its value if you want
   ```sh
   echo $PROPERTIES_PATH
   ```
   If you export like this, then the value will only be available in that particular single terminal session.
   If you are a linux user, its better to store the value of PROPERTIES_PATH in the " ~/.bashrc " or " /etc/profile " for system wide use.

3. Install Pyinstaller package to package client as a single executable.
   ```sh
   pip install pyinstaller
   ```
4. Execute the below command to make an executable using pyinstaller
   ```sh
   pyinstaller --onefile store.py
   ```
5. CD into the dist folder and copy the store app and paste it wherever you want to execute the commands.
   ```sh
   cd dist
   cp store ~ # copying to home for now
   cd #navigate to home
   ```
6. After copying you can delete the all the folders and files that were created when building the binary.

7. You can use the command as below:
   ```sh
   ./store ls
   ```
   *Please note that the add and update commands needs the files to be present in the same location where the binary is located*


#### Steps to test the whole application inside a container

1. Pull the docker image from DockerHub
   ```sh
   docker pull krishnanunni333/store-full-app:v0.1
   ```
2. Run the image as a container with port mapping and in detached mode
   ```sh
   docker run -it -d -p 5000:5000 krishnanunni333/store-full-app:v0.1 /bin/bash
   ```
3. Verify whether the container is running fine
   ```sh
   docker ps -a
   ```
4. Get inside the running container
   ```sh
   docker exec -it <container name> /bin/bash
   ```
5. Run the setup.sh file.
   ```sh
   sh setup.sh
   ```
6. CD into the server directory
   ```sh
   cd server
   ```
7. Run the server 
   ```sh
   python app.py
   ```
8. Open a second terminal and do step 4 
9. CD into client directory
   ```sh
   cd client
   ```
10. Just to make sure that server is running fine execute the following
   ```sh
   wget http://127.0.0.1:5000 
   ```
   This will create an index.html file with 'Hello World!' as its content. Remove that file
   ```sh
   rm index.html 
   ```
11. Run the automated tests using the following command in the current directory
   - pytest
   
   The automated test will create new txt files with content in it and performs, add, rm, ls, wc commands and checks their output. It only contains some basic cases and the test cases can be made much bigger and broader to cover the whole application working.
   
   *The application has all the functionalities as per the document shared but automated test coverage is not there for all the functionalities*
   
#### Usage of the cli tool using python command
**add**
This command will upload all the files to the server if the file is not present in the server. If the file is present, that file is ignored. If a file that has same content as the local file but has a different name in the server, then only copying at the server level will take place with localname as the name of new file.
```sh
   python store.py add file 1 file 2 ... file n 
   ```
**ls**
This command will list all the files present in the server.
```sh
   python store.py ls 
   ```
**rm**
This command will remove a file in the server if its present.
```sh
   python store.py rm file
   ```
**update**
This command will upload the local file if the content at server is different and creates a new file if the file is not present. If a file that has same content as the local file but has a different name in the server, then only copying at the server level will take place with localname as the name of new file.
```sh
   python store.py update file
   ```
**wc**
This command will return the number of words in all the files in the server combined .
```sh
   python store.py wc
   ```
**freq-words**
This command will return the most or least frequently repeated words upto a limit of n .
dsc - most frequent
asc - least frequent
```sh
   python store.py freq-words -n <num> --order <dsc or asc>
   ```
   or
   ```sh
   python store.py freq-words -limit <num> --order <dsc or asc>
   ```
#### Assumptions and Stratergies
- The file is send to the server as line-by-line and not as a whole to overcome issues with sending large file as a whole. There were two stratergies that would have taken:
    1. Either send line by line
	or
	2. Send as data chunks, for eg : 1 MB data
In this project  the first approach is used assuming that a single line data will not overflow the memory of the system
- Multithreading is implmented in multiple places, including add command to send multiple files, wc command getting word count of all the files, freq-words command getting the most or least frequent words in all the files.
- If there is an issue with network connection, then we will retry upto 5 times
- Only try to modify/create/delete files through the CLI app.
- A linux environment is considered for running client and server applications.

#### Further development
1. Metadata file will contain all the basic details of the files. This file can be used for further developement in future to include thve feature to pause and start download whenever the user wants so that the next time when user tries to repload, the upload starts from the last line that was sent before.

2. Data chunk based approach can also be followed to include more type of files like video files.

3. If you want to build the image locally, just copy the Dockerfile outside the server and client folders and execute the below command
```sh
docker build -t <image name>:<tag name> . --no-cache
```
eg: 
```sh
docker build -t krishnanunni333/store-full-app:v0.1 . --no-cache
```
#### Notes
1. **While getting inside container through VScode, please go to root folder. The repo txt_puller will be there** 
2. **If you are facing error related to config from binary, please store the path of store.properties to PROPERTIES_PATH variable**


