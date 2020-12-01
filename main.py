# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import signal
import time
import webbrowser
from os import path

import win32api
import wmi
from pip._vendor import requests
from win32con import VK_MEDIA_PLAY_PAUSE, KEYEVENTF_EXTENDEDKEY


# os.environ["SPOTIPY_CLIENT_ID"] = "ba4d42f183344519be578ae32c894494"
# os.environ["SPOTIPY_CLIENT_SECRET"] = "83fbc1cf5e1449a591a2a962a1783fff"

client_id = "ba4d42f183344519be578ae32c894494"
client_secret = "83fbc1cf5e1449a591a2a962a1783fff"

url_for_initial_get = "https://accounts.spotify.com/authorize?client_id=ba4d42f183344519be578ae32c894494&response_type=code&redirect_uri=https%3A%2F%2Faavvii.github.io%2FSpotiFreeHost&scope=user-read-playback-state%20user-modify-playback-state&state=34fFs29kd09"

spotify_path = ""

checking_frequency = 2.5


def get_spotify_path():
    global spotify_path
    if not path.exists("path.txt"):
        print("It would seem this is your first time running SpotyFree on this machine.")
        path_new = input("Please write the path to the Spotify launcher. It might be at C:\\Users\\<your user name>\\AppData\\Roaming\\Spotify\\SpotifyLauncher.exe\n")
        while not path.exists(path_new) or path_new.split("\\")[-1] != "SpotifyLauncher.exe":
            path_new = input("Launcher could not be found. Please try again\n")
        print("Path seems valid")
        f = open("path.txt", "w")
        f.write(path_new)
        spotify_path = path_new
        f.close()
    else:
        f = open("path.txt", "r")
        spotify_path = f.read()
    return True


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

    code = input("Please copy the code from the browser page you were redirected to\n\n")

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
    os.system(spotify_path)


def make_sure_spotify_runs():
    print("Ensuring spotify is running...\n")
    runs = False
    f = wmi.WMI()
    # Iterating through all the running processes
    for process in f.Win32_Process():
        if process.Name == "Spotify.exe":
            runs = True
    if not runs:
        start_spotify()


def run():
    print("SpotyFree will now open your browser.")
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
        time.sleep(checking_frequency)


if __name__ == '__main__':
    print("Script started...")
    get_spotify_path()
    make_sure_spotify_runs()
    run()
