#!/usr/bin/env python
import PySimpleGUI as sg
import subprocess
import youtube_dl
import os
import threading

app_name = 'syd-music'
sg.theme('LightGreen')
layout = [  [sg.Text('YouTube URL')],
            [sg.InputText(key='url')], 
            [sg.Button('Download MP3', key='dl'), sg.Button('View downloaded songs', key='view')], 
            [sg.Text(key='status', size=(24,1))] ]
window = sg.Window('syd-music', layout)

download_path = '{}/Music/{}/'.format(os.environ['HOME'], app_name)
ydl_opts = {
    'outtmpl': '{}%(title)s.%(ext)s'.format(download_path),
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '128',
    }],
}
ytdl = youtube_dl.YoutubeDL(ydl_opts)

def download(url, callback):
    ytdl.download([url])
    callback()

def on_dl_start():
    window['dl'].update(disabled=True)
    window['status'].update('Downloading...')

def on_dl_complete():
    window['status'].update('Done!')
    window['dl'].update(disabled=False)

while True: 
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'dl':
        on_dl_start()
        threading.Thread(
            target=download, 
            args=(values['url'], on_dl_complete)
        ).start()
        continue
    if event == 'view':
        subprocess.Popen(['xdg-open', download_path])

window.close()
