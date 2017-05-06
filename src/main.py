# -*- coding: utf-8 -*-

import argparse
import os
import toml
import spotify
from dbmanager import dbManager

# Ici on gère les arguments d'appel du script

default_file_config = "../conf/default-config.toml"
parser = argparse.ArgumentParser(description="Manage a history of the music you listen on Spotify")
parser.add_argument("--config", help="Specifies the config file to use")
args = parser.parse_args()

# On charge la config

if(args.config and os.path.isfile(args.config)):
    config = toml.load(args.config)
else:
    config = toml.load(default_file_config)

# On créer le handler de l'api Spotify
application = spotify.spotify(config["spotify"]["client_id"], config["spotify"]["client_secret"], config["spotify"]["username"])
config["spotify"]["refresh_token"] = application.refresh
config["spotify"]["access_token"] = application.token

# On stock les infos utiles
with open(default_file_config, 'w') as myfile:
    toml.dump(config, myfile)


# On créer la bdd et on l'initialise (création des tables)
db_manager = dbManager(config["database"]["name"])
db_manager.init_db()

tracks = application.get_history()
db_manager.add_tracks(tracks)
tracks_to_add = db_manager.get_non_added_tracks()
(playlist_present, playlist_id) = application.is_playlist_created("W18")

if(not playlist_present):
    playlist_id = application.create_playlist("W18")["id"]

application.add_tracks_playlist(playlist_id, [x[1] for x in tracks_to_add])
db_manager.set_added()

