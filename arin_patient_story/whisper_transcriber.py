import json
import os

import whisper
from whisper import Whisper


class WhisperTranscriber:
    def __init__(self):
        self.model: Whisper = whisper.load_model("base")

    def transcribe(self, path_file_audio: str, path_file_transcript: str) -> None:
        if not os.path.isfile(path_file_audio):
            raise RuntimeError("audio file does not exist")
        path_dir_transcript = os.path.dirname(path_file_transcript)
        if not os.path.exists(path_dir_transcript):
            os.makedirs(path_dir_transcript)
        transcript = self.model.transcribe(path_file_audio)

        with open(path_file_transcript, "w") as file:
            json.dump(transcript, file)
