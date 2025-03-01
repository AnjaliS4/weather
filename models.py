from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_city = db.Column(db.String(100))
    preferred_topic = db.Column(db.String(100))

    def __repr__(self):
        return f'<UserPreference {self.id}>'
