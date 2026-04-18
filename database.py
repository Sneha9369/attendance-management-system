import sqlite3

conn = sqlite3.connect("ams.db", check_same_thread=False)
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
username TEXT PRIMARY KEY,
password TEXT,
role TEXT
)
""")

# STUDENTS
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    student_id TEXT,
    name TEXT,
    course TEXT,
    department TEXT,
    username TEXT UNIQUE,
    photo TEXT,
    father_name TEXT,
    mother_name TEXT,
    contact TEXT,
    address TEXT
)
""")

# TEACHERS
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


# ATTENDANCE
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT,
    subject TEXT,
    date TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(
    student_id TEXT,
    subject TEXT,
    marks INTEGER
)
""")

# MASTER TABLES
cursor.execute("CREATE TABLE IF NOT EXISTS courses(name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS departments(name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS subjects(name TEXT)")

conn.commit()

