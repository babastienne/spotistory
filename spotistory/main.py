# -*- coding: utf-8 -*-

import argparse
import os
import toml
import spotify
import authentication
from dbmanager import dbManager

# Ici on gère les arguments d'appel du script

default_file_config = 'conf/default-config.toml'
parser = argparse.ArgumentParser(description='Manage a history of the music you listen on Spotify')
parser.add_argument('--config', help='Specifies the config file to use')
parser.add_argument('--init', help='For the first connection launch an authentication server to get an access_token.', action='store_true')
args = parser.parse_args()

# On charge la config
config_file = args.config if args.config and os.path.isfile(args.config) else default_file_config
config = toml.load(config_file)

# authenticate the user if not already done
authentication.init(config, config_file)
if args.init:
    authentication.launch()
if not args.init and config['spotify']['access_token'] == '':
    raise Exception('No token provided. To generate a token please run the program with the \'--init\' parameter.')

here = os.path.dirname(__file__)
os.chdir(here)

application = spotify.spotify(
    config=config['spotify']
)

# On créer la bdd et on l'initialise (création des tables)
db_manager = dbManager(config['database']['name'])
db_manager.init_db()

# Si on ne connait pas encore l'utilisateur courant alors on récupère son profil
if config['spotify']['user_id'] == '':
    user = application.get_user_profile()
    config['spotify']['user_id'] = user.id
    # On écrit dans le fichier de config l'id de l'utilisateur
    with open(config_file, 'w') as myfile:
        toml.dump(config, myfile)
    # On créé l'user dans la base
    db_manager.insert_values('user', [user])

# On récupère les données et ajoute le tout en base
historics = application.get_history()
db_manager.insert_values('artist', application.get_history_related_artists())
db_manager.insert_values('track', application.get_history_related_tracks())
db_manager.insert_values('history', historics)
