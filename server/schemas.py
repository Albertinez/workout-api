from marshmallow import Schema, fields, validate

# =====================================================
# EXERCISE SCHEMA
# =====================================================
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()


# =====================================================
# WORKOUT EXERCISE SCHEMA
# =====================================================
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))


# =====================================================
# WORKOUT SCHEMA
# =====================================================
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Str(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str()

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True)