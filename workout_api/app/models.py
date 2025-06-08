from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    body_part = db.Column(db.String(50))
    duration = db.Column(db.Integer)  # in minutes
    level = db.Column(db.String(20))
    equipment = db.Column(db.String(100))
    exercises = db.Column(db.Text)  # Store JSON string if needed

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'body_part': self.body_part,
            'duration': self.duration,
            'level': self.level,
            'equipment': self.equipment,
            'exercises': json.loads(self.exercises) if self.exercises else []
        }
