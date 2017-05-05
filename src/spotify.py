# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import spotipy
import spotipy.util as util
import json
import track
import time
from calendar import timegm
from track import track


scope = 'user-library-read'

class spotify:

    def __init__(self, token, user):
        self.token = token
        self.user = user
        self.PATTERN = "%Y-%m-%dT%H:%M:%S.%fZ"

    def getHistory(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            results = sp._get("me/player/recently-played", limit=50)
            tracks = []
            for item in results["items"]:
                played_at = timegm(time.strptime(item["played_at"], self.PATTERN))
                current = track(item["track"]["id"], item["track"]["uri"], played_at)
                tracks.append(current)
            return tracks
        else:
            print "Can't get token for" + self.user

    def createPlaylist(self, name):
        if self.token and self.user:
            try:
                sp = spotipy.Spotify(auth=self.token)
                results = sp.user_playlist_create(self.user, name)
                return results
            except Exception:
                return None
        else:
            print "Can't get token for" + self.user

    def addTracksPlaylist(self, playlist, tracks):
        if self.token and self.user:
            try:
                sp = spotipy.Spotify(auth=self.token)
                results = sp.user_playlist_add_tracks(self.user, playlist, tracks)
                print results
                return json.loads(str(results).encode('unicode-escape'))
            except Exception:
                return None
        else:
            print "Can't get token for" + self.user

    def getPlaylist(self, playlist):
        if self.token and self.user:
            try:
                sp = spotipy.Spotify(auth=self.token)
                results = sp.user_playlist(self.user)
                print results
                return json.loads(str(results).encode('unicode-escape'))
            except Exception:
                return None
        else:
            print "Can't get token for" + self.user

    def getPlaylists(self):
        if self.token and self.user:
            try:
                sp = spotipy.Spotify(auth=self.token)
                results = sp.current_user_playlists()
                playlists = []
                for item in results["items"]:
                    playlists.append((item["name"], item["id"]))
                return dict(playlists)

            except Exception:
                return None
        else:
            print "Can't get token for" + self.user

    def is_playlist_created(self, name):
        playlists = self.getPlaylists()
        if(name in playlists.viewkeys()):
            return (True, playlists[name])
        return (False, "no")


