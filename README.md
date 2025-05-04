# ⚽ FIFA League App

This is a lightweight web app for managing a FIFA head-to-head league among friends. Built with **Django**, it tracks player scores, auto-generates fixtures, and displays a live league table and playoffs — just like real football leagues.

---

## 🔥 Features

- ✅ Player registration via Google Form CSV import  
- ✅ Auto-generated home & away fixtures  
- ✅ Live-updated league table with:
  - Games Played, Wins, Draws, Losses  
  - Goals For / Against, Goal Difference  
  - Points & Remaining Games  
- ✅ Player score submission form  
- ✅ Scrollable upcoming fixtures & recent results  
- ✅ Playoffs for top 4 (1 vs 4, 2 vs 3, then Final)  
- ✅ Admin-only Reset Tournament button  
- ✅ Mobile-friendly & clean UI  
- ✅ Rules section displayed on landing page  

---

## 🚀 How to Run Locally

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/fifa-league-app.git
   cd fifa-league-app

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

###3. Install dependencies
```bash
pip install -r requirements.txt
   
###4. Apply migrations
```bash
python manage.py migrate
   
###5. Import players (from Google Form CSV)
```bash
python manage.py import_players players_form.csv

###6. Generate fixtures
```bash
python manage.py shell
>>> from core.utils import generate_fixtures
>>> generate_fixtures()
>>> exit()
    
###7. Run the app
```bash
python manage.py runserver

###8. Open http://127.0.0.1:8000

### 🌐 Live Demo
Hosted on Heroku:
https://fifa-league-app-d8649c766f0d.herokuapp.com/

### 📂 Project Structure
```text
fifa_league/
├── core/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── landing.html
├── static/
│   └── css/
│       └── styles.css
├── manage.py
├── requirements.txt
├── Procfile
└── runtime.txt

### 🛠 Built With
-Django
-HTML5 + CSS3
-Deployed on Heroku

### 📜 License
This project is for private FIFA league use. Contact the author if you'd like to adapt it for public or commercial tournaments.
