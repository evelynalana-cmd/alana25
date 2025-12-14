 Week 7: Secure Authentication System

Student Name: Evelyn A Byanjeru
Student ID: M00995689
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform

Project Description
A command-line authentication system implementing secure password hashing.

Features
- Secure password hashing using bcrypt
- User registration with duplicate prevention
- User login with password verification
- Input validation
- File-based persistence

Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: users.txt (comma-separated values)
- Password Security: One-way hashing

 Week 8: Database Pipeline & CRUD Operations

 Summary

Successfully implemented a complete database layer with CRUD operations for all three domains of the Multi-Domain Intelligence Platform. This week focused on migrating legacy data, designing schemas, and ensuring reproducible data pipelines.


 Completed Tasks ✅

1. *Database Manager* – Implemented SQLite connection management (`db.py`)  
2. *Schema Design* – Created tables for users, incidents, datasets, and tickets (`schema.py`)  
3. *User Migration* – Migrated Week 7 users from text file to database (`migrate_users.py`)  
4. *CRUD Implementation* – Full Create, Read, Update, Delete operations for all domains  
5. *CSV Data Loading* – Loaded 270 records from CSV files using pandas  

Week 9 – Multi‑domain dashboards & reporting
- Pages:
- Home: Home.py (login/register with bcrypt)
- Incidents: pages/2_Incidents.py (filters, charts, raw table, CSV export)
- Tickets: pages/3_Tickets.py (filters, charts, raw table, CSV export)
- Architecture (MVC):
- Model: SQLite (intelligence_platform.db) with users, incidents, tickets
- Service layer: incident_service.py, ticket_service.py (CRUD and queries)
- View/controller: Streamlit pages with role checks and session state
- Authentication & roles:
- bcrypt: hashed passwords, verified on login
- Roles: Admin (full CRUD), Analyst (view + add), Viewer (read‑only)
- Session state: username, role, logged_in
- Analytics:
