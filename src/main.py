# -*- coding: utf-8 -*-

import sys
import credentials
import spotify
from db_manager import db_manager

db_manager = db_manager("test.db")
db_manager.init_db()

application = spotify.spotify(credentials.token, credentials.user)

tracks = application.getHistory()
db_manager.add_tracks(tracks)
tracks_to_add = db_manager.get_non_added_tracks()

(playlist_present, playlist_id) = application.is_playlist_created("W18")

if(not playlist_present):
    playlist_id = application.createPlaylist("W18")["id"]

print tracks_to_add

application.addTracksPlaylist(playlist_id, [x[1] for x in tracks_to_add])

db_manager.set_added()

