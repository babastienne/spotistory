## Spotistory

This little project is made in order to keep into a databse some informations about my listenings on spotify.
Using the spotify API as well as spotipy and flask, it fetch the history of listening of a user. It also keep into separate table informations about tracks played, artists and genres.

## Run

#### Initialize

First of all don't forget to install the requirements for the project by running `pip install -r requirements.txt` !

You should insert into the config file some informations : client_id and client_secret.
Then in order to generate an access token for your profile you need to run the program with the command `python path/to/program/main.py --init`. the init parameter will launch a server running on the address in the config file (default is `http://127.0.0.1:8080`).
visit the address and it should return a message indicating that everything went fine. If you visit your configuration file it should now be filled with an access_token and a refresh_token as well. 

#### Launch the synchronization

After the init step, you can now launch the program `python /path/to/program/main.py`. It will fetch the most recently played songs on your profile and stock them into a database (path to the database can be put in the configuration file).
