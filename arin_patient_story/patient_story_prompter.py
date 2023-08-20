import json
import os

import openai
from arin_core_azure.env_tools import get_string_from_env
from arin_openai.client_openai import ClientOpenai


class PatientStoryPrompter:
    def __init__(self):
        engine_name = get_string_from_env("OPENAI_ENGINE_NAME")
        self.client = ClientOpenai.from_default_azure(engine_name, do_cache=False)

    def prompt(self, path_file_transcript: str, path_file_story: str):
        if not os.path.isfile(path_file_transcript):
            raise RuntimeError(f"Transcipt file does not exist: {path_file_transcript}")
        path_dir_story = os.path.dirname(path_file_story)
        if not os.path.exists(path_dir_story):
            os.makedirs(path_dir_story)

        with open(path_file_transcript, "r") as file:
            transcript = json.load(file)

        with open(path_file_transcript, "r") as file:
            transcript = json.load(file)
        text = transcript["text"]
        list_message = []
        list_message.append(
            {
                "role": "system",
                "content": "You are an assistent for processing informal patient stories to stuctured data",
            }
        )
        # instructions:
        list_instruction = []
        list_instruction.append("Reply only in json")
        list_instruction.append("Leave keys empty if not known")
        list_instruction.append(
            "Use the follwing keys: `Patient Name`, `Patient Age`, `Primary Diagnoses`, `Events`, `Institutions`"
        )
        list_instruction.append("Under the `Events` key list all events in the patients treatment add `Date` if known")
        list_instruction.append(
            "In every event under the key `Emotion` also list a assement of the emotional state of the patient during that event"
        )
        list_instruction.append(
            "Under the key `Institutions` list all institutions and organisations the patient interacted with"
        )

        for i, instruction in enumerate(list_instruction):
            list_message[0]["content"] += f"\n{str(i+1)}. {instruction}"

        list_message.append(
            {
                "role": "user",
                "content": f"convert the following patient story to structured data: ```{text}```",
            }
        )

        chat = self.client.chat_completion_messages(list_message, temperature=0.95)

        reply = chat.choices[0].message.content

        story = json.loads(reply)
        with open(path_file_story, "w") as file:
            json.dump(story, file)
