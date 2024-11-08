import requests, os
from pytubefix import YouTube
from pytubefix.cli import on_progress
from ..util import print_log


class DownloadVideo:
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url

    def is_youtube_url(self):
        YOUTUBE_URL_TYPE_A = "https://youtube.com"
        YOUTUBE_URL_TYPE_B = "https://m.youtube.com"
        YOUTUBE_URL_TYPE_C = "https://www.youtube.com"
        YOUTUBE_URL_TYPE_D = "https://youtu.be"
        return self.url.startswith(
            (
                YOUTUBE_URL_TYPE_A,
                YOUTUBE_URL_TYPE_B,
                YOUTUBE_URL_TYPE_C,
                YOUTUBE_URL_TYPE_D,
            )
        )

    def youtube_video_download(self):
        output_path = "data/video"
        yt = YouTube(self.url, on_progress_callback=on_progress)
        ys = yt.streams.get_highest_resolution()
        video = ys.download(output_path)
        os.rename(video, f"{output_path}/{self.filename}.mp4")

    def non_youtube_video_download(self):
        r = requests.get(self.url)
        with open(f"data/video/{self.filename}.mp4", "wb") as outfile:
            outfile.write(r.content)

    def download_video(self):
        print_log("Video downloading started.")
        try:
            if self.is_youtube_url():
                self.youtube_video_download()
            else:
                self.non_youtube_video_download()
            print_log("Video downloaded successfully.")
        except Exception as e:
            raise Exception(e)
