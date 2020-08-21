#Description: Goes into one of your Spotify Playlist and selects certain songs that match requirements

import os
import sys
import re
import json
import requests

from secrets import spotify_token, spotify_user_id

class CreatePlaylist:
    def __init__(self):
        pass
    def get_spotify_playlist(self):
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        #print(response_json)
        playlist_name = []
        playlist_id = []
        for item in response_json["items"]:
            playlist_name.append(item["name"])
            playlist_id.append(item["id"])
            #https://open.spotify.com/playlist/{playlist_id}
        playlist_info = dict(zip(playlist_name, playlist_id))
        print("Type one of these playlists:" + str(playlist_name))
        chosen_playlist_name = input()
        chosen_playlist_id = playlist_info[chosen_playlist_name]
        return chosen_playlist_id

    def select_tracks(self):
        playlist_id = self.get_spotify_playlist() #gets the playlist's id
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        track_id = []
        for item in response_json["items"]:
            #track_name.append(item["track"]["name"])
            track_id.append(item["track"]["id"])
            #http://open.spotify.com/track/{track_id}
        accepted_songs = []
        for id in track_id:
            audio_query = "https://api.spotify.com/v1/audio-features/{}".format(
                id)
            audio_response = requests.get(
                audio_query,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(spotify_token)
                }
            )
            audio_response_json = audio_response.json()
            if audio_response_json["tempo"] > 160.0:
                accepted_songs.append(id)

        return accepted_songs

    def create_new_playlist(self):
        request_body = json.dumps({
            "name": "Project Playlist Tempo160+",
            "description": "Proj 2",
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        return response.json()["id"]
    def spotify_id_to_uris(self, track_ids):
        uris = []
        for ids in track_ids:
            uris.append("spotify:track:" + ids)
        return uris

    def add_song_to_playlist(self):
        song_list = self.select_tracks()
        uris = self.spotify_id_to_uris(song_list)
        new_playlist_id = self.create_new_playlist()

        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            new_playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        print("New Playlist Made!")
        return response_json

if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()
