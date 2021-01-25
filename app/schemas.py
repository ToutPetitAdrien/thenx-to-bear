from marshmallow import Schema, fields

class ExerciseSchema(Schema):
    title = fields.Str()
    quantity = fields.Str()

class RoundSchema(Schema):
    title = fields.Str()
    exercises = fields.List(fields.Nested(ExerciseSchema))

class WorkoutSchema(Schema):
    title = fields.Str()
    rounds = fields.List(fields.Nested(RoundSchema))

class WeekSchema(Schema):
    title = fields.Str()
    workouts = fields.List(fields.Str())

class ProgramSchema(Schema):
    title = fields.Str()
    weeks = fields.List(fields.Nested(WeekSchema))

class TemplateSchema(Schema):
    workout_url = fields.Str()
    week_name = fields.Str()
    program_name = fields.Str()