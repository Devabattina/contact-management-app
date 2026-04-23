# Contact Management Application

## Demo Video
[Watch Demo](https://drive.google.com/file/d/112-toZZ0Pbmnd2Y0Qq_Eh4TcV6B5N-Ad/view?usp=drive_link)

## Overview
This is a web-based Contact Management Application built using Flask, SQLAlchemy, and MySQL. It allows users to perform CRUD operations (Create, Read, Update, Delete) on contact data.

## Features
- Add new contacts
- View all contacts
- Update existing contacts
- Delete contacts
- Backend validation for name, email, and phone number
- Unique constraint for email and phone

## Tech Stack
- Backend: Python (Flask)
- ORM: SQLAlchemy
- Database: MySQL
- Frontend: HTML, Bootstrap

## How to Run

### Prerequisites
- Python installed
- MySQL installed

### Steps

1. Install dependencies:

pip install -r requirements.txt

2. Create database in MySQL:

CREATE DATABASE contact_app;

3. Update database credentials in `app.py` if required

4. Run the application:

python app.py

5. Open in browser:

http://127.0.0.1:5000/


## Challenges Faced
- Faced schema mismatch issues when updating the model without updating the database
- Handled validation at both input and database levels
- Managed database connection configuration and special characters in credentials

## Future Improvements
- Add search functionality
- Implement pagination
- Use Flask-Migrate for database migrations

## Author
Anjani Devabattina