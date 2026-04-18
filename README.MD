# 🎓 Attendance Management System (AMS)

## 📌 Introduction

The Attendance Management System (AMS) is a web-based application developed using Flask (Python) that helps educational institutions manage student attendance, marks, and performance efficiently. The system provides separate dashboards for Admin, Teacher, and Student roles.

This project aims to digitize traditional attendance systems and provide real-time insights into student performance.

---

## 🎯 Objectives

- Automate attendance tracking
- Provide subject-wise attendance insights
- Allow teachers to manage student marks
- Enable students to view performance and attendance
- Maintain organized academic records

---

## 🏗️ System Modules

### 👨‍💼 Admin Panel
- Add/Edit/Delete Students
- Add/Edit/Delete Teachers
- View Reports
- Manage Attendance

### 👩‍🏫 Teacher Panel
- Take Attendance
- Add Marks
- View Students
- Manage Subjects

### 🎓 Student Panel
- View Attendance %
- View Marks
- Performance Dashboard
- Personal Profile

---

## ⚙️ Technologies Used

| Technology | Description |
|----------|------------|
| Python | Backend logic |
| Flask | Web framework |
| SQLite | Database |
| HTML/CSS | Frontend |
| JavaScript | Dynamic UI |

---

## 🗄️ Database Structure

The system uses SQLite database with the following tables:

- `students`
- `teachers`
- `attendance`
- `marks`

Database is automatically created using `database.py`.

---

## 🚀 How to Run the Project

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

#=============== IMPORTANT===============
“Run database.py before running app.py”

2️⃣ Install Dependencies
pip install flask
3️⃣ Create Database
python database.py
4️⃣ Run Application
python app.py

2️⃣ Install Dependencies
pip install flask
3️⃣ Create Database
python database.py
4️⃣ Run Application
python app.py