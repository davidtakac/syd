import PySimpleGUI as sg
import youtube_dl
import threading
import pyperclip
import utils

class Syd:
    def start(self):
        while True: 
            event, values = self._window.read()
            if event == utils.BTN_DL:
                self._download(values[utils.INPUT_URL])
            elif event == utils.BTN_DL_ENABLED:
                self._window[utils.BTN_DL].update(disabled=not values[event])
            elif event == utils.LABEL_STATUS:
                self._window[event].update(values[event])
            elif event == utils.BTN_VIEW:
                utils.open_file(utils.DL_PATH)
            elif event == utils.PASTE:
                self._paste()
            elif event == utils.CLEAR:
                self._clear()
            elif event == sg.WINDOW_CLOSED:
                break
            else: 
                print(event)

        self._window.close()

    def __init__(self):
        self._init_gui()
        self._init_ytdl()
        
    def _init_gui(self):
        sg.theme('LightGreen')
        menu = [
            ['Edit', [utils.PASTE, utils.CLEAR]],
        ]
        layout = [ 
            [sg.Menu(menu)],
            [sg.Text('YouTube link')],
            [sg.In(key=utils.INPUT_URL)], 
            [sg.Button('Download MP3', key=utils.BTN_DL, bind_return_key=True), sg.Button('View downloaded songs', key=utils.BTN_VIEW)], 
            [sg.Text(key=utils.LABEL_STATUS, size=(36,1))]
        ]
        self._window = sg.Window(utils.APP_NAME, layout)

    def _init_ytdl(self):
        params = {
            #outtmpl is dynamically set
            'format': 'bestaudio/best',
            'quiet': False,
            'progress_hooks': [self._dl_progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
        }
        self._ytdl = youtube_dl.YoutubeDL(params)

    def _download(self, url):
        threading.Thread(
            target=self._dl_worker, 
            args=(url,), 
            daemon=True
        ).start()

    def _event(self, key, value=any):
        self._window.write_event_value(key, value)
    
    def _update_outtmpl(self, isPlaylist):
        self._ytdl.params.update(
            {'outtmpl': utils.OUTTMPL_PLAYLIST if isPlaylist else utils.OUTTMPL_SINGLES}
        )

    def _dl_worker(self, url):
        self._on_begin()
        try:
            info = self._ytdl.extract_info(url, download=False)
            self._update_outtmpl('entries' in info)
            self._ytdl.download([url])
        except:
            self._on_error()
        else:
            self._on_convert_end(info['title'])

    def _dl_progress_hook(self, prog):
        status = prog['status']
        if status == 'downloading':
            self._on_progress_update(prog)
        if status == 'finished':
            self._on_progress_finished(prog)

    def _on_begin(self):
        self._event(utils.BTN_DL_ENABLED, False)
        self._event(utils.LABEL_STATUS, 'Extracting info…')

    def _on_progress_update(self, prog):
        video_name = utils.base_filename(prog['filename'])
        video_name = utils.trunc(video_name, utils.TRUNC_SIZE)
        status_str = '"{}" {}'.format(video_name, prog['_percent_str'])
        self._event(utils.LABEL_STATUS, status_str)

    def _on_progress_finished(self, prog):
        video_name = utils.base_filename(prog['filename'])
        video_name = utils.trunc(video_name, utils.TRUNC_SIZE)
        status_str = '"{}" to MP3…'.format(video_name)
        self._event(utils.LABEL_STATUS, status_str)

    def _on_error(self):
        self._event(utils.LABEL_STATUS, 'Error, check your link.')
        self._event(utils.BTN_DL_ENABLED, True)

    def _on_convert_end(self, title):
        self._event(utils.CLEAR)
        self._event(utils.LABEL_STATUS, '"{}" done!'.format(utils.trunc(title, utils.TRUNC_SIZE)))
        self._event(utils.BTN_DL_ENABLED, True)

    def _paste(self):
        self._window[utils.INPUT_URL].update(pyperclip.paste())

    def _clear(self):
        self._window[utils.INPUT_URL].update('')

if __name__ == '__main__':
    Syd().start()
