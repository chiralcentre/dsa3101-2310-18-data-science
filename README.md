# DataGuru

A DSA3101 group project of the topic "What is Data Science?"

## Usage

1. Clone the repo

    ```
    git clone https://github.com/chiralcentre/dsa3101-2310-18-data-science.git
    ```

2. Install Docker. Refer to the following guides for instructions.

- [Windows](https://docs.docker.com/windows/started)
- [OS X](https://docs.docker.com/mac/started/)
- [Linux](https://docs.docker.com/linux/started/)

3. Once installed, start Docker and make sure the Docker Engine is running successfully. 

4. In the command terminal of your system, run 
    ```
    docker compose up -d
    ```
    The first boot up will take some time (~15 min) so just be patient please. 
    
    Note that the backend models will need some additional time (~3min) to initialize even after the docker containers started running. 

5. Access the DataGuru website via `http://localhost:3000/` and the backend API via `http://localhost:5000/`. 