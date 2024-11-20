-- Create Database for the Course Management System
CREATE DATABASE course_management_db;

-- Use the newly created database
USE course_management_db;

-- Table to store courses
CREATE TABLE courses (
    course_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    instructor VARCHAR(255) NOT NULL,
    duration VARCHAR(100),
    price DECIMAL(10, 2),
    seats_available INT
);


-- Table to store students
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(15)
);

-- Table to store enrollments (Many-to-Many relationship between students and courses)
CREATE TABLE enrollments (
    student_id VARCHAR(10),
    course_id VARCHAR(10),
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
-- Inserting sample courses
INSERT INTO courses (course_id, title, instructor, duration, price, seats_available)
VALUES
('CS101', 'Introduction to Computer Science', 'Dr. Smith', '3 months', 100.00, 50),
('MATH101', 'Calculus I', 'Prof. Johnson', '4 months', 150.00, 30),
('ENG201', 'English Literature', 'Dr. Brown', '6 months', 120.00, 25);

-- Inserting sample students
INSERT INTO students (student_id, name, email, phone)
VALUES
('S001', 'John Doe', 'john.doe@example.com', '123-456-7890'),
('S002', 'Jane Smith', 'jane.smith@example.com', '987-654-3210'),
('S003', 'Bob Brown', 'bob.brown@example.com', '555-555-5555');

-- Inserting sample enrollments
INSERT INTO enrollments (student_id, course_id)
VALUES
('S001', 'CS101'),
('S002', 'MATH101'),
('S003', 'ENG201');

select * from courses;
select * from students;
select * from enrollments;