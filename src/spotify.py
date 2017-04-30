# -*- coding: utf-8 -*-

import sys
import spotipy
import spotipy.util as util
import json

scope = 'user-library-read'

class spotify:

    def __init__(self, token, user):
        self.token = token
        self.user = user

    def getHistory(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            results = sp._get("me/player/recently-played", limit=50)
            for item in results['items']:
                track = item
                print track
                print "\n"
            return json.loads(str(results).encode('unicode-escape'), encoding="UTF-8")
        else:
            print "Can't get token for" + self.user

    def createPlaylist(self, name):
        if self.token and self.user:
            try:
                sp = spotipy.Spotify(auth=self.token)
                results = sp.user_playlist_create(self.user, name)
                print results
                return json.loads(str(results).encode('unicode-escape'))
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
