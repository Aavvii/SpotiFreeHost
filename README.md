SpotifyFree is a python project dedicated to closing the spotify app whenever it plays an ad, and restarting it afterwards. This is useful because whenever spotify starts, it will never start by playing an ad, so ads can be skipped.
It works using the SpotifyAPI and it constantly checks what kind of content the user is listening to (song, ad, nothing). If an ad is detected, it makes a system call to pause the ad, then closes spotify via PID, opens it back and saves the new PID of the app to quickly close it next time.


This project's main purpose is to provide the host that SpotiFree requires to work.

The source code is also available, it being "main.py".

To use, just download the .zip - it contains the python project with the required libraries. Anyone with python installed should be able to run it.
