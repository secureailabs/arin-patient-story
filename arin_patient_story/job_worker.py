import hashlib
import json
import os
import threading
from queue import Queue

from arin_core_azure.env_tools import get_dir_from_env

from arin_patient_story.ffmpeg_transcoder import FFmpegTranscoder
from arin_patient_story.patient_story_prompter import PatientStoryPrompter
from arin_patient_story.whisper_transcriber import WhisperTranscriber
from arin_patient_story.youtube_downloader import YoutubeDownloader


class JobWorker(threading.Thread):
    def __init__(self, path_dir_data: str, queue: Queue, dict_job: dict):
        super().__init__()
        self.path_dir_data = path_dir_data
        self.queue = queue
        self.dict_job = dict_job
        self.downloader = YoutubeDownloader()
        self.transcoder = FFmpegTranscoder()
        self.transcriber = WhisperTranscriber()
        self.prompter = PatientStoryPrompter()

    @staticmethod
    def load_dict_job() -> dict:
        path_dir_data = get_dir_from_env("PATH_DIR_DATA_PATIENT_STORY", create_if_missing=True)
        path_file_dict_job = os.path.abspath(os.path.join(path_dir_data, "dict_job.json"))
        if os.path.exists(path_file_dict_job):
            with open(path_file_dict_job, "r") as file:
                dict_job = json.load(file)
        else:
            dict_job = {}
        return dict_job

    @staticmethod
    def save_dict_job(dict_job: dict) -> None:
        path_dir_data = get_dir_from_env("PATH_DIR_DATA_PATIENT_STORY", create_if_missing=True)
        path_file_dict_job = os.path.abspath(os.path.join(path_dir_data, "dict_job.json"))
        with open(path_file_dict_job, "w") as file:
            json.dump(dict_job, file)

        def get_job_id(self, url: str) -> str:
            return hashlib.sha256(url.encode()).hexdigest()

    def get_job_id(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def process_queue(self):
        job_id = self.queue.get()
        job = self.dict_job[job_id]
        self.process_job(job)

    def process_job(self, job: dict):
        job_id = job["job_id"]
        url = job["url"]
        path_file_video = os.path.abspath(os.path.join(self.path_dir_data, "video", job_id, "video.mp4"))
        path_file_audio = os.path.abspath(os.path.join(self.path_dir_data, "audio", job_id, "audio.mp3"))

        path_file_transcript = os.path.abspath(
            os.path.join(self.path_dir_data, "transcript", job_id, "transcript.json")
        )
        path_file_story = os.path.abspath(os.path.join(self.path_dir_data, "story", job_id, "story.json"))
        try:
            job["status"] = "downloading"
            JobWorker.save_dict_job(self.dict_job)
            self.downloader.download(url, path_file_video)

            job["status"] = "transcoding"
            JobWorker.save_dict_job(self.dict_job)
            self.transcoder.extract_audio(path_file_video, path_file_audio)

            job["status"] = "transcribing"
            JobWorker.save_dict_job(self.dict_job)
            self.transcriber.transcribe(path_file_audio, path_file_transcript)

            job["status"] = "prompting"
            JobWorker.save_dict_job(self.dict_job)
            self.prompter.prompt(path_file_transcript, path_file_story)

            with open(path_file_story, "r") as file:
                job["story"] = json.load(file)
            job["status"] = "completed"
            JobWorker.save_dict_job(self.dict_job)
        except Exception as e:
            job["status"] = "failed"
            job["error_message"] = str(e)
            print(str(e))

            JobWorker.save_dict_job(self.dict_job)

    def run(self):
        while True:
            self.process_queue()
