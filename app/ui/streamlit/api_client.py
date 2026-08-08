import json

import requests


class DebateAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")


    def run_debate(self,topic:str,max_rounds:int):
        response = requests.post(
            f"{self.base_url}/debates",
            json={
                "topic": topic,
                "max_rounds": max_rounds,
            },
        )

        response.raise_for_status()

        return response.json()

    def stream_debate(
        self,
        topic: str,
        max_rounds: int,
    ):
        response = requests.post(
            f"{self.base_url}/debates/stream",
            json={
                "topic": topic,
                "max_rounds": max_rounds,
            },
            stream=True,
        )

        response.raise_for_status()

        for line in response.iter_lines(chunk_size=1):
            if not line:
                continue
            line=line.decode('utf-8')
            if line.startswith("data: "):
                payload = line.removeprefix("data: ")
                yield json.loads(payload)