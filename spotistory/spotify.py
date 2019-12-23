# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import json
import track
import time
from calendar import timegm
from track import track


scope = 'user-library-read user-read-recently-played playlist-modify-public playlist-modify-private'

class spotify:

    def __init__(self, client_id, client_secret, redirect_uri, access_token, refresh_token):
        self.PATTERN = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri)
        self.token = access_token
        self.refresh = refresh_token
        self.check_token()
        self.sp = spotipy.Spotify(auth=self.token)

    def check_token(self):
        self.token = self.oauth.refresh_access_token(self.refresh)

    def get_history(self):
            results = self.sp._get("me/player/recently-played", limit=50)
            tracks = []
            for item in results["items"]:
                played_at = timegm(time.strptime(item["played_at"], self.PATTERN))
                current = track(item["track"]["id"], item["track"]["uri"], played_at)
                tracks.append(current)
            return tracks

    # def create_playlist(self, name):
    #     results = self.sp.user_playlist_create(self.user, name)
    #     return results

    # def add_tracks_playlist(self, playlist, tracks):
    #         try:
    #             print tracks
    #             results = self.sp.user_playlist_add_tracks(self.user, playlist, tracks)
    #             return results
    #         except Exception:
    #             return None

    # def get_playlist(self, playlist):
    #         try:
    #             results = self.sp.user_playlist(self.user)
    #             print results
    #             return json.loads(str(results).encode('unicode-escape'))
    #         except Exception:
    #             return None

    # def get_all_playlists(self):
    #         try:
    #             results = self.sp.current_user_playlists()
    #             playlists = []
    #             for item in results["items"]:
    #                 playlists.append((item["name"], item["id"]))
    #             return dict(playlists)

    #         except Exception:
    #             return None

    # def is_playlist_created(self, name):
    #     playlists = self.get_all_playlists()
    #     if(name in playlists.viewkeys()):
    #         return (True, playlists[name])
    #     return (False, "no")


