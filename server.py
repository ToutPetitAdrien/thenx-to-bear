from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

import requests
from os import getenv

from bs4 import BeautifulSoup

app = FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True

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

        return templates.TemplateResponse("workout.html.jinja", {
            "request": request,
            "title": "Abs",
            "tag": "sport/thenx/intermediateprogram",
            "rounds": [{
                "title": "Warm Up",
                "repeat": 2,
                "exercises": [{
                    "title": "Low Plank to High Plank",
                    "quantity": "20 seconds",
                }, {
                    "title": "Half Burpees",
                    "quantity": "30 seconds",
                }, {
                    "title": "Jumping Jacks",
                    "quantity": "30 seconds",
                }]
            }, {
                "title": "Round 1",
                "repeat": 2,
                "exercises": [{
                    "title": "Low Plank to High Plank",
                    "quantity": "20 seconds",
                }, {
                    "title": "Half Burpees",
                    "quantity": "30 seconds",
                }, {
                    "title": "Jumping Jacks",
                    "quantity": "30 seconds",
                }]
            }, {
                "title": "Round 2",
                "repeat": 2,
                "exercises": [{
                    "title": "Low Plank to High Plank",
                    "quantity": "20 seconds",
                }, {
                    "title": "Half Burpees",
                    "quantity": "30 seconds",
                }, {
                    "title": "Jumping Jacks",
                    "quantity": "30 seconds",
                }]
            }]
        })
