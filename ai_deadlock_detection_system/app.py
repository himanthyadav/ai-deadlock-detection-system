import os
import pkgutil
import importlib.util
from flask import Flask, render_template, request, jsonify

# Compatibility shim: Python versions where `pkgutil.get_loader` is removed
# (or not present) cause Flask internals to fail; provide a simple fallback.
if not hasattr(pkgutil, 'get_loader'):
    def _get_loader(name):
        try:
            spec = importlib.util.find_spec(name)
            return spec.loader if spec is not None else None
        except Exception:
            return None
    pkgutil.get_loader = _get_loader
from dotenv import load_dotenv
from database import db, ProcessLog, PredictionLog
from deadlock_detector import DeadlockDetector
from ml_model import DeadlockMLModel

load_dotenv()

detector = DeadlockDetector()
model = DeadlockMLModel()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///deadlock.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/detect', methods=['POST'])
    def detect_deadlock():
        data = request.json
        graph = data.get('graph', {})
        is_deadlock = detector.detect_deadlock_wfg(graph)
        log = ProcessLog(processes=str(graph), resources='-', result=str(is_deadlock))
        db.session.add(log)
        db.session.commit()
        return jsonify({'deadlock': is_deadlock})

    @app.route('/predict', methods=['POST'])
    def predict_deadlock():
        f = request.json.get('features', [])
        prob, cls = model.predict(f)
        log = PredictionLog(features=str(f), probability=prob, prediction=str(cls))
        db.session.add(log)
        db.session.commit()
        return jsonify({'probability': prob, 'prediction': int(cls)})

    @app.route('/dashboard')
    def dashboard():
        logs = ProcessLog.query.order_by(ProcessLog.created_at.desc()).limit(200).all()
        preds = PredictionLog.query.order_by(PredictionLog.created_at.desc()).limit(200).all()
        return render_template('dashboard.html', logs=logs, preds=preds)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
