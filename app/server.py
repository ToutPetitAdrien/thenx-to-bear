from flask import Flask, request, abort, render_template, jsonify
from flask_cors import cross_origin
from loguru import logger

from app.fetch import get_dom_page
from app.serializer import get_program_from_dom, get_workout_from_dom
from app.schemas import ProgramSchema, WorkoutSchema, TemplateSchema
from app.auth import requires_auth, AuthError

APP = Flask(__name__)
template_schema = TemplateSchema()

@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@APP.route('/')
def hello_world():
    return 'Hello, World!!!'


@APP.route("/program/<int:id>")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def get_program(id: int):
    dom = get_dom_page(f"https://thenx.com/programs/{id}")
    program = get_program_from_dom(dom)
    json_program = ProgramSchema().dump(program)
    return json_program


@APP.route("/workouts", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
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