from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

import requests
from os import getenv

from bs4 import BeautifulSoup

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/workout/{id}", response_class=PlainTextResponse)
def read_workout(request: Request, id: str):
    with requests.Session() as s:
        html_doc = s.get('https://thenx.com/sign_in')
        soup = BeautifulSoup(html_doc.text, 'html.parser')

        data = {
            'authenticity_token': soup.find('input').attrs["value"],
            'session[email]': getenv('THENX_EMAIL'),
            'session[password]': getenv('THENX_PASSWORD'),
            'commit': 'Login',
        }

        s.post("https://thenx.com/session", data=data)
        response = s.get(f"https://thenx.com/workouts/{id}")

        return response.content
