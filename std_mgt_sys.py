import copy
import json
import pickle

# courses dictionary
courses = {'FC308': {'Ass 1': {'Grade': -1, 'weighting': 0.1},
                     'Ass 2': {'Grade': -1, 'weighting': 0.4},
                     'Exam': {'Grade': -1, 'weighting': 0.5}},
           'FC315': {'Ass 1': {'Grade': -1, 'weighting': 0.4},
                     'Ass 2': {'Grade': -1, 'weighting': 0.6}},
           'FC311': {'Ass 1': {'Grade': -1, 'weighting': 0.1},
                     'Ass 2': {'Grade': -1, 'weighting': 0.4},
                     'Exam': {'Grade': -1, 'weighting': 0.5}},
           'EXTPRJ': {'Ass 1': {'Grade': -1, 'weighting': 0.4},
                      'Ass 2': {'Grade': -1, 'weighting': 0.6}},
           'FC300': {'Ass 1': {'Grade': -1, 'weighting': 0.1},
                     'Ass 2': {'Grade': -1, 'weighting': 0.5},
                     'Presentation': {'Grade': -1, 'weighting': 0.4}}}

# dath path file format
data_path = 'data.txt'


# parse the data file and create a dictionary
def parse_data(filename):
    userdata = []
    # read the data file
    with open(filename, 'r') as file:
        for line in file.readlines():
            # user data
            user = {
                'User Name': line.split(",")[0],
                'Password': line.split(",")[1],
                'Name': line.split(",")[2],
                'Student': line.split(",")[3],
                'Courses': {}
            }
            # add the student to the courses dictionary
            userdata.append(user)
            for course_grades in line.split(",")[4:]:
                course, grades = course_grades.split('-', 1)
                grades = grades.split('|')
                assignments = {}
                # grade assignment list
                for grade in grades:
                    assignment, grade_value = grade.split(':')
                    assignments[assignment.strip()] = {
                        'Grade': int(grade_value),
                        'weighting': float(courses[course][assignment.strip()]['weighting'])
                    }
                # add the assignments to the course
                user['Courses'][course] = assignments
        # return the dictionary
        return userdata
    


# write the data to the file
def write_data(filename, users):
    with open(filename, 'w') as f:
        for i, user in enumerate(users):
            # write the user data to the file
            user_data = [users[i]['User Name'], users[i]['Password'],
                         users[i]['Name'], str(user['Student'])]
            for course, assignments in user['Courses'].items():
                # write the course data to the file
                grades = '|'.join(
                    [f"{assignment}:{grade['Grade']}" for assignment, grade in assignments.items()])
                user_data.append(f"{course}-{grades}")
            # write the user data to the file
            f.write(','.join(user_data) + '\n')


# read the data file
users = parse_data(data_path)


# Enter the new student name
def enterUser():
    while True:
        newCourse = {}
        newUser = copy.deepcopy(users[0])
        newUser['User Name'] = input('Enter user name: ')
        user_exists = False
        for user in users:
            if user['User Name'] == newUser['User Name']:
                user_exists = True
                break
        # if user_exists
        if user_exists:
            print('User already exists Please choose another user name')
            continue
        else:
            # password
            newUser['Password'] = input('Enter password: ')
            user_input = ''
            while user_input not in ['S', 'T']:
                user_input = input('(S)tudent/(T)utor?: ').upper()
                # if user_input not in ['S', 'T
                if user_input == 'S':
                    newUser['Student'] = True
                elif user_input == 'T':
                    newUser['Student'] = False
                else:
                    # Invalid input
                    print(
                        'Invalid input. Please enter either "S" for student or "T" for tutor.')
                    continue

            while True:
                # enter name
                try:
                    name = input('Enter name: ')
                    if len(name) < 3:
                        raise ValueError
                    newUser['Name'] = name
                    break
                # if name is not valid
                except ValueError:
                    print('Please enter a valid name with at least 3 characters.')
                    continue
            newUser['Courses'] = {}
            while True:
                course = input(
                    'Enter course title (Type \'end\' when finished): ')
                # if course is lower than end
                if course.lower() != 'end':
                    newCourse[course] = {}
                    while True:
                        # enter assessment
                        assessment = input(
                            'Enter assessment title (Type \'end\' when finished): ')
                        if assessment.lower() != 'end':
                            while True:
                                try:
                                    # enter grade
                                    grade = int(
                                        input('Enter grade for ' + assessment + ': '))
                                    break
                                # if grade is not valid
                                except ValueError:
                                    print('Please enter a valid number.')
                                    continue

                            while True:
                                try:
                                    # enter weighting
                                    weighting = float(
                                        input('Enter weighting for ' + assessment + ': '))
                                    break
                                # if weighting is not valid
                                except ValueError:
                                    print('Please enter a valid number.')
                                    continue
                            newCourse[course][assessment] = {
                                'Grade': grade, 'weighting': weighting}
                        else:
                            break
                else:
                    break

            # add new course
            newUser['Courses'] = newCourse
            users.append(newUser)
            write_data(data_path, users)
            print('User added successfully!')
            if input('Enter another user (y/n)? ').lower() == 'n':
                break


# Enter the new student name
def getUser(userName, users):
    user = {}
    userFound = False
    for u in users:
        if u['User Name'] == userName and u['Student']:
            user = u
            userFound = True
            break
    if not userFound:
        print(f"No student user found with user name '{userName}'")
    return user, userFound


# see courses and grades for a student
def seeCourses():
    while True:
        # enter user name
        userName = input(
            'Enter student user name (Type "end" when finished): ')
        if userName == 'end':
            break
        user, userFound = getUser(userName, users)
        if userFound:
            # Check if user has any courses
            courses = user['Courses']
            for course in courses:
                if course in courses:
                    print(f"Course: {course}")
                    for a in courses[course]:
                        # print out the assessment name, grade and weighting
                        print(
                            f"{a}: Grade={courses[course][a]['Grade']}, weighting={courses[course][a]['weighting']}")
                    score = 0
                    weight = 0
                    # calculate the weighted score
                    for a in courses[course]:
                        score += courses[course][a]['Grade'] * \
                            courses[course][a]['weighting']
                        weight += courses[course][a]['weighting']
                        weighted_score = score / weight
                    print(f"Accumulated score:{weighted_score}\n")

        else:
            print(f"{userName} is not a registered student.")


def addGrades():
    while True:
        print('Add Grades')
        # enter user name
        userName = input('Enter student user name: (or "end" to quit): ')
        if userName == 'end':
            break
        # get user and check if user exists
        user, userFound = getUser(userName, users)
        if userFound:
            # enter grades
            for c in user['Courses']:
                for a in user['Courses'][c]:
                    while True:
                        try:
                            # enter updated grade for assessment
                            print(f'enter grade for {a} on {c}: ', end='')
                            g = int(input())
                            break
                        # if grade is not valid
                        except ValueError:
                            print('Please enter a valid number.')
                            continue
                    user['Courses'][c][a]['Grade'] = g
            # write data to file
            write_data(data_path, users)
            print('Grades updated successfully!')
            print(user['Courses'])
        else:
            print('user not found')


# Login function
def login():
    attempts = 3
    while True:
        if attempts == 0:
            print('Maximum attempts reached. Program will now exit.')
            quit()
        userFound = False
        currentUser = {}
        # Get user input
        logName = input('Enter login name: ')
        logPass = input('Enter Login password: ')
        # Check if user exists
        for k, i in enumerate(users):
            if users[k]['User Name'] == logName and users[k]['Password'] == logPass:
                currentUser = users[k]
                userFound = True
                break
        # If user exists, break loop
        if userFound:
            break
        else:
            attempts -= 1
            print('Invalid username or password. Please try again. {attempts} attempts left.\n'.format(
                attempts=attempts))
    return currentUser


# Get students in a module
def get_students():
    module = input('Enter module code: ')
    students = []
    for user in users:
        # if user is student and module code is in user's courses
        if user['Student'] and module in user['Courses']:
            students.append(user['Name'])
    return students


# Student unger 40 grade
def get_students_under_40():
    students = []
    for user in users:
        if user['Student']:
            total = 0
            for course in user['Courses']:
                for assessment in user['Courses'][course]:
                    total += user['Courses'][course][assessment]['Grade']
            if total / len(user['Courses']) < 40:
                students.append(user['Name'])
    return students


# Student graded
def get_students_not_graded():
    students = []
    for user in users:
        # if user is student
        if user['Student']:
            ungraded_count = 0
            for course in user['Courses']:
                for assessment in user['Courses'][course]:
                    if user['Courses'][course][assessment]['Grade'] == -1:
                        ungraded_count += 1
                        break
            # if user has ungraded assessment
            if ungraded_count > 0:
                students.append(user['Name'])
    return students


# Display grade
def display_grade(current_user):
    if current_user['Student'] == "True":
        print('Displaying Grades:\n')
        user = current_user
        courses = user['Courses']
        for course in courses:
            print(f"Course: {course}")
            # print out the assessment name, grade and weighting
            for a in courses[course]:
                print(
                    f"{a}: Grade={courses[course][a]['Grade']}, weighting={courses[course][a]['weighting']}")
            score = 0
            weight = 0
            # calculate the weighted score
            for a in courses[course]:
                score += courses[course][a]['Grade'] * \
                    courses[course][a]['weighting']
                weight += courses[course][a]['weighting']
                weighted_score = score / weight
            print(f"Accumulated score:{weighted_score}\n")
    else:
        # If user is not a student
        print('Access denied. Only students are allowed to view grades.')


def logout():
    print('Logging out...')
    print('Goodbye!')
    quit()


while True:
    curUser = login()
    if curUser['Student'] == "True":
        while True:
            print()
            # Student Grade Menu
            print('---- Student Grade ----')
            print('''
            Press 1 to see your grades.
            Press 2 to Logout
            ''')
            choice = input()
            # See grades
            if choice == '1':
                display_grade(curUser)
            # Logout
            elif choice == '2':
                logout()
            

    else:
        while True:
            print()
            # Student Management System Menu
            print('---- Student Management System ----')
            print('''
            Press 1 to enter new student.
            Press 2 to see a students courses.
            Press 3 to show all users
            press 4 to add student grades
            press 5 to see Students on a specified module
            press 6 to see students under 40% grade average
            press 7 to show students not yet graded
            press 8 to Logout
            ''')
            choice = input()
            # Enter new student
            if choice == '1':
                enterUser()
            # See a students courses
            elif choice == '2':
                seeCourses()
            # Show all users
            elif choice == '3':
                print(json.dumps(users, indent=4))
            # Add student grades
            elif choice == '4':
                addGrades()
            # See students on a specified module
            elif choice == '5':
                print(get_students())
            # See students under 40% grade average
            elif choice == '6':
                print(get_students_under_40())
            # See students not yet graded
            elif choice == '7':
                # See students not yet graded
                print(get_students_not_graded())
            elif choice == '8':
                logout()
