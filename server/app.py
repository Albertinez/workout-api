from flask import Flask, request
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema

app = Flask(__name__)

# -------------------
# CONFIG
# -------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# -------------------
# SCHEMAS
# -------------------
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

# -------------------
# HOME ROUTE
# -------------------
@app.route('/')
def home():
    return {"message": "Workout API running"}

# =====================================================
# WORKOUT ROUTES
# =====================================================

# GET all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200


# GET single workout
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout), 200


# CREATE workout
@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.json

    errors = workout_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    workout = Workout(
        date=data['date'],
        duration_minutes=data['duration_minutes'],
        notes=data.get('notes')
    )

    db.session.add(workout)
    db.session.commit()

    return workout_schema.dump(workout), 201


# DELETE workout
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)

    db.session.delete(workout)
    db.session.commit()

    return {"message": "Workout deleted"}, 200


# =====================================================
# EXERCISE ROUTES
# =====================================================

# GET all exercises
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200


# GET single exercise
@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_schema.dump(exercise), 200


# CREATE exercise
@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.json

    errors = exercise_schema.validate(data)
    if errors:
        return {"errors": errors}, 400

    exercise = Exercise(
        name=data['name'],
        category=data['category'],
        equipment_needed=data.get('equipment_needed', False)
    )

    db.session.add(exercise)
    db.session.commit()

    return exercise_schema.dump(exercise), 201


# DELETE exercise
@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)

    db.session.delete(exercise)
    db.session.commit()

    return {"message": "Exercise deleted"}, 200


# =====================================================
# JOIN TABLE ROUTE
# =====================================================

# ADD exercise to workout
@app.route('/workouts/<int:wid>/exercises/<int:eid>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(wid, eid):
    data = request.json

    workout = Workout.query.get_or_404(wid)
    exercise = Exercise.query.get_or_404(eid)

    we = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds')
    )

    db.session.add(we)
    db.session.commit()

    return {
        "message": "Exercise added to workout"
    }, 201


# -------------------
# RUN SERVER
# -------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)