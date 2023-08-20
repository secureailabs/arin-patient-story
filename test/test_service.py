from time import sleep

import requests

if __name__ == "__main__":
    url_base = "http://localhost:8000/"
    # list_url = [
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
    list_url = ["https://www.youtube.com/watch?v=kn5PT3mAOHQ"]
    for url in list_url:
        response = requests.post(
            url_base + "process_youtube/?url={https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DBvVzcobqjck}"
        )
        # response = requests.post(url_base + "process_youtube/?url={url}")
        job = response.json()
        job_id = job["job_id"]
        while job["status"] != "completed":
            print(job["status"])
            job = requests.get(url_base + f"job/{job_id}").json()
            sleep(1)

        transcript = requests.get(url_base + f"transcript/{job_id}").json()
        print(transcript["text"])
        story = requests.get(url_base + f"story/{job_id}").json()
        print(story)
