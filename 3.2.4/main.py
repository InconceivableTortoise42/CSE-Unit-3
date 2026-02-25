from course import Course
from student import Student

math = Course("Algebra I")
language = Course("Spanish I")
science = Course("Earth Science")
history = Course("U.S. History I")
phys_ed = Course("Physical Education I")

# TODO: Add two more courses of your choosing

cse = Course("Computer Science Essentials")
jazz = Course("Jazz Band")

test_student = Student("Jill", "Sample")
test_student.add_course(math)
test_student.add_course(language)
test_student.add_course(science)
test_student.add_course(history)

test_student2 = Student("Bill", "Sample")
test_student2.add_course(math)
test_student2.add_course(phys_ed)
test_student2.add_course(science)
test_student2.add_course(history)

# TODO Add a third test student and assign them four classes

test_student3 = Student("John", "Smith")
test_student3.add_course(cse)
test_student3.add_course(jazz)
test_student3.add_course(math)
test_student3.add_course(history)

# TODO Add all the test students to a list of your own creation

students:list[Student] = [
    test_student,
    test_student2,
    test_student3
]

# TODO print student_list

for i, student in enumerate(students):
    print(f"{i + 1}. {student.get_full_name()}")

# TODO iterate over each of the students in the list and print their names and course schedules.
    # Each iteration should:
        # print the student

for student in students:
    print("-"*40)
    print(student.first_name, student.last_name)
    print("Courses:")
    for course in student.courses:
        print(f"  -  {course.course_name}")
    print("-"*40)
