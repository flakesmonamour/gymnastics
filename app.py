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
def groups(current_user):
    return jsonify({'groups': ['Group 1', 'Group 2', 'Group 3']}), 200

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