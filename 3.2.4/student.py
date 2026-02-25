from course import Course
import json

class Student:
    
    student_id = 0
    
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.courses:list[Course] = []
        self.student_id = Student.student_id
        Student.student_id += 1
    
    def __str__(self):
        # Calling "print(student)"" from main.py will call this method instead
        # TODO You will need to use a variable in the loop, so you must intialize it here,

        student:dict = {
            "name": self.first_name,
            "lastname": self.last_name,
            "studentId": self.student_id,
            "courses": []
        }

        # that variable will need to be initalized to get items listed in the first def _init_ section
        # TODO add a loop that will go through the course list
            # TODO Add code here to create a string representation of a student,
            # including first and last name and all courses that student is taking
        for course in self.courses:
            student["courses"] = student["courses"] + [course.course_name]

        return json.dumps(student)
        
    def get_first_name(self):
        return self.first_name
        
    def get_last_name(self):
        return self.last_name
        
    def get_student_id(self):
        return self.student_id
    
    def add_course(self, new_course):
        # TODO add code to append new_course to self.courses
        self.courses.append(new_course)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"