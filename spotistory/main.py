# -*- coding: utf-8 -*-

import argparse
import os
import toml
import spotify
import authentication
from dbmanager import dbManager

here = os.path.dirname(__file__)
os.chdir(here)
print here

# Ici on gère les arguments d'appel du script

default_file_config = "conf/default-config.toml"
parser = argparse.ArgumentParser(description="Manage a history of the music you listen on Spotify")
parser.add_argument("--config", help="Specifies the config file to use")
parser.add_argument("--init", help="For the first connection launch an authentication server")
args = parser.parse_args()

# On charge la config
config_file = args.config if args.config and os.path.isfile(args.config) else default_file_config
config = toml.load(config_file)

# authenticate the user if not already done
auth = authentication(config, config_file)
if args.init:
    authentication.launch()
    return

application = spotify.spotify(
    client_id=config["spotify"]["client_id"],
    client_secret=config["spotify"]["client_secret"],
    redirect_uri=config["spotify"]["redirect_uri"],
    access_token=config["spotify"]["access_token"],
    refresh_token=config["spotify"]["refresh_token"]
)

# On créer la bdd et on l'initialise (création des tables)
db_manager = dbManager(config["database"]["name"])
db_manager.init_db()

tracks = application.get_history()
db_manager.add_tracks(tracks)
tracks_to_add = db_manager.get_non_added_tracks()

db_manager.set_added()
