# -*- coding: utf-8 -*-

import requests
import spotipy.oauth2 as oauth2
from track import track
import time
from calendar import timegm


class spotify:

    def __init__(self, config):
        self.PATTERN = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.oauth = oauth2.SpotifyOAuth(config["client_id"], config["client_secret"], config["redirect_uri"])
        self.token = config["access_token"]
        self.refresh = config["refresh_token"]
        self.api_url = "{0}/{1}/".format(config["api_base_url"], config["api_version"])
        self.check_token()

    def check_token(self):
        resp = self.oauth.refresh_access_token(self.refresh)
        self.token = resp["access_token"]
        self.refresh = resp["refresh_token"]

    def request(self, method, url, **params):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}'.format(self.token),
        }
        args = dict(params=params)
        response = requests.request(method, self.api_url + url, headers=headers, **args)
        return response.json()

    def get_history(self):
        results = self.request("GET", 'me/player/recently-played', limit=50)
        tracks = []
        for item in results["items"]:
            played_at = timegm(time.strptime(item["played_at"], self.PATTERN))
            current = track(item["track"]["id"], item["track"]["uri"], played_at)
            tracks.append(current)
        return tracks
