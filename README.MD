# 🎓 Attendance Management System (AMS)

<p align="center">
  <b>A Smart Web-Based System to Manage Attendance, Marks & Student Performance</b>
</p>

---

## 📌 Overview

The **Attendance Management System (AMS)** is a Flask-based web application designed to simplify and digitize academic record management.  

It provides separate dashboards for **Admin, Teacher, and Student**, enabling efficient handling of attendance, marks, and performance analysis.

---

## ✨ Key Features

- 🔐 Role-based Login System (Admin / Teacher / Student)
- 📅 Attendance Tracking System
- 📊 Marks & Performance Management
- 🧑‍🏫 Teacher Subject Handling
- 📁 Image Upload Support
- 📈 Student Dashboard with Insights
- 🔎 Search & Report System

---

## 🏗️ System Modules

### 👨‍💼 Admin Panel
- Manage Students & Teachers
- View Reports
- Control System Data

### 👩‍🏫 Teacher Panel
- Take Attendance
- Add Marks
- View Students

### 🎓 Student Panel
- View Attendance %
- Check Marks
- Track Performance

---

## ⚙️ Tech Stack

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

---

## 📂 Project Structure

AMS/
│
├── app.py
├── database.py
├── train.py
├── recognize.py
├── register.py
├── README.md
├── .gitignore
│
├── static/
│ ├── style.css
│ ├── login.png
│ ├── screenshots/
│ │ ├── admin_dashboard.png
│ │ ├── student_dashboard.png
│ │ ├── teacher_dashboard.png
│ │ ├── report.png
│ │ └── manual_attendance.png
│ └── uploads/ (ignored)
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── student_dashboard.html
│ ├── teacher_dashboard.html
│ ├── admin_dashboard.html
│ ├── my_attendance.html
│ ├── marks.html
│ └── ...
│
├── attendance/
│ └── attendance.csv
│
└── dataset/


---

## 📸 Screenshots

### 🔹 Admin Dashboard
![Admin](static/screenshots/admin_dashboard.png)

### 🔹 Student Dashboard
![Student](static/screenshots/student_dashboard.png)

### 🔹 Teacher Dashboard
![Teacher](static/screenshots/teacher_dashboard.png)

### 🔹 Attendance System
![Attendance](static/screenshots/manual_attendance.png)

### 🔹 Reports
![Report](static/screenshots/report.png)

---

## 🚀 How to Run

```bash
# Clone repo
git clone https://github.com/Sneha9369/attendance-management-system.git
cd attendance-management-system

# Install dependencies
pip install flask

# Create database
python database.py

# Run app
python app.py
