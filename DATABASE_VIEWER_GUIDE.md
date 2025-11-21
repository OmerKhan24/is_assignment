# 🔍 How to View SQLite Database

## Hospital Management System Database Guide

Your database is SQLite (not MySQL), so XAMPP won't work. Here are several ways to view your database:

---

## Method 1: Using Our Custom Database Viewer (Easiest) ✅

Run the included Python script:

```powershell
python view_database.py
```

This will show an interactive menu to:
- View all tables
- View specific tables (users, patients, logs, etc.)
- Run custom SQL queries
- Export data

**Interactive Menu:**
```
1. View All Tables
2. View Users Table
3. View Patients Table
4. View Logs Table
5. View GDPR Consent Table
6. Run Custom Query
7. Exit
```

---

## Method 2: DB Browser for SQLite (Recommended GUI) ⭐

**Download:** https://sqlitebrowser.org/dl/

### Steps:
1. Download and install DB Browser for SQLite
2. Open the application
3. Click "Open Database"
4. Navigate to: `F:\FAST-WORK\Seventh_SEM\is\Assignment_04\`
5. Select `hospital.db`
6. Browse tables, run queries, export data

**Features:**
- ✅ Visual table browser
- ✅ SQL query editor
- ✅ Data editing
- ✅ Export to CSV/JSON/SQL
- ✅ Schema viewer
- ✅ Free and open source

---

## Method 3: VS Code SQLite Extension

**Install Extension:** "SQLite" by alexcvzz

### Steps:
1. Open VS Code
2. Press `Ctrl+Shift+X` (Extensions)
3. Search for "SQLite"
4. Install "SQLite" by alexcvzz
5. Press `Ctrl+Shift+P`
6. Type "SQLite: Open Database"
7. Select `hospital.db`
8. View tables in the Explorer panel

**Features:**
- ✅ Built into VS Code
- ✅ Quick queries
- ✅ Table browsing
- ✅ Export data

---

## Method 4: Command Line SQLite

Open PowerShell in your project folder:

```powershell
# If you have SQLite installed
sqlite3 hospital.db

# Inside SQLite shell:
.tables                    # List all tables
.schema users             # View users table structure
SELECT * FROM users;      # View all users
SELECT * FROM patients;   # View all patients
SELECT * FROM logs;       # View all logs
.exit                     # Exit SQLite
```

**Install SQLite CLI:**
- Download from: https://www.sqlite.org/download.html
- Or use: `choco install sqlite` (if you have Chocolatey)

---

## Method 5: Online SQLite Viewer

**Website:** https://sqliteviewer.app/ or https://inloop.github.io/sqlite-viewer/

### Steps:
1. Go to the website
2. Click "Choose File"
3. Upload your `hospital.db` file
4. Browse tables and data in browser

**⚠️ Note:** Only use trusted sites for sensitive data

---

## Method 6: Python Script (Quick View)

Create a quick Python script:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('hospital.db')

# View users
print("\n=== USERS ===")
print(pd.read_sql_query("SELECT * FROM users", conn))

# View patients
print("\n=== PATIENTS ===")
print(pd.read_sql_query("SELECT * FROM patients", conn))

# View logs
print("\n=== LOGS ===")
print(pd.read_sql_query("SELECT * FROM logs", conn))

conn.close()
```

---

## Method 7: Streamlit App Database Tab (In Your App)

I can add a database viewer tab in your Streamlit app!

---

## Quick Commands Reference

### View All Tables:
```sql
SELECT name FROM sqlite_master WHERE type='table';
```

### View Users:
```sql
SELECT user_id, username, role FROM users;
```

### View Patients:
```sql
SELECT patient_id, name, contact, diagnosis, 
       anonymized_name, anonymized_contact, is_anonymized 
FROM patients;
```

### View Recent Logs:
```sql
SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10;
```

### View GDPR Consents:
```sql
SELECT * FROM gdpr_consent;
```

### Count Records:
```sql
SELECT 
  (SELECT COUNT(*) FROM users) as users_count,
  (SELECT COUNT(*) FROM patients) as patients_count,
  (SELECT COUNT(*) FROM logs) as logs_count;
```

---

## Database Location

Your database file is located at:
```
F:\FAST-WORK\Seventh_SEM\is\Assignment_04\hospital.db
```

---

## XAMPP Alternative (If You Want MySQL Instead)

If you prefer MySQL (for XAMPP), I can create a MySQL version:

1. Install XAMPP
2. Start Apache + MySQL
3. Create database in phpMyAdmin
4. I'll modify the code to use MySQL instead of SQLite

**Pros of SQLite (current):**
- ✅ No installation needed
- ✅ Single file database
- ✅ Portable
- ✅ Fast for small apps
- ✅ Perfect for assignments

**Pros of MySQL:**
- ✅ Better for large data
- ✅ Multi-user access
- ✅ phpMyAdmin interface
- ✅ Industry standard

---

## Recommended Approach for Assignment

**For quick viewing:** Use `python view_database.py`

**For detailed exploration:** Install DB Browser for SQLite

**For your report screenshots:** Use DB Browser or Streamlit app

---

## Need MySQL Version?

Let me know if you want me to:
1. ✅ Convert to MySQL/MariaDB (for XAMPP)
2. ✅ Keep SQLite but add Streamlit database viewer tab
3. ✅ Both options

---

## Current Database Schema

```
hospital.db
├── users (3 default users)
│   ├── user_id (PK)
│   ├── username
│   ├── password (hashed)
│   └── role
│
├── patients
│   ├── patient_id (PK)
│   ├── name (raw)
│   ├── contact (raw)
│   ├── diagnosis (raw)
│   ├── anonymized_name
│   ├── anonymized_contact
│   ├── date_added
│   └── is_anonymized
│
├── logs (audit trail)
│   ├── log_id (PK)
│   ├── user_id (FK)
│   ├── username
│   ├── role
│   ├── action
│   ├── timestamp
│   └── details
│
└── gdpr_consent
    ├── consent_id (PK)
    ├── patient_id (FK)
    ├── consent_given
    ├── consent_date
    └── data_retention_days
```

---

**Quick Answer:** Run `python view_database.py` for instant database viewing! 🚀
