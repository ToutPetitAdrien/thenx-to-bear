from bs4 import BeautifulSoup

from schemas import ProgramSchema, WeekSchema, WorkoutSchema, RoundSchema, ExerciseSchema

def get_program_from_dom(dom: str) -> ProgramSchema:
    soup = BeautifulSoup(dom, 'html.parser')
    all_dom_weeks = soup.select('.card')
    weeks = []
    title = soup.find('h3').string
    for dom_week in all_dom_weeks:
        weeks.append(WeekSchema(
            title=dom_week.find('h5').string,
            workouts=['https://thenx.com' + workout.get('href') for workout in dom_week.find_all('a')],
        ))
    return ProgramSchema(title=title, weeks=weeks)


def get_workout_from_dom(dom: str) -> WorkoutSchema:
    soup = BeautifulSoup(dom, 'html.parser')
    all_dom_rounds = soup.select('.card')
    rounds = []
    for dom_round in all_dom_rounds:
        dom_exercises = dom_round.find_all('a')
        exercises = []
        for dom_exercise in dom_exercises:
            exercises.append(ExerciseSchema(
                title=dom_exercise.find('h6').string,
                quantity=dom_exercise.find('p').string
            ))
        rounds.append(RoundSchema(
            title=dom_round.find('h5').string,
            exercises=exercises,
        ))
    return WorkoutSchema(
        title=soup.find('h3').string,
        rounds=rounds,
    )


