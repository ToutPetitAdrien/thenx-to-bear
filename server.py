from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

import requests
from os import getenv

from bs4 import BeautifulSoup

from fetch import get_dom_page
from fastapi.encoders import jsonable_encoder

from serializer import get_program_from_dom, get_workout_from_dom
from schemas import TemplateSchema

app = FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True

@app.get("/program/{id}")
def get_program(id: int):
    dom = get_dom_page(f"https://thenx.com/programs/{id}")
    program = get_program_from_dom(dom)
    json_program = jsonable_encoder(program)
    return json_program

@app.post("/workouts/")
def create_template(request: Request, template: TemplateSchema):
    dom = get_dom_page(template.workout_url)
    workout = get_workout_from_dom(dom)
    json_workout = jsonable_encoder(workout)
    json_workout_with_tag = {
        **json_workout,
        "week_name": template.week_name,
        "program_name": template.program_name,
        "request": request,
    }

    return templates.TemplateResponse("workout.html.jinja", json_workout_with_tag)

    # with requests.Session() as s:
    #     html_doc = s.get('https://thenx.com/sign_in')
    #     soup = BeautifulSoup(html_doc.text, 'html.parser')

    #     data = {
    #         'authenticity_token': soup.find('input').attrs["value"],
    #         'session[email]': getenv('THENX_EMAIL'),
    #         'session[password]': getenv('THENX_PASSWORD'),
    #         'commit': 'Login',
    #     }

    #     s.post("https://thenx.com/session", data=data)
    #     response = s.get(f"https://thenx.com/workouts/{id}")

    #     return templates.TemplateResponse("workout.html.jinja", {
    #         "request": request,
    #         "title": "Abs",
    #         "tag": "sport/thenx/intermediateprogram",
    #         "rounds": [{
    #             "title": "Warm Up",
    #             "repeat": 2,
    #             "exercises": [{
    #                 "title": "Low Plank to High Plank",
    #                 "quantity": "20 seconds",
    #             }, {
    #                 "title": "Half Burpees",
    #                 "quantity": "30 seconds",
    #             }, {
    #                 "title": "Jumping Jacks",
    #                 "quantity": "30 seconds",
    #             }]
    #         }, {
    #             "title": "Round 1",
    #             "repeat": 2,
    #             "exercises": [{
    #                 "title": "Low Plank to High Plank",
    #                 "quantity": "20 seconds",
    #             }, {
    #                 "title": "Half Burpees",
    #                 "quantity": "30 seconds",
    #             }, {
    #                 "title": "Jumping Jacks",
    #                 "quantity": "30 seconds",
    #             }]
    #         }, {
    #             "title": "Round 2",
    #             "repeat": 2,
    #             "exercises": [{
    #                 "title": "Low Plank to High Plank",
    #                 "quantity": "20 seconds",
    #             }, {
    #                 "title": "Half Burpees",
    #                 "quantity": "30 seconds",
    #             }, {
    #                 "title": "Jumping Jacks",
    #                 "quantity": "30 seconds",
    #             }]
    #         }]
    #     })
