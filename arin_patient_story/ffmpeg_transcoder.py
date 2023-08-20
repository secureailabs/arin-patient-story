import os
import subprocess


class FFmpegTranscoder:
    def __init__(self):
        self.path_file_ffmpeg = os.getenv("PATH_FILE_FFMPEG", "ffmpeg")

    def extract_audio(self, path_file_input: str, path_file_output: str):
        if not os.path.isfile(path_file_input):
            raise RuntimeError("Input file does not exist")
        output_path = os.path.dirname(path_file_output)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        try:
            subprocess.run(
                [self.path_file_ffmpeg, "-i", path_file_input, "-vn", "-acodec", "libmp3lame", "-y", path_file_output],
                check=True,
            )
            print("Audio extracted and saved as:", path_file_output)
        except subprocess.CalledProcessError as e:
            print("Error occurred while extracting audio:", e)
