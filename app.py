from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os
import google.generativeai as genai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' 

# Use absolute path for database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'tarist.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLE_API_KEY'] = 'AIzaSyDrYMou99aJ4wzkBDOGeqINwbcJcwTM624'

# Configure AI
genai.configure(api_key=app.config['GOOGLE_API_KEY'])

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route('/')
def home():
    return render_template('new 1.html')

@app.route('/explore')
def explore():
    return render_template('explore.html', experiences=experiences_data)

@app.route('/dashboard')
def dashboard():
    # Mock data for demonstration
    trips = [1] # Simulating one planned trip
    return render_template('dashboard.html', trips=trips)

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/about')
def about():
    return render_template('about.html')

# --- Data ---
experiences_data = [
    {
        "id": 1,
        "title": "From Stone to Sky: The Evolution of the Pyramids",
        "short_desc": "See the pyramids the way history intended.",
        "full_desc": "See the pyramids the way history intended. This experience walks you through Egypt’s pyramid-building journey in chronological order—from early step pyramids to the iconic giants of Giza—so you understand how and why these monuments evolved, not just what they look like.",
        "image": "pyramids_evolution.png",
        "duration": "4–6 hours",
        "price": "Contact for Price",
        "rating": "4.9 ★",
        "category": "History • Architecture",
        "location": "Saqqara → Dahshur → Giza Plateau",
        "focus_points": [
            {"icon": "📐", "title": "Architectural Evolution", "desc": "Trace the design shifts from step pyramids to the smooth-sided giants."},
            {"icon": "👑", "title": "Political & Religious", "desc": "Political and religious motivations behind each phase."},
            {"icon": "🏗️", "title": "Engineering", "desc": "Engineering breakthroughs and failures."},
            {"icon": "🏜️", "title": "Context", "desc": "Context beyond “the three pyramids”."}
        ]
    },
    {
        "id": 2,
        "title": "One Street, Three Faiths",
        "short_desc": "Experience centuries of coexistence in Old Cairo.",
        "full_desc": "In one compact area, experience centuries of coexistence. This walk through Old Cairo’s Religious Complex explores Islamic, Christian, and Jewish landmarks side by side—revealing how belief, culture, and daily life intersected in Cairo long before modern borders and labels.",
        "image": "rel_complex.png",
        "duration": "2–3 hours",
        "price": "Contact for Price",
        "rating": "4.8 ★",
        "category": "Culture • Religion",
        "location": "Old Cairo (Coptic Cairo)",
        "focus_points": [
            {"icon": "🤝", "title": "Coexistence", "desc": "Religious coexistence in Egyptian history."},
            {"icon": "✝️", "title": "Coptic Heritage", "desc": "Coptic Christianity and early churches."},
            {"icon": "✡️", "title": "Jewish History", "desc": "Jewish heritage in Cairo."},
            {"icon": "🕌", "title": "Islamic Rules", "desc": "Islamic rule and urban layering."}
        ]
    },
    {
        "id": 3,
        "title": "Breakfast on Wheels: Egypt’s Foul Ritual",
        "short_desc": "Foul isn’t just food—it’s a daily ritual.",
        "full_desc": "Foul isn’t just food—it’s a daily ritual. This experience takes you to a classic street cart where locals start their morning, showing how one humble dish became a national constant across class, neighborhood, and generation.",
        "image": "foul_cart.png",
        "duration": "30–45 mins",
        "price": "Contact for Price",
        "rating": "5.0 ★",
        "category": "Food • Street Culture",
        "location": "Local neighborhoods across Cairo",
        "focus_points": [
            {"icon": "🥘", "title": "Street Food", "desc": "Egyptian street food culture."},
            {"icon": "☕", "title": "Morning Rituals", "desc": "Social rituals around breakfast."},
            {"icon": "🍋", "title": "Ingredients", "desc": "Ingredients, preparation, and variations."},
            {"icon": "🥄", "title": "Eat Like a Local", "desc": "Eating like a local, respectfully."}
        ]
    },
    {
        "id": 4,
        "title": "Money Talks: Egypt’s History in Your Wallet",
        "short_desc": "Your cash is a hidden guidebook.",
        "full_desc": "Your cash is a hidden guidebook. This experience connects Egyptian banknotes to the real monuments printed on them, taking you from paper to place. You’ll visit the Sultan Hassan Mosque, Al-Rifa’i Mosque, and the Citadel of Saladin, uncovering why these landmarks were chosen to represent Egypt’s power, faith, and identity.",
        "image": "money_history.jpg",
        "duration": "3–4 hours",
        "price": "Contact for Price",
        "rating": "4.9 ★",
        "category": "Culture • Urban Exploration",
        "location": "Islamic Cairo & Citadel area",
        "focus_points": [
            {"icon": "💶", "title": "Symbolism", "desc": "Symbolism behind Egyptian currency design."},
            {"icon": "🕌", "title": "Power", "desc": "Mamluk and Ottoman architectural power."},
            {"icon": "🆔", "title": "Identity", "desc": "How nations curate identity through money."},
            {"icon": "🔗", "title": "Connections", "desc": "Linking everyday objects to historical sites."}
        ]
    }
]

@app.route('/experience/<int:id>')
def experience_details(id):
    experience = next((exp for exp in experiences_data if exp['id'] == id), None)
    if not experience:
        return redirect(url_for('explore'))
    return render_template('experience_details.html', experience=experience)

@app.route('/questionnaire')
@login_required 
def questionnaire():
    return render_template('questionnaire.html')

# --- Auth Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email') # or username
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('explore'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('signup'))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

        db.session.add(new_user)
        db.session.commit()
        
        # Log user in immediately after signup
        login_user(new_user)

        return redirect(url_for('questionnaire'))

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/api/auth/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify({
            'is_authenticated': True,
            'name': current_user.name,
            'trip_count': current_user.trip_count
        })
    return jsonify({'is_authenticated': False})

@app.route('/api/book_trip', methods=['POST'])
@login_required
def book_trip():
    current_user.trip_count += 1
    db.session.commit()
    return jsonify({
        'success': True,
        'trip_count': current_user.trip_count
    })

# --- AI Chat Route ---
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({'response': "I am currently overloaded with requests from other travelers. Please try again in a moment!"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
