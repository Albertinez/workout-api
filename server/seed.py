from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    print("Resetting database...")

    db.drop_all()
    db.create_all()

    # =====================================================
    # EXERCISES
    # =====================================================
    pushups = Exercise(name="Push Ups", category="Strength", equipment_needed=False)
    squats = Exercise(name="Squats", category="Strength", equipment_needed=False)
    running = Exercise(name="Running", category="Cardio", equipment_needed=False)

    # =====================================================
    # WORKOUTS
    # =====================================================
    workout1 = Workout(date="2026-04-10", duration_minutes=45, notes="Leg day")
    workout2 = Workout(date="2026-04-11", duration_minutes=30, notes="Cardio day")

    # =====================================================
    # JOIN TABLE ENTRIES
    # =====================================================
    we1 = WorkoutExercise(workout=workout1, exercise=pushups, reps=15, sets=3)
    we2 = WorkoutExercise(workout=workout1, exercise=squats, reps=12, sets=4)
    we3 = WorkoutExercise(workout=workout2, exercise=running, duration_seconds=600)

    # =====================================================
    # SAVE TO DB
    # =====================================================
    db.session.add_all([
        pushups, squats, running,
        workout1, workout2,
        we1, we2, we3
    ])

    db.session.commit()

    print("Database seeded successfully!")