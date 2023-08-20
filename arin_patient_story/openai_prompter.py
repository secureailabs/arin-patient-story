import json
import os

import openai


class OpenaiPrompter:
    def __init__(self) -> None:
        pass

    def prompt(self, text: str) -> str:
        return "prompted text"

    def prompt_story(self, transcript: str) -> str:

        return "prompted text"

    path_file_transcript = "transcript.json"
    openai.api_key = os.environ["OPENAI_API_KEY"]
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
    list_instruction.append(
        "Under the `Events` key list all events in the patients treatment use key `Description` for the description  add `Date` if known"
    )
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

    call_dict = {}
    call_dict["model"] = "gpt-3.5-turbo-16k"
    call_dict["temperature"] = 0.95
    call_dict["messages"] = list_message

    chat = openai.ChatCompletion.create(**call_dict)

    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    list_message.append({"role": "assistant", "content": reply})
    print(f"ChatGPT: {reply}")
    list_message.append({"role": "assistant", "content": reply})
