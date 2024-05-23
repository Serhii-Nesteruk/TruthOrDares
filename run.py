from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Додано секретний ключ для використання сесій
db = SQLAlchemy(app)
players = []
current_player_index = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

truths = [
    "What is your biggest fear?",
    "What is your most embarrassing moment?",
    "Have you ever lied to a friend?"
]

dares = [
    "Do 20 pushups.",
    "Sing a song loudly.",
    "Dance like a monkey for 1 minute."
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        players.append({'name': name, 'gender': gender})
        return render_template('register.html', players=players)
    return render_template('register.html', players=players)

@app.route('/start_game')
def start_game():
    return render_template('game.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/get_task', methods=['POST'])
def get_task():
    global current_player_index

    data = request.json
    task_type = data.get('taskType')
    
    if task_type == 'truth':
        task = random.choice(truths)
    elif task_type == 'dare':
        task = random.choice(dares)
    else:
        task = "Invalid task type."

    if players:
        player = players[current_player_index]
        player_name = player['name']
        current_player_index = (current_player_index + 1) % len(players)
    else:
        player_name = "No players registered"

    return jsonify({'task': task, 'player': player_name})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
