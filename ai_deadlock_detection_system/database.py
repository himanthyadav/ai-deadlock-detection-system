from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ProcessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    processes = db.Column(db.String, nullable=False)
    resources = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    features = db.Column(db.String, nullable=False)
    probability = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
