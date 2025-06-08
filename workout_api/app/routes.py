from flask import Blueprint, request, jsonify, redirect
from .models import db, Workout
import json


workout_bp = Blueprint('workout_bp', __name__)

@workout_bp.route('/', methods=['GET'])
def get_all_workouts():
    workouts = Workout.query.all()
    return jsonify([{
        'id': w.id,
        'name': w.name,
        'body_part': w.body_part,
        'duration': w.duration,
        'level': w.level,
        'equipment': w.equipment,
        'exercises': json.loads(w.exercises) if w.exercises else []
    } for w in workouts])

@workout_bp.route('/', methods=['POST'])
def add_workout():
    data = request.get_json()
    new_workout = Workout(
        name=data['name'],
        body_part=data['body_part'],
        duration=data['duration'],
        level=data['level'],
        equipment=data.get('equipment', ''),
        exercises=json.dumps(data.get('exercises', []))
    )
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': 'Workout added successfully'}), 201

@workout_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if workout:
        return {
            'id': workout.id,
            'name': workout.name,
            'body_part': workout.body_part,
            'duration': workout.duration,
            'level': workout.level,
            'equipment': workout.equipment,
            'exercises': json.loads(workout.exercises) if workout.exercises else []
        }
    else:
        return {'error': 'Workout not found'}, 404
    
@workout_bp.route('/api/workouts/search')
def search_workouts():
    body_part = request.args.get('body_part')
    level = request.args.get('level')

    if not body_part or not level:
        return jsonify({'error': 'Missing body_part or level'}), 400

    workout = Workout.query.filter_by(body_part=body_part, level=level).first()

    if workout:
        return jsonify(workout.to_dict())
    else:
        return jsonify({'message': 'No workout found.'}), 404
    
@workout_bp.route('/register')
def go_to_upload():
    return redirect("http://127.0.0.1:5001/register")