# -*- coding: utf-8 -*-

import spotipy
import spotipy.oauth2 as oauth2
from models import artist, track, history, user
import time
from calendar import timegm


class spotify:

    def __init__(self, config):
        self.PATTERN = '%Y-%m-%dT%H:%M:%S.%fZ'
        self.oauth = oauth2.SpotifyOAuth(
            config['client_id'],
            config['client_secret'],
            config['redirect_uri']
        )
        self.token = config['access_token']
        self.refresh = config['refresh_token']
        self.api_url = '{0}/{1}/'.format(config['api_base_url'], config['api_version'])
        self.check_token()
        self.sp = spotipy.Spotify(auth=self.token)
        # elems
        self.artists = []
        self.tracks = []
        self.historics = []
        self.user_id = config['user_id']

    def check_token(self):
        resp = self.oauth.refresh_access_token(self.refresh)
        self.token = resp['access_token']
        self.refresh = resp['refresh_token']

    def get_user_profile(self):
        result = self.sp.me()
        self.user_id = result['id']
        return user.User(
            self.user_id,
            result['display_name'],
            result['followers']['total'],
            result['uri']
        )

    def get_history(self):
        results = self.sp._get('me/player/recently-played', limit=50)
        tracks, artists, historics = [], [], []

        for item in results['items']:
            # fetch artists related to track
            for a in item['track']['artists']:
                artists.append(
                    artist.Artist(
                        a['id'],
                        a['uri'],
                        a['name']
                    )
                )
            # fetch track information
            tracks.append(
                track.Track(
                    item['track']['id'],
                    item['track']['uri'],
                    item['track']['duration_ms'] // 1000,
                    item['track']['artists'][0]['id'],  # FIXME create relational table to avoid choosing only the first artist related to a track
                    item['track']['name']
                )
            )
            # fetch item information
            historics.append(
                history.History(
                    item['track']['id'],
                    timegm(time.strptime(item['played_at'], self.PATTERN)),
                    self.user_id
                )
            )
        # save data
        self.artists, self.tracks, self.historics = artists, tracks, historics
        # return historics
        return self.historics

    def get_history_related_artists(self):
        return self.artists

    def get_history_related_tracks(self):
        return self.tracks
