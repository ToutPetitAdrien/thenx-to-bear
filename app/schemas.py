from dataclasses import dataclass, field

from pydantic import BaseModel

class ExerciseSchema(BaseModel):
    title: str
    quantity: str

class RoundSchema(BaseModel):
    title: str
    exercises: list[ExerciseSchema]

class WorkoutSchema(BaseModel):
    title: str
    rounds: list[RoundSchema]

class WeekSchema(BaseModel):
    title: str
    workouts: list[str]

class ProgramSchema(BaseModel):
    title: str
    weeks: list[WeekSchema]

class TemplateSchema(BaseModel):
    workout_url: str
    week_name: str
    program_name: str

