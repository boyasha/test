import requests


class OpenAIAPI:
    def __init__(self, file):
        self.api_token = 'sk-proj-nQ5XPSZ1Kw3QkhpCs5HZT3BlbkFJk7t51cB6sWKGiDhMvps5'
        self.api_url = ' https://api.openai.com/v1/audio/transcriptions'
        self.file = file
        self.api_answer = None
        self.proxies = {
            'http': 'http://194.34.232.76:8800',
            'https': 'http://194.34.232.76:8800'
        }

    def create_headers(self, api_token):
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        return headers

    def create_data(self):
        data = {"model": "whisper-1"}
        return data

    def create_file(self, file):
        return {'file': open(file, 'rb')}

    def request(self):
        return requests.post(self.api_url, headers=self.create_headers(self.api_token), data=self.create_data(),
                             files=self.create_file(self.file), proxies=self.proxies).text

