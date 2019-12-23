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
args = parser.parse_args()

# On charge la config
config_file = args.config if args.config else default_file_config
# if args.config and os.path.isfile(args.config):
#     config = toml.load(args.config)
# else:
    config = toml.load(config_file)

# authenticate the user
auth = authentication(config, config_file)
if args.init:
    authentication.launch()
else:
    authentication.reconnect()

# On créer le handler de l'api Spotify
if ("refresh_token" in config["spotify"] and "access_token" in config["spotify"]):
    application = spotify.spotify(client_id=config["spotify"]["client_id"],
                                  client_secret=config["spotify"]["client_secret"],
                                  username=config["spotify"]["username"],
                                  redirect_uri=config["spotify"]["redirect_url"],
                                  access=config["spotify"]["access_token"],
                                  refresh=config["spotify"]["refresh_token"])
else:
    application = spotify.spotify(client_id=config["spotify"]["client_id"],
                                  client_secret=config["spotify"]["client_secret"],
                                  username=config["spotify"]["username"],
                                  redirect_uri=config["spotify"]["redirect_url"])
    config["spotify"]["refresh_token"] = application.refresh
    config["spotify"]["access_token"] = application.token
    config["spotify"]["expires_at"] = application.expiration

# On stock les infos utiles
# with open(default_file_config, 'w') as myfile:
#     toml.dump(config, myfile)


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
