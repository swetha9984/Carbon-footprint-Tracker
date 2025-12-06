# EcoTrack - Carbon Footprint Tracker

## Overview
EcoTrack is a Flask-based web application that helps users track their carbon footprint from daily activities. Users can calculate emissions from vehicle use and food consumption, earn badges for eco-friendly actions, and learn about UN Sustainable Development Goals related to climate action.

**Status**: ✅ Complete and ready for use  
**Last Updated**: October 29, 2025  
**Tech Stack**: Python 3.11, Flask, Bootstrap 5, Chart.js

## Features
- **Once-per-day login**: Username and password authentication with daily login restriction
- **Carbon emission calculator**: Track emissions from vehicles and food
- **Achievement system**: Earn 10 different badges for eco-friendly actions
- **Data visualization**: Interactive Chart.js scatter plots showing daily emissions
- **SDG education**: Learn about 4 UN Sustainable Development Goals
- **Eco-friendly design**: Green/white/beige color scheme with responsive layout

## Project Structure
```
EcoTrack/
├── app.py                 # Main Flask application
├── static/
│   ├── css/
│   │   └── style.css     # Eco-friendly styling
│   ├── js/
│   │   └── main.js       # Chart.js integration
│   └── images/           # Image assets (empty)
└── templates/
    ├── login.html        # One-time login page
    ├── dashboard.html    # Main dashboard with charts
    ├── calculate.html    # Emission calculator
    ├── badges.html       # Achievement system
    └── sdg.html          # SDG information page
```

## Emission Factors
### Vehicle Emissions (kg CO₂/km)
- Car: 0.192
- Bike: 0.082
- Bus: 0.105
- Train: 0.041
- Bicycle: 0.0

### Food Emissions (kg CO₂/day)
- Vegetarian: 1.7
- Non-Vegetarian: 3.3
- Vegan: 1.5

## Badge System
1. 🚴 Green Commuter (50 pts) - Used bus/train/bike >10 km
2. 🥗 Eco Eater (75 pts) - Chose vegetarian/vegan diet
3. 🌱 Carbon Conscious (100 pts) - Total emissions < 50 kg
4. 💧 Water Wise (80 pts) - Logged 3+ eco meals
5. 🌞 Solar Supporter (90 pts) - Used only non-fuel transport
6. 🌳 Tree Saver (110 pts) - Travel emissions < 30 kg
7. ♻️ Zero Waste Warrior (120 pts) - Logged 5+ eco-friendly actions
8. 💚 Climate Guardian (150 pts) - Earned 5 badges
9. 🌎 Sustainability Star (200 pts) - Earned all badges
10. 🔋 Eco Power User (250 pts) - Completed all forms of activity

## Environment Configuration
**Required Environment Variable:**
- `SESSION_SECRET`: Secure session key (automatically set in Replit)

## Data Storage
All data is stored in-memory without a database:
- **Session storage**: Emission data, badges, points stored in Flask sessions
- **Server-side tracking**: LOGIN_TRACKER dictionary tracks daily logins per username
- **No database required**: All data is in-memory
- **Session data**: Persists during user session, resets on logout
- **Login tracking**: Persists until server restart, automatically cleans old entries daily

## Recent Changes
- **Oct 29, 2025**: Updated to username/password login with once-per-day restriction
  - **Changed login system**: Now requires both username and password
  - **Once-per-day restriction**: Users can only log in once per day (not once per session)
  - **Server-side tracking**: LOGIN_TRACKER persists login dates across sessions
  - **Bypass prevention**: Restriction works even if user logs out and tries to log back in
  - **Automatic cleanup**: Old login entries removed daily to prevent memory buildup

- **Oct 29, 2025**: Initial implementation completed
  - Created all Flask routes and templates
  - Implemented session-based authentication
  - Added emission calculators for vehicles and food
  - Built 10-badge achievement system with points
  - Integrated Chart.js for data visualization
  - Added SDG information page
  - Implemented eco-friendly UI design
  - Fixed security: SESSION_SECRET now required (no hard-coded fallback)

## Running the Application
The application runs automatically on port 5000. Access it through the webview panel.

**Routes:**
- `/` - Redirects to login or dashboard
- `/login` - One-time session login
- `/dashboard` - Main dashboard with charts
- `/calculate` - Emission calculator
- `/badges` - View achievements
- `/sdg` - Learn about SDGs
- `/logout` - Clear session
- `/api/emissions-data` - JSON endpoint for chart data

## Development Notes
- Flask debug mode is enabled for development
- Server binds to 0.0.0.0:5000 for Replit compatibility
- Bootstrap 5 CDN used for styling
- Chart.js CDN used for visualizations
- Session management handles all state without database

## Security
- SESSION_SECRET environment variable enforced
- No hard-coded credentials
- Session-based authentication
- CSRF protection via Flask sessions

## Future Enhancements
Potential additions:
- Export emission reports as PDF/CSV
- Weekly/monthly trend comparisons
- Additional activity categories (electricity, waste, water)
- Personalized eco-tips based on patterns
- Social sharing features
