class Exercise:
    def __init__(self, title, quantity):
        self.title = title
        self.quantity = quantity

class Round:
    def __init__(self, title, exercises):
        self.title = title
        self.exercises = exercises

class Workout:
    def __init__(self, title, rounds):
        self.title = title
        self.rounds = rounds

class Week:
    def __init__(self, title, workouts):
        self.title = title
        self.workouts = workouts

class Program:
    def __init__(self, title, weeks):
        self.title = title
        self.weeks = weeks