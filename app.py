from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta
import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET')
if not app.secret_key:
    raise ValueError("SESSION_SECRET environment variable must be set")

LOGIN_TRACKER = {}

EMISSION_FACTORS = {
    'vehicle': {
        'Car': 0.192,
        'Bike': 0.082,
        'Bus': 0.105,
        'Train': 0.041,
        'Bicycle': 0.0
    },
    'food': {
        'Vegetarian': 1.7,
        'Non-Vegetarian': 3.3,
        'Vegan': 1.5
    }
}

BADGES = [
    {
        'id': 'green_commuter',
        'name': '🚴 Green Commuter',
        'description': 'Used bus/train/bike >10 km',
        'points': 50,
        'criteria': 'eco_transport_10km'
    },
    {
        'id': 'eco_eater',
        'name': '🥗 Eco Eater',
        'description': 'Chose vegetarian/vegan diet',
        'points': 75,
        'criteria': 'eco_diet'
    },
    {
        'id': 'carbon_conscious',
        'name': '🌱 Carbon Conscious',
        'description': 'Total emissions < 50 kg',
        'points': 100,
        'criteria': 'total_under_50'
    },
    {
        'id': 'water_wise',
        'name': '💧 Water Wise',
        'description': 'Logged 3+ eco meals',
        'points': 80,
        'criteria': 'eco_meals_3'
    },
    {
        'id': 'solar_supporter',
        'name': '🌞 Solar Supporter',
        'description': 'Used only non-fuel transport',
        'points': 90,
        'criteria': 'only_non_fuel'
    },
    {
        'id': 'tree_saver',
        'name': '🌳 Tree Saver',
        'description': 'Travel emissions < 30 kg',
        'points': 110,
        'criteria': 'travel_under_30'
    },
    {
        'id': 'zero_waste',
        'name': '♻️ Zero Waste Warrior',
        'description': 'Logged 5+ eco-friendly actions',
        'points': 120,
        'criteria': 'eco_actions_5'
    },
    {
        'id': 'climate_guardian',
        'name': '💚 Climate Guardian',
        'description': 'Earned 5 badges',
        'points': 150,
        'criteria': 'badges_5'
    },
    {
        'id': 'sustainability_star',
        'name': '🌎 Sustainability Star',
        'description': 'Earned all badges',
        'points': 200,
        'criteria': 'all_badges'
    },
    {
        'id': 'eco_power_user',
        'name': '🔋 Eco Power User',
        'description': 'Completed all forms of activity',
        'points': 250,
        'criteria': 'all_activities'
    }
]

def initialize_session():
    if 'emissions' not in session:
        session['emissions'] = []
    if 'total_co2' not in session:
        session['total_co2'] = 0.0
    if 'points' not in session:
        session['points'] = 0
    if 'earned_badges' not in session:
        session['earned_badges'] = []
    if 'eco_transport_count' not in session:
        session['eco_transport_count'] = 0
    if 'eco_transport_distance' not in session:
        session['eco_transport_distance'] = 0
    if 'eco_meals_count' not in session:
        session['eco_meals_count'] = 0
    if 'travel_emissions' not in session:
        session['travel_emissions'] = 0.0
    if 'only_non_fuel' not in session:
        session['only_non_fuel'] = True
    if 'eco_actions' not in session:
        session['eco_actions'] = 0
    if 'has_vehicle' not in session:
        session['has_vehicle'] = False
    if 'has_food' not in session:
        session['has_food'] = False

def check_and_award_badges():
    newly_earned = []
    
    for badge in BADGES:
        if badge['id'] in session['earned_badges']:
            continue
            
        earned = False
        criteria = badge['criteria']
        
        if criteria == 'eco_transport_10km':
            if session['eco_transport_distance'] > 10:
                earned = True
        elif criteria == 'eco_diet':
            if session['eco_meals_count'] > 0:
                earned = True
        elif criteria == 'total_under_50':
            if session['total_co2'] < 50:
                earned = True
        elif criteria == 'eco_meals_3':
            if session['eco_meals_count'] >= 3:
                earned = True
        elif criteria == 'only_non_fuel':
            if session['only_non_fuel'] and session['has_vehicle']:
                earned = True
        elif criteria == 'travel_under_30':
            if session['travel_emissions'] < 30 and session['has_vehicle']:
                earned = True
        elif criteria == 'eco_actions_5':
            if session['eco_actions'] >= 5:
                earned = True
        elif criteria == 'badges_5':
            if len(session['earned_badges']) >= 5:
                earned = True
        elif criteria == 'all_badges':
            if len(session['earned_badges']) >= 9:
                earned = True
        elif criteria == 'all_activities':
            if session['has_vehicle'] and session['has_food']:
                earned = True
                
        if earned:
            session['earned_badges'].append(badge['id'])
            session['points'] += badge['points']
            newly_earned.append(badge['name'])
    
    session.modified = True
    return newly_earned

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

def clean_old_logins():
    today = datetime.now().strftime('%Y-%m-%d')
    users_to_remove = [user for user, date in LOGIN_TRACKER.items() if date != today]
    for user in users_to_remove:
        del LOGIN_TRACKER[user]

@app.route('/login', methods=['GET', 'POST'])
def login():
    clean_old_logins()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', message="Please enter both username and password.")
        
        if username in LOGIN_TRACKER and LOGIN_TRACKER[username] == today:
            return render_template('login.html', message="You can only log in once per day. Please try again tomorrow.")
        
        LOGIN_TRACKER[username] = today
        
        session.clear()
        session['logged_in'] = True
        session['username'] = username
        session['password'] = password
        session['login_date'] = today
        initialize_session()
        return redirect(url_for('dashboard'))
    
    current_user = session.get('username')
    if current_user and current_user in LOGIN_TRACKER and LOGIN_TRACKER[current_user] == today:
        message = "You can only log in once per day. Please try again tomorrow."
    else:
        message = None
        
    return render_template('login.html', message=message)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template('dashboard.html',
                         username=session.get('username', 'User'),
                         total_co2=round(session['total_co2'], 2),
                         points=session['points'],
                         badge_count=len(session['earned_badges']))

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category = request.form.get('category')
        emission = 0
        description = ""
        
        if category == 'vehicle':
            vehicle_type = request.form.get('vehicle_type', 'Car')
            distance = float(request.form.get('distance', 0))
            
            emission = EMISSION_FACTORS['vehicle'][vehicle_type] * distance
            description = f"{vehicle_type} - {distance} km"
            
            session['travel_emissions'] += emission
            session['has_vehicle'] = True
            
            if vehicle_type in ['Bus', 'Train', 'Bicycle']:
                session['eco_transport_count'] += 1
                session['eco_transport_distance'] += distance
                session['eco_actions'] += 1
            
            if vehicle_type not in ['Bicycle', 'Train', 'Bus']:
                session['only_non_fuel'] = False
                
        elif category == 'food':
            diet_type = request.form.get('diet_type', 'Vegetarian')
            meals = int(request.form.get('meals', 0))
            
            emission = EMISSION_FACTORS['food'][diet_type] * (meals / 3)
            description = f"{diet_type} - {meals} meals/day"
            
            session['has_food'] = True
            
            if diet_type in ['Vegetarian', 'Vegan']:
                session['eco_meals_count'] += 1
                session['eco_actions'] += 1
        
        session['total_co2'] += emission
        
        emission_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'day': len(session['emissions']) + 1,
            'category': category,
            'description': description,
            'emission': round(emission, 2)
        }
        session['emissions'].append(emission_entry)
        
        newly_earned = check_and_award_badges()
        
        session.modified = True
        
        return render_template('calculate.html',
                             success=True,
                             emission=round(emission, 2),
                             newly_earned=newly_earned)
    
    return render_template('calculate.html')

@app.route('/badges')
def badges():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    earned_badge_ids = session['earned_badges']
    earned_badges_list = [b for b in BADGES if b['id'] in earned_badge_ids]
    locked_badges_list = [b for b in BADGES if b['id'] not in earned_badge_ids]
    
    total_possible_points = sum(b['points'] for b in BADGES)
    current_points = session['points']
    
    next_badge = None
    if locked_badges_list:
        locked_badges_sorted = sorted(locked_badges_list, key=lambda x: x['points'])
        next_badge = locked_badges_sorted[0]
    
    progress_percent = 0
    if next_badge:
        if len(earned_badges_list) > 0:
            last_earned_points = earned_badges_list[-1]['points'] if earned_badges_list else 0
            points_needed = next_badge['points']
            progress_in_range = current_points - sum(b['points'] for b in earned_badges_list[:-1]) if len(earned_badges_list) > 1 else current_points
            progress_percent = min(100, int((progress_in_range / points_needed) * 100))
        else:
            progress_percent = int((current_points / next_badge['points']) * 100)
    
    return render_template('badges.html',
                         earned_badges=earned_badges_list,
                         locked_badges=locked_badges_list,
                         points=current_points,
                         total_points=total_possible_points,
                         next_badge=next_badge,
                         progress_percent=progress_percent)

@app.route('/sdg')
def sdg():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    sdgs = [
        {
            'number': 7,
            'title': 'Affordable and Clean Energy',
            'description': 'Ensure access to affordable, reliable, sustainable and modern energy for all. By tracking vehicle emissions, we promote the use of clean transportation and renewable energy sources.',
            'color': '#FCC30B'
        },
        {
            'number': 11,
            'title': 'Sustainable Cities and Communities',
            'description': 'Make cities and human settlements inclusive, safe, resilient and sustainable. Reducing carbon emissions from daily commutes helps create greener, healthier urban environments.',
            'color': '#FD9D24'
        },
        {
            'number': 12,
            'title': 'Responsible Consumption and Production',
            'description': 'Ensure sustainable consumption and production patterns. By making conscious food choices and tracking our carbon footprint, we contribute to sustainable resource use.',
            'color': '#BF8B2E'
        },
        {
            'number': 13,
            'title': 'Climate Action',
            'description': 'Take urgent action to combat climate change and its impacts. Every carbon emission we reduce and track is a step towards fighting global climate change.',
            'color': '#3F7E44'
        }
    ]
    
    return render_template('sdg.html', sdgs=sdgs)

@app.route('/api/emissions-data')
def emissions_data():
    if not session.get('logged_in'):
        return jsonify([])
    
    return jsonify(session.get('emissions', []))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
