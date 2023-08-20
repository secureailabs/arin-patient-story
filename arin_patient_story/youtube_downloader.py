import os
from typing import Dict, Optional

from pytube import Channel, Playlist, YouTube


class YoutubeDownloader:
    def download(self, video_page_url: str, path_file_target: str) -> None:
        youtube_object = YouTube(video_page_url)
        youtube_object = youtube_object.streams.get_highest_resolution()
        if youtube_object is None:
            raise RuntimeError("An error has occurred while getting highest resolution")
        try:
            output_path = os.path.dirname(path_file_target)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            filename = os.path.basename(path_file_target)
            youtube_object.download(output_path=output_path, filename=filename)
        except:
            raise RuntimeError("An error has occurred while downloading")

        if not os.path.isfile(path_file_target):
            raise RuntimeError("video does not exist after download")

        print("Download is completed successfully")


# class UserChannel(Playlist):
#     def __init__(self, user_handle: str, proxies: Optional[Dict[str, str]] = None):
#         """Construct a :class:`Channel <Channel>`.
#         :param str url:
#             A valid YouTube channel URL.
#         :param proxies:
#             (Optional) A dictionary of proxies to use for web requests.
#         """
#         self.user_handle = user_handle
#         self.channel_url = f"https://www.youtube.com/{self.user_handle}"
#         super().__init__(self.channel_url, proxies)

#         self.videos_url = self.channel_url + "/videos"
#         self.playlists_url = self.channel_url + "/playlists"
#         self.community_url = self.channel_url + "/community"
#         self.featured_channels_url = self.channel_url + "/channels"
#         self.about_url = self.channel_url + "/about"

#         # Possible future additions
#         self._playlists_html = None
#         self._community_html = None
#         self._featured_channels_html = None
#         self._about_html = None


# channel = UserChannel("@katiekickscancer4840")
# user_handle = "@katiekickscancer"
# list_url_video = [
#     "https://www.youtube.com/watch?v=Js27JwrXsIg",
#     "https://www.youtube.com/watch?v=92Da-XC-7dk",
#     "https://www.youtube.com/watch?v=xu6uv0aGTCY",
#     "https://www.youtube.com/watch?v=jT2PFFmeeBk",
#     "https://www.youtube.com/watch?v=HOpILlb9FyM",
#     "https://www.youtube.com/watch?v=JcLkww0tEIc",
#     "https://www.youtube.com/watch?v=ZW2-ciZbXtM",
#     "https://www.youtube.com/watch?v=Iue_GsVen0U",
#     "https://www.youtube.com/watch?v=BvVzcobqjck",
# ]

# for url in list_url_video:
#     id_video = url.split("https://www.youtube.com/watch?v=")[1]
#     print(id_video)
#     video = {}
#     video["video_source"] = "youtube"
#     video["id_video"] = id_video
#     video["url_video_page"] = url
#     video_dict[id_video] = video
#     youtube = YouTube(url)
#     if context.has_video_content(user_handle, id_video):
#         continue
#     output_path = os.path.dirname(context._path_video_content(user_handle, id_video))
#     filename = id_video + ".mp4"
#     youtube.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().last().download(
#         output_path, filename
#     )
