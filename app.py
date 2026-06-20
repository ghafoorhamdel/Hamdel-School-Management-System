from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_connection():
    return sqlite3.connect("school.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT,
        date_of_birth TEXT,
        grade TEXT,
        phone TEXT,
        email TEXT
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    subject TEXT,
    phone TEXT,
    email TEXT
)
""")
    conn.commit()
    conn.close()

@app.route("/")
def home():

    conn = get_connection()
    cursor = conn.cursor()

    # Count students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Count teachers
    cursor.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total_students=total_students,
        total_teachers=total_teachers,
        total_classes=0,
        attendance_percentage=0
    )

@app.route("/students")
def students():
    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("""
        SELECT id, first_name, last_name, grade, phone, email
        FROM students
        WHERE first_name LIKE ?
           OR last_name LIKE ?
           OR grade LIKE ?
           OR phone LIKE ?
           OR email LIKE ?
        ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
        SELECT id, first_name, last_name, grade, phone, email
        FROM students
        ORDER BY id DESC
        """)

    students = cursor.fetchall()
    conn.close()

    return render_template(
        "students.html",
        students=students,
        search=search
    )

@app.route("/add_student", methods=["POST"])
def add_student():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (first_name, last_name, gender, date_of_birth, grade, phone, email)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form["first_name"],
        request.form["last_name"],
        request.form["gender"],
        request.form["date_of_birth"],
        request.form["grade"],
        request.form["phone"],
        request.form["email"]
    ))

    conn.commit()
    conn.close()

    return redirect("/students")

@app.route("/edit_student/<int:id>")
def edit_student(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("edit_student.html", student=student)

@app.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET first_name = ?,
        last_name = ?,
        gender = ?,
        date_of_birth = ?,
        grade = ?,
        phone = ?,
        email = ?
    WHERE id = ?
    """, (
        request.form["first_name"],
        request.form["last_name"],
        request.form["gender"],
        request.form["date_of_birth"],
        request.form["grade"],
        request.form["phone"],
        request.form["email"],
        id
    ))

    conn.commit()
    conn.close()

    return redirect("/students")

@app.route("/delete_student/<int:id>")
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/students")
@app.route("/teachers")
def teachers():
    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("""
        SELECT id, first_name, last_name, subject, phone, email
        FROM teachers
        WHERE first_name LIKE ?
           OR last_name LIKE ?
           OR subject LIKE ?
           OR phone LIKE ?
           OR email LIKE ?
        ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))
    else:
        cursor.execute("""
        SELECT id, first_name, last_name, subject, phone, email
        FROM teachers
        ORDER BY id DESC
        """)

    teachers = cursor.fetchall()
    conn.close()

    return render_template("teachers.html", teachers=teachers, search=search)

@app.route("/add_teacher", methods=["POST"])
def add_teacher():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO teachers
    (first_name, last_name, gender, subject, phone, email)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        request.form["first_name"],
        request.form["last_name"],
        request.form["gender"],
        request.form["subject"],
        request.form["phone"],
        request.form["email"]
    ))

    conn.commit()
    conn.close()

    return redirect("/teachers")

@app.route("/delete_teacher/<int:id>")
def delete_teacher(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teachers WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/teachers")
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)