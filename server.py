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
        "week_name": template.week_name.replace(" ", ""),
        "program_name": template.program_name.replace(" ", ""),
        "request": request,
    }

    return templates.TemplateResponse("workout.html.jinja", json_workout_with_tag)
