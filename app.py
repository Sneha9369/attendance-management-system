from flask import Flask, jsonify, render_template, request, redirect, session, flash
import sqlite3, os, random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

conn = sqlite3.connect("ams.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
role TEXT
)
""")

# STUDENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
student_id TEXT,
name TEXT,
course TEXT,
department TEXT,
section TEXT,
username TEXT UNIQUE,
photo TEXT,
father_name TEXT,
mother_name TEXT,
contact TEXT,
address TEXT
)
""")



# TEACHERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
teacher_id TEXT,
name TEXT,
course TEXT,
department TEXT,
subjects TEXT,
father_name TEXT,
mother_name TEXT,
contact TEXT,
address TEXT,
city TEXT,
state TEXT,
photo TEXT,
username TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_id TEXT,
subject TEXT,
date TEXT,
status TEXT
)
""")

conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
    student_id TEXT,
    subject TEXT,
    marks INTEGER
)
""")

conn.commit()



cursor.execute(
"INSERT INTO attendance (student_id, subject, date, status) VALUES (?,?,?,?)",
("TEST1", "ML", "2026-04-18", "Present")
)
conn.commit()

# 🔥 TABLE CREATE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
role TEXT
)
""")

cursor.execute("UPDATE students SET department='Data Science' WHERE department='DS'")
cursor.execute("UPDATE students SET department='Computer Science' WHERE department='CSE'")
cursor.execute("UPDATE students SET department='Artificial Intelligence' WHERE department='AI'")

conn.commit()

print("Departments Updated ✅")


#  (ALTER TABLE CODE)
try:
    cursor.execute("ALTER TABLE students ADD COLUMN father_name TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE students ADD COLUMN mother_name TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE students ADD COLUMN contact TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE students ADD COLUMN address TEXT")
except:
    pass

conn.commit()

# 🔥 ADMIN AUTO INSERT 
cursor.execute("INSERT OR IGNORE INTO users VALUES ('admin','admin123','admin')")
conn.commit()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())
# ================= HOME =================
@app.route('/')
def home():
    return render_template("login.html")

# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    password = request.form.get('password')

    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()

    if user:
        session['username'] = username
        session['role'] = user[2]

        flash("Login Successful ✅", "success")

        if user[2] == "admin":
            return redirect('/admin_dashboard')
        elif user[2] == "teacher":
            return redirect('/teacher_dashboard')
        else:
            return redirect('/student_dashboard')

    else:
        flash("Invalid Credentials ❌", "error")
        return redirect('/')
    
#=============REGISTER=======================
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        try:
            cursor.execute(
                "INSERT INTO users VALUES (?,?,?)",
                (username, password, role)
            )
            conn.commit()

            flash("Registered Successfully ✅", "success")
            return redirect('/')

        except:
            flash("Username already exists ❌", "error")
            return redirect('/register')

    return render_template("register.html")

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ================= ADMIN =================
@app.route('/admin_dashboard')
def admin_dashboard():
    students = cursor.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    teachers = cursor.execute("SELECT COUNT(*) FROM teachers").fetchone()[0]
    return render_template("admin_dashboard.html", students=students, teachers=teachers)


#================== Profile============
@app.route('/my_profile')
def my_profile():

    username = session.get('username')

    student = cursor.execute(
        "SELECT * FROM students WHERE username=?",
        (username,)
    ).fetchone()

    return render_template("profile.html", student=student)

# ================= ADD TEACHER =================
@app.route('/add_teacher', methods=['POST'])
def add_teacher():

    id = request.form.get("id")
    name = request.form.get("name")
    course = request.form.get("course")
    dept = request.form.get("department")

    subjects = request.form.getlist("subjects")
    subjects = ", ".join(subjects)

    father = request.form.get("father_name")
    mother = request.form.get("mother_name")

    contact = request.form.get("contact")
    address = request.form.get("address")

    # 
    print("CONTACT:", contact)
    print("ADDRESS:", address)

    city = request.form.get("city")
    state = request.form.get("state")
    username = request.form.get("username")

    file = request.files["photo"]
    photo = file.filename
    file.save("static/uploads/" + photo)

    cursor.execute("""
    INSERT INTO teachers
    (teacher_id, name, course, department, subjects, father_name, mother_name, contact, address, city, state, photo, username)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (id, name, course, dept, subjects, father, mother, contact, address, city, state, photo, username))

    conn.commit()

    return redirect('/view_teachers')
#============TEACHER DASHBOARD=============
@app.route('/teacher_dashboard')
def teacher_dashboard():

    if session.get('role') != 'teacher':
        return redirect('/')

    username = session.get('username')

    teacher = cursor.execute(
        "SELECT * FROM teachers WHERE username=?",
        (username,)
    ).fetchone()

    return render_template("teacher_dashboard.html", teacher=teacher)

#============= TEACHER PROFILE===========


@app.route('/teacher_profile')
def teacher_profile():

    username = session.get('username')

    teacher = cursor.execute(
        "SELECT * FROM teachers WHERE username=?",
        (username,)
    ).fetchone()

    return render_template("teacher_profile.html", t=teacher)



#==============EDIT TEACHER======================
@app.route('/edit_teacher/<id>')
def edit_teacher(id):
    teacher = cursor.execute(
        "SELECT * FROM teachers WHERE teacher_id=?",
        (id,)
    ).fetchone()

    return render_template("edit_teacher.html", teacher=teacher)


@app.route('/update_teacher', methods=['POST'])
def update_teacher():

    cursor.execute("""
    UPDATE teachers
    SET name=?, department=?, subjects=?, contact=?, city=?, state=?
    WHERE teacher_id=?
    """, (
        request.form.get('name'),
        request.form.get('department'),
        request.form.get('subjects'),
        request.form.get('contact'),
        request.form.get('city'),
        request.form.get('state'),
        request.form.get('teacher_id')
    ))

    conn.commit()
    return redirect('/view_teachers')

# ================= VIEW TEACHERS =================
@app.route('/view_teachers')
def view_teachers():
    data = cursor.execute("SELECT * FROM teachers").fetchall()
    return render_template("view_teachers.html", data=data)

# ================= DELETE TEACHER =================
@app.route('/delete_teacher/<id>')
def delete_teacher(id):
    cursor.execute("DELETE FROM teachers WHERE teacher_id=?", (id,))
    conn.commit()
    return redirect('/view_teachers')

# ================= ADD STUDENT =================
import random

@app.route('/add_student', methods=['POST'])
def add_student():

    name = request.form.get('name')
    course = request.form.get('course')
    dept = request.form.get('department')

    father = request.form.get('father_name')
    mother = request.form.get('mother_name')
    contact = request.form.get('contact')
    address = request.form.get('address')

    username = request.form.get('username')
    password = request.form.get('password')

    photo = request.files['photo']
    filename = photo.filename
    photo.save("static/uploads/" + filename)

    student_id = "ST" + str(random.randint(1000,9999))

    # 🔥 students table insert
    cursor.execute("""
    INSERT INTO students
    (student_id, name, course, department, username, photo, father_name, mother_name, contact, address)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    """, (student_id, name, course, dept, username, filename, father, mother, contact, address))

    # 🔥 users table insert (login ke liye)
    cursor.execute(
        "INSERT INTO users VALUES (?,?,?)",
        (username, password, "student")
    )

    conn.commit()

    flash("Student Added Successfully ✅", "success")
    return redirect('/add_student_page')

@app.route('/add_student_page')
def add_student_page():
    return render_template("add_student.html")
# ================= VIEW STUDENTS =================
@app.route('/view_students')
def view_students():

    course = request.args.get('course')
    dept = request.args.get('dept')

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if course and course != "All":
        query += " AND course=?"
        params.append(course)

    if dept and dept != "All":
        query += " AND department=?"
        params.append(dept)

    data = cursor.execute(query, params).fetchall()

    return render_template("view_students.html", data=data)
# ================STUDENT PROFILE =================
@app.route('/profile/<id>')
def profile(id):
    student = cursor.execute(
        "SELECT * FROM students WHERE student_id=?",
        (id,)
    ).fetchone()

    if not student:
        return "❌ Student not found"

    return render_template("profile.html", student=student)

# ================DELETE STUDENT=================
@app.route('/delete_student/<id>')
def delete_student(id):
    cursor.execute("DELETE FROM students WHERE student_id=?", (id,))
    conn.commit()

    flash("🗑 Student Deleted Successfully", "success")
    return redirect('/view_students')

# ================EDIT STUDENT=================
@app.route('/edit_student/<id>')
def edit_student(id):
    student = cursor.execute(
        "SELECT * FROM students WHERE student_id=?",
        (id,)
    ).fetchone()

    return render_template("edit_student.html", student=student)

# ================UPDATE STUDENT=================
@app.route('/update_student', methods=['POST'])
def update_student():

    cursor.execute("""
    UPDATE students
    SET name=?, course=?, department=?, section=?,
        father_name=?, mother_name=?, contact=?, address=?
    WHERE student_id=?
    """, (
        request.form.get('name'),
        request.form.get('course'),
        request.form.get('department'),
        request.form.get('section'),
        request.form.get('father_name'),
        request.form.get('mother_name'),
        request.form.get('contact'),
        request.form.get('address'),
        request.form.get('student_id')
    ))

    conn.commit()
    return redirect('/view_students')

#=============STUDENT DASHBOARD=================

import random   # 🔥 file के सबसे ऊपर (once only)

@app.route('/student_dashboard')
def student_dashboard():

    if 'username' not in session:
        return redirect('/')

    username = session.get('username')

    student = cursor.execute(
        "SELECT * FROM students WHERE username=?",
        (username,)
    ).fetchone()

    if not student:
        return "Student not found ❌"

    student_id = student[0]

    attendance = cursor.execute(
        "SELECT subject, date, status FROM attendance WHERE student_id=?",
        (student_id,)
    ).fetchall()

    # 🔥 QUOTES (function के अंदर ही)
    quotes = [
        "Success doesn’t come to you, you go to it 🚀",
        "Push yourself, because no one else will 💪",
        "Dream big. Start small. Act now ✨",
        "Consistency is the key to success 🔑",
        "Don’t stop until you’re proud 😎",
        "Small progress is still progress 📈",
        "Your future is created by what you do today 🔥",
        "Stay focused and never give up 🎯",
        "Hard work beats talent 💯",
        "Believe in yourself 👊"
    ]

    random_quote = random.choice(quotes)

    return render_template(
        "student_dashboard.html",
        student=student,
        attendance=attendance,
        quote=random_quote   # 🔥 IMPORTANT
    )

#=================ADD MARKS=================
@app.route('/add_marks', methods=['GET', 'POST'])
def add_marks():

    course = request.args.get('course')
    dept = request.args.get('dept')

    students = []

    if course and dept:
        students = cursor.execute(
            "SELECT student_id, name FROM students WHERE course=? AND department=?",
            (course, dept)
        ).fetchall()

    return render_template(
        "add_marks.html",
        students=students,
        course=course,
        dept=dept
    )

#================ MANUAL ATTENDANCE==========
@app.route('/manual_attendance')
@app.route('/manual_attendance')
def manual_attendance():

    course = request.args.get('course')
    department = request.args.get('department')

    students = []

    if course and department:
        students = cursor.execute(
            "SELECT student_id, name FROM students WHERE course=? AND department=?",
            (course, department)
        ).fetchall()

    return render_template("manual_attendance.html", students=students)
#SAVE ATTENDANCE

@app.route('/save_manual_attendance', methods=['POST'])
def save_manual_attendance():

    date = request.form.get('date')
    subject = request.form.get('subject')
    course = request.form.get('course')
    dept = request.form.get('department')

    present = request.form.getlist('present')

    students = cursor.execute(
        "SELECT student_id FROM students WHERE course=? AND department=?",
        (course, dept)
    ).fetchall()

    for s in students:
        status = "Present" if str(s[0]) in present else "Absent"

        cursor.execute(
            "INSERT INTO attendance (student_id, subject, date, status) VALUES (?,?,?,?)",
            (s[0], subject, date, status)
        )

    conn.commit()

    flash("Attendance Saved ✅", "success")
    return redirect('/manual_attendance')
    print("FORM:", request.form)
    print("PRESENT:", request.form.getlist('present'))

#=========MY ATTENDANCE%=================
@app.route('/my_attendance')
def my_attendance():

    if 'username' not in session:
        return redirect('/')

    username = session.get('username')

    student = cursor.execute(
        "SELECT * FROM students WHERE username=?",
        (username,)
    ).fetchone()

    student_id = student[0]

    # 
    data = cursor.execute("""
    SELECT subject,
           COUNT(*) as total,
           SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present
    FROM attendance
    WHERE student_id=?
    GROUP BY subject
    """, (student_id,)).fetchall()

    return render_template("my_attendance.html", data=data)



#=================MARKS==========

@app.route('/my_marks')
def my_marks():
    username = session.get('username')

    student = cursor.execute(
        "SELECT student_id FROM students WHERE username=?",
        (username,)
    ).fetchone()

    if not student:
        flash("Student not found ❌", "error")
        return redirect('/student_dashboard')

    student_id = student[0]

    data = cursor.execute(
        "SELECT subject, marks FROM marks WHERE student_id=?",
        (student_id,)
    ).fetchall()

    return render_template("marks.html", data=data)

#SAVE MARKS
@app.route('/save_marks', methods=['POST'])
def save_marks():

    subject = request.form.get('subject')

    for key in request.form:
        if key.startswith("marks_"):
            student_id = key.split("_")[1]
            marks = request.form.get(key)

            cursor.execute(
                "INSERT INTO marks (student_id, subject, marks) VALUES (?,?,?)",
                (student_id, subject, marks)
            )

    conn.commit()

    flash("Marks Saved ✅", "success")
    return redirect('/add_marks')

#==============REPORT===================

@app.route('/report')
def report():

    course = request.args.get('course')
    dept = request.args.get('dept')

    query = "SELECT student_id, name, course, department FROM students WHERE 1=1"
    params = []

    if course and course != "All":
        query += " AND course=?"
        params.append(course)

    if dept and dept != "All":
        query += " AND department=?"
        params.append(dept)

    students = cursor.execute(query, params).fetchall()

    report_data = []

    for s in students:

        student_id = s[0]

        total = cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id=?",
            (student_id,)
        ).fetchone()[0]

        present = cursor.execute(
            "SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",
            (student_id,)
        ).fetchone()[0]

        percent = 0
        if total > 0:
            percent = round((present / total) * 100, 2)

        report_data.append((
            s[0],   # id
            s[1],   # name
            s[2],   # course
            s[3],   # dept
            percent
        ))

    return render_template("report.html", data=report_data)
#=============== CHANGE PASSWORD==============

@app.route('/change_password_page')
def change_password_page():
    return render_template("change_password.html")

@app.route('/change_password', methods=['POST'])
def change_password():

    username = session.get('username')
    old = request.form.get('old_password')
    new = request.form.get('new_password')

    user = cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, old)
    ).fetchone()

    if not user:
        return "❌ Wrong Old Password"

    cursor.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new, username)
    )

    conn.commit()

    return "✅ Password Updated"

#================ PERFORMANCE GRAPH===============
@app.route('/student_graph')
def student_graph():

    username = session.get('username')

    student = cursor.execute(
        "SELECT student_id FROM students WHERE username=?",
        (username,)
    ).fetchone()

    if not student:
        return render_template("graph.html", subjects=[], marks=[])

    student_id = student[0]

    rows = cursor.execute(
        "SELECT subject, marks FROM marks WHERE student_id=?",
        (student_id,)
    ).fetchall()

    subjects = []
    marks = []

    for r in rows:
        subjects.append(str(r[0]) if r[0] else "")

        try:
            m = int(r[1])
        except:
            m = 0

        # 🔥 ensure out of 100
        if m > 100:
            m = 100
        if m < 0:
            m = 0

        marks.append(m)

    return render_template("graph.html", subjects=subjects, marks=marks)
# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)

print(cursor.execute("SELECT * FROM attendance").fetchall())

from flask import jsonify

@app.route('/get_students')
def get_students():

    course = request.args.get('course')
    dept = request.args.get('dept')

    print("REQ:", course, dept)

    students = cursor.execute(
        "SELECT student_id, name FROM students WHERE course=? AND department=?",
        (course, dept)
    ).fetchall()

    print("RESULT:", students)

    return jsonify([{"id": s[0], "name": s[1]} for s in students])
print("ATTENDANCE DATA:", cursor.execute("SELECT * FROM attendance").fetchall())

print(cursor.execute("SELECT DISTINCT course, department FROM students").fetchall())

print(cursor.execute("SELECT student_id, name, course, department FROM students").fetchall())

print(cursor.execute("SELECT * FROM teachers").fetchall())

subjects = request.form.getlist("subjects")   # list
subjects = ", ".join(subjects)                # string

subjects_list = request.form.getlist("subjects")  
subjects = ", ".join(subjects_list)              
print("SUBJECTS LIST:", subjects_list)
print("SUBJECTS STRING:", subjects)

