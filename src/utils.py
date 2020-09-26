import os
import subprocess

APP_NAME = 'syd-music'
#manual events
ON_BEGIN = 'event-begin'
ON_PROGRESS = 'event-dl-progress'
ON_CONVERT_BEGIN = 'event-convert-begin'
ON_CONVERT_END = 'event-convert-end'
ON_ERROR = 'event-error'
BTN_DL_ENABLED = 'event-dl-enabled'
CLEAR = 'event-clear'
#view keys
BTN_DL = 'event-download'
BTN_VIEW = 'event-view'
INPUT_URL = 'url'
LABEL_STATUS = 'status'
#other constants
TRUNC_SIZE = 24

#paths
DL_PATH = '{}/Music/{}/'.format(os.environ['HOME'], APP_NAME)
OUTTMPL_SINGLES = '{}%(title)s.%(ext)s'.format(DL_PATH)
OUTTMPL_PLAYLIST = '{}%(playlist)s/%(title)s.%(ext)s'.format(DL_PATH)

def base_filename(path):
    #get filename without path
    filename = os.path.basename(path)
    #remove extension
    filename = os.path.splitext(filename)[0]
    return filename

def trunc(text, trunc_size):
    if len(text) > trunc_size: 
        text = text[:trunc_size] + '…'
    return text

def open_file(path):
    subprocess.Popen(['xdg-open', path])