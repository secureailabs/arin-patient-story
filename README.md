# arin-patient-story

## startup manual

set the following environment variable: \\
```
"PATH_DIR_DATA_PATIENT_STORY"="/data/patient_story"
"PATH_FILE_FFMPEG"="/usr/bin/ffmpeg"
"OPENAI_API_KEY"=
```
start the service from the app folder or use the docker_deploy command \\
```uvicorn main:app --host 0.0.0.0 --port 8000```

## startup docker
set the following environment variable: \\
```
"ARIN_PYPI_REPOSITORY_URL"=
"ARIN_PYPI_USERNAME"=
"ARIN_PYPI_PASSWORD"=
"PATH_DIR_DATA_PATIENT_STORY"="/data/patient_story"
"PATH_FILE_FFMPEG"="/usr/bin/ffmpeg"
"OPENAI_API_KEY"=
```
python deploy_docker.py \\

## usage
at the /docs# endpoint you will find a swagger documentation \\

using the ```process_youtube{url}``` endpoint you can create a job.\\
This will return you a ```job_id```\\
\\
using the ```get_job\{job_id}``` endpoint you can check the status of this job.\\
\\
Job will progress through the following stages\\
*queued\\
*downloading\\
*transcoding (ffmpeg extracts audio and recodes to mp3)\\
*transcribing (whisper exctracts a transcript at about 4 times playback speed)\\
*promting (GPT3 is used to convert transcript to json)\\
\\
using the ```listjobs``` endpoint you can check the status of all jobs.\\
\\
if you do not like the final output you can repromt with the ```redo_prompt\{job_id}``` endpoint \\