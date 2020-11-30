# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import signal
import time
import webbrowser

import win32api
import wmi
from pip._vendor import requests
from win32con import VK_MEDIA_PLAY_PAUSE, KEYEVENTF_EXTENDEDKEY


os.environ["SPOTIPY_CLIENT_ID"] = "ba4d42f183344519be578ae32c894494"
os.environ["SPOTIPY_CLIENT_SECRET"] = "83fbc1cf5e1449a591a2a962a1783fff"

client_id = "ba4d42f183344519be578ae32c894494"
client_secret = "83fbc1cf5e1449a591a2a962a1783fff"

url_for_initial_get = "https://accounts.spotify.com/authorize?client_id=ba4d42f183344519be578ae32c894494&response_type=code&redirect_uri=https%3A%2F%2Faavvii.github.io%2FSpotiFreeHost&scope=user-read-playback-state%20user-modify-playback-state&state=34fFs29kd09"


def get_played_track_type(token):
    payload = {'Authorization': "Bearer " + token}
    r = requests.get(url="https://api.spotify.com/v1/me/player/currently-playing", headers=payload)
    if r.status_code == 204:
        return "Not playing"
    elif r.status_code == 200:
        data = r.json()
        # print song name
        # if data['currently_playing_type'] != "ad":
            # print(data['item']['name'])
        return data['currently_playing_type']
    else:
        return "Failed"


def get_next_token(old_token):
    payload = {
        'grant_type': "refresh_token",
        'refresh_token': old_token,
        'client_id': client_id,
        'client_secret': client_secret
    }

    post = requests.post("https://accounts.spotify.com/api/token", data=payload)
    # print(post.json())
    return post.json()['access_token']


def get_init_token():
    url = webbrowser.open(url_for_initial_get)

    grant_type = "authorization_code"

    code = input("Please enter the code you got from the browser\n")

    redirect_uri = "https://aavvii.github.io/SpotiFreeHost"

    payload = {
        'grant_type': grant_type,
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    post = requests.post("https://accounts.spotify.com/api/token", data=payload)
    # print(post.json())
    # print(post)

    token = post.json()['access_token']
    refresh_token = post.json()['refresh_token']

    # print(token)
    return token, refresh_token


def resume_play():
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)


def kill_spotify():
    # Initializing the wmi constructor
    f = wmi.WMI()
    # Iterating through all the running processes
    for process in f.Win32_Process():
        if process.Name == "Spotify.exe":
            try:
                os.kill(process.ProcessId, signal.CTRL_C_EVENT)
            except:
                pass


def start_spotify():
    os.system('C:\\Users\\Avi\\AppData\\Roaming\\Spotify\\SpotifyLauncher.exe')


def make_sure_spotify_runs():
    print("Ensuring spotify is running...")
    runs = False
    f = wmi.WMI()
    # Iterating through all the running processes
    for process in f.Win32_Process():
        if process.Name == "Spotify.exe":
            runs = True
    if not runs:
        start_spotify()


def run():
    token, refresh_token = get_init_token()
    print("Service started!")
    while True:
        track_info = get_played_track_type(token)
        if track_info == "ad":
            kill_spotify()
            start_spotify()
            time.sleep(0.5)
            resume_play()
            current_time = time.localtime()
            current_time = time.strftime("%H:%M:%S", current_time)
            print("Skipped an ad at", current_time)
        if track_info == "Failed":
            get_next_token(refresh_token)
        time.sleep(2.5)


if __name__ == '__main__':
    make_sure_spotify_runs()
    run()
