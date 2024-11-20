from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'course_management_project'

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '9865'  # Your MySQL password here
app.config['MYSQL_DB'] = 'course_management_db'  # Your course management database name here
mysql = MySQL(app)

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to display all available courses
@app.route('/courses')
def courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses")  # Query to fetch all courses
    courses_info = cur.fetchall()
    cur.close()
    return render_template('courses.html', courses=courses_info)

# Route to search courses by ID, Title, or Instructor
@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    if request.method == "POST":
        search_term = request.form['search_term']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM courses WHERE course_id LIKE %s OR title LIKE %s OR instructor LIKE %s"
        cur.execute(query, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        search_results = cur.fetchall()  # Fetch all matching results
        cur.close()
        return render_template('courses.html', courses=search_results)

# Route to insert a new course
@app.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == "POST":
        course_id = request.form['course_id']
        title = request.form['title']
        instructor = request.form['instructor']
        duration = request.form['duration']
        price = request.form['price']
        seats_available = request.form['seats_available']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO courses (course_id, title, instructor, duration, price, seats_available) VALUES (%s, %s, %s, %s, %s, %s)",
                    (course_id, title, instructor, duration, price, seats_available))
        mysql.connection.commit()
        cur.close()
        flash("Course added successfully!", "success")
        return redirect(url_for('courses'))

    return render_template('insert_course.html')

# Route to delete a course
@app.route('/delete/<string:course_id>', methods=['GET'])
def delete(course_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM courses WHERE course_id=%s", (course_id,))
    mysql.connection.commit()
    cur.close()
    flash("Course deleted successfully!", "success")
    return redirect(url_for('courses'))

# Route to edit course details (Display the Edit Form)
@app.route('/edit/<string:course_id>', methods=['GET'])
def edit(course_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses WHERE course_id=%s", (course_id,))
    course = cur.fetchone()  # Fetch the course details to edit
    cur.close()
    return render_template('edit_course.html', course=course)

# Route to handle the update of course details
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        instructor = request.form['instructor']
        duration = request.form['duration']
        price = request.form['price']
        seats_available = request.form['seats_available']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE courses SET title=%s, instructor=%s, duration=%s, price=%s, seats_available=%s WHERE course_id=%s",
                    (title, instructor, duration, price, seats_available, course_id))
        mysql.connection.commit()
        cur.close()
        flash("Course updated successfully!", "success")
        return redirect(url_for('courses'))

# Route to enroll a student in a course
@app.route('/enroll', methods=['POST', 'GET'])
def enroll():
    if request.method == "POST":
        student_id = request.form['student_id']
        course_id = request.form['course_id']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
        mysql.connection.commit()
        cur.close()
        flash("Student enrolled successfully!", "success")
        return redirect(url_for('courses'))

    return render_template('enroll_student.html')


if __name__ == "__main__":
    app.run(debug=True)
