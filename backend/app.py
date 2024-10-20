from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import bcrypt
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    members = db.relationship('User', secondary='group_membership', backref='groups')

class GroupMembership(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        token = jwt.encode({
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/api/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    return jsonify({'message': f'Welcome to your dashboard, {current_user.email}!'}), 200

@app.route('/api/groups', methods=['GET'])
@token_required
def get_groups(current_user):
    groups = Group.query.all()
    return jsonify({'groups': [{'id': g.id, 'name': g.name} for g in groups]}), 200

@app.route('/api/groups', methods=['POST'])
@token_required
def create_group(current_user):
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Group name is required'}), 400
    new_group = Group(name=name)
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Group created successfully', 'group': {'id': new_group.id, 'name': new_group.name}}), 201

@app.route('/api/workouts', methods=['POST'])
@token_required
def create_workout(current_user):
    data = request.json
    workout_type = data.get('type')
    duration = data.get('duration')
    calories = data.get('calories')
    
    if not all([workout_type, duration, calories]):
        return jsonify({'error': 'Type, duration, and calories are required'}), 400
    
    new_workout = Workout(user_id=current_user.id, type=workout_type, duration=duration, calories=calories)
    db.session.add(new_workout)
    db.session.commit()
    
    return jsonify({'message': 'Workout logged successfully'}), 201

@app.route('/api/workouts', methods=['GET'])
@token_required
def get_workouts(current_user):
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return jsonify({'workouts': [{'id': w.id, 'type': w.type, 'duration': w.duration, 'calories': w.calories, 'date': w.date} for w in workouts]}), 200

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    # In a real-world scenario, you might want to invalidate the token on the server-side
    # For this example, we'll just return a success message
    return jsonify({'message': 'Logged out successfully'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)