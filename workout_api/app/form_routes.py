from flask import Blueprint, render_template, request, redirect, flash
from .models import db, Workout
import json

form_bp = Blueprint('form_bp', __name__)

@form_bp.route('/upload', methods=['GET', 'POST'])
def upload_workout():
    if request.method == 'POST':
        try:
            name = request.form['name']
            body_part = request.form['body_part']
            duration = int(request.form['duration'])
            level = request.form['level']
            equipment = request.form.get('equipment', '')

            # Build exercises list dynamically
            exercises = []
            i = 0
            while f'exercise_name_{i}' in request.form:
                exercises.append({
                    'name': request.form[f'exercise_name_{i}'],
                    'sets': int(request.form[f'exercise_sets_{i}']),
                    'reps': int(request.form[f'exercise_reps_{i}'])
                })
                i += 1

            new_workout = Workout(
                name=name,
                body_part=body_part,
                duration=duration,
                level=level,
                equipment=equipment,
                exercises=json.dumps(exercises)  # store as JSON in DB
            )

            db.session.add(new_workout)
            db.session.commit()
            flash('Workout added successfully!', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

        return redirect('/upload')

    return render_template('upload.html')



