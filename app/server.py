from flask import Flask, request, abort, render_template
from loguru import logger

from app.fetch import get_dom_page
from app.serializer import get_program_from_dom, get_workout_from_dom
from app.schemas import ProgramSchema, WorkoutSchema, TemplateSchema

app = Flask(__name__)
template_schema = TemplateSchema()

@app.route('/')
def hello_world():
    return 'Hello, World!!'

@app.route("/program/<int:id>")
def get_program(id: int):
    dom = get_dom_page(f"https://thenx.com/programs/{id}")
    program = get_program_from_dom(dom)
    json_program = ProgramSchema().dump(program)
    return json_program


@app.route("/workouts", methods=['POST'])
def create_template():
    errors = template_schema.validate(request.form)
    if errors:
        abort(400, errors)
    dom = get_dom_page(request.form['workout_url'])
    workout = get_workout_from_dom(dom)
    json_workout = WorkoutSchema().dump(workout)
    json_workout_with_tag = {
        **json_workout,
        "week_name": request.form['week_name'].replace(" ", ""),
        "program_name": request.form['program_name'].replace(" ", ""),
    }

    return render_template(
        "workout.html.jinja",
        **json_workout_with_tag
    )