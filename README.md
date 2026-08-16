# Smart Internship Management System (SIMS)

A modern, responsive full-stack web application designed to centralize internship processes. Students can search/apply for roles, companies can post/review postings, and administrators can monitor system integrity.

## Core Architecture & Design

SIMS is built with a modular **MVC (Model-View-Controller)** pattern using Python Flask for routes and logic, Bootstrap 5 for visual elements, and a Snowflake-ready connection layer with a local SQLite fallback database.

- **Frontend**: HTML5, CSS3, Bootstrap 5, Javascript
- **Backend**: Python Flask (Modular Blueprints and Controllers)
- **Database**: Snowflake (with fallback SQLite `database.db`)
- **Aesthetics**: Premium Blue & White themed responsive user interfaces with dynamic sidebars, metrics counters, and badge logs.

---

## Directory Structure

```
Smart-Internship-Management-System/
├── config/
│   └── settings.py          # Session keys, Snowflake credentials, fallback DB routes
├── database/
│   ├── connection.py        # Reusable Snowflake/SQLite connection & query wrapper
│   └── schema.sql           # Database schema definition script
├── models/
│   ├── student.py           # Student database interactions & password hashing
│   ├── company.py           # Company profile queries & listings management
│   ├── admin.py             # Administrator audits & statistics queries
│   ├── internship.py        # Postings publication & keyword searching
│   └── application.py       # Candidate submittals, status workflow & reviews
├── routes/
│   ├── auth.py              # Login/Register endpoints blueprints
│   ├── student.py           # Student portal dashboard & apply actions
│   ├── company.py           # Company portal postings & candidate screenings
│   └── admin.py             # System moderation dashboards
├── controllers/
│   ├── auth_controller.py   # Auth login validation, logout, session storage
│   ├── student_controller.py# Profiles, CV file uploads, matching scoring
│   ├── company_controller.py# Postings editing, applicant status decisions
│   └── admin_controller.py  # KPI calculations, Power BI embeds config
├── services/
│   ├── skill_analysis.py    # Python Skill Gap Analysis placeholder
│   ├── recommendation.py    # Match scoring internship recommendations engine
│   ├── verification.py      # UiPath Document Scanning RPA trigger placeholder
│   └── powerbi.py           # Power BI Embed token configuration details
├── static/
│   ├── css/
│   │   └── style.css        # Theme stylesheet (Inter typography, sidebars)
│   └── js/
│       └── main.js          # Forms verification & alerts fader hooks
├── templates/               # Jinja2 Layout files & portal dashboards
├── app.py                   # Flask server entrypoint script
├── requirements.txt         # Package dependencies file
└── README.md                # System execution guide documentation
```

---

## Setup & Running Instructions

### 1. Prerequisites
- Python 3.8+ installed.

### 2. Environment Setup
Create and activate a python virtual environment:
```bash
python -m venv venv
# On Windows PowerShell
.\venv\Scripts\Activate.ps1
# On Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Fallback Options
SIMS is built to run **out of the box** without complex cloud setup:
- **Snowflake Mode**: If you have an active Snowflake database, open [config/settings.py](file:///c:/Users/ASUS/OneDrive/Desktop/Smart-Internship-Management-System/config/settings.py) and input your credentials (`Account`, `Username`, `Password`, etc.). The connector will execute queries on your schema.
- **SQLite Fallback Mode (Default)**: If any Snowflake credentials are left empty, the database wrapper logs a warning and automatically instantiates a local SQLite file at `database/database.db`, executing DDL tables setup and seeding a default administrator account.

### 5. Seeding Details (Default Admin Account)
On initialization, a default administrator is seeded for evaluation:
- **Email**: `admin@sims.com`
- **Password**: `admin123`

### 6. Run the Application
Start the local web server:
```bash
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## Technical Features Implemented

1. **Dual-DB SQL Execution**: Positional placeholders mapped from `%s` (Snowflake pyformat) to `?` (SQLite qmark) dynamically in the query runner.
2. **Resume Scanning (UiPath RPA)**: CV uploads trigger a mock RPA robot verification that validates student records.
3. **Skill Gap Analytics**: Compares candidate skill CSV inputs directly against employer listings. Computes match scores and outputs tailored Coursera/Udemy training course suggestions.
4. **Power BI Report Slots**: Configured dashboard embeds inside admin panels with access tokens and url slots.
