import os
from queue import Queue

from arin_patient_story.ffmpeg_transcoder import FFmpegTranscoder
from arin_patient_story.job_worker import JobWorker
from arin_patient_story.patient_story_prompter import PatientStoryPrompter
from arin_patient_story.whisper_transcriber import WhisperTranscriber
from arin_patient_story.youtube_downloader import YoutubeDownloader

if __name__ == "__main__":
    path_dir_data = os.environ.get("PATH_DIR_DATA_PATIENT_STORY")
    dict_job = {}
    url_queue = Queue()
    # url = "https://www.youtube.com/watch?v=kn5PT3mAOHQ"
    url = "https://www.youtube.com/watch?v=BvVzcobqjck"  # shorter video
    worker = JobWorker(path_dir_data, url_queue, dict_job)
    job_id = worker.get_job_id(url)
    job = {"job_id": job_id, "url": url, "status": "queued", "error_message": "", "story": ""}
    worker.process_job(job)
