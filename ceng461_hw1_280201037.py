import sys
class Course:
    def __init__(self, course_id, instructor, students, hours):
        self.course_id = course_id
        self.instructor = instructor
        self.students = int(students)
        self.hours = int(hours)
        self.coordination = []

instructors = {}
classrooms_capacity = {}
courses = []

schedule = {}
assigned_times_classrooms = {}
assigned_times_instructors = {}
assigned_times_courses = {}



def read_file(file_path):
    file_contents = []
    if file_path.endswith("preferences.csv"):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                split1 = line.strip().split(",")
                file_contents.append(split1[0])
                split2 = split1[1].split(" ")
                file_contents.append(split2)
    elif file_path.endswith("coordinations.csv"):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                split1 = line.strip().split(" ")
                file_contents.append(split1)
    else:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                split1 = line.strip().split(",")
                file_contents.append(split1)
    return file_contents

def create_solution_file(sol_path, solutions):
    sol_number = 0
    for schedule in solutions:
        file_path = sol_path+"/" +str(sol_number+1) + ".csv"
        with open(file_path, "w", newline="") as file:
            file.write("Course, Time, Classroom \n")
            for k, v in schedule.items():
                schedule_data = k+", "+v[0]+", "+v[1]+"\n"
                file.write(schedule_data)
            sol_number += 1
        


def capacity_compliance(course, classroom):
    return course.students <= classrooms_capacity[classroom]

def consecutive_scheduling(course,start):
    instructor = course.instructor
    instructor_preferences = instructors[instructor]
    for hour in range(0,course.hours):
        time_slot = instructor_preferences[start + hour]
        if hour > 0:
            previous_time_slot = instructor_preferences[start + hour - 1] 
            if previous_time_slot and previous_time_slot[-1]=="4" and time_slot[-1]=="5":
                return False  
            elif previous_time_slot and previous_time_slot[0:3] != time_slot[0:3]:
                return False
    return True

def instructor_preferences_compliance(course,start):
    is_prefered = False
    instructor = course.instructor
    instructor_preferences = instructors[instructor]

    for hour in range(0,course.hours):
        time_slot = instructor_preferences[start + hour]
        for preference in instructor_preferences:
            if preference == time_slot:
                is_prefered = True
    return is_prefered

def coordination_restrictions(course,start):
    instructor = course.instructor
    instructor_preferences = instructors[instructor]
    for hour in range(0,course.hours):
        time_slot = instructor_preferences[start + hour]
        for coordinated_course in course.coordination:
            for assigned_time_slot in assigned_times_courses[coordinated_course]:
                if time_slot == assigned_time_slot:
                    return False
    return True
            
def exclusive_classroom_assignment(course,start,classroom):
    instructor = course.instructor
    instructor_preferences = instructors[instructor]
    for hour in range(0,course.hours):
        time_slot = instructor_preferences[start + hour]
        for assigned_time_slot in assigned_times_classrooms[classroom]:
            if time_slot == assigned_time_slot:
                return False
    return True
        
def instructor_avaliability(course,start):
    instructor = course.instructor
    instructor_preferences = instructors[instructor]
    for hour in range(0,course.hours):
        time_slot = instructor_preferences[start + hour]
        for assigned_time_slot in assigned_times_instructors[course.instructor]:
            if time_slot == assigned_time_slot:
                return False
    return True


def schedule_courses(index, all_solutions):
    """
    Recursive depth first strategy is used to schedule each course

    Parameters:
            index (int): current index in courses list
            all_solutions (list): list to store valid schedules
    Returns:
            all_solutions (list): list which stores all valid schedules

    """

    if index == len(courses):
        new_schedule = {}
        for k, v in schedule.items():
            new_schedule[k] = v[0]
        all_solutions.append(new_schedule)
        return all_solutions

    course= courses[index]
    course_id = course.course_id
    instructor_id = course.instructor

    for classroom in classrooms_capacity:
        for start_time in range(len(instructors[instructor_id]) - course.hours + 1):
            if instructor_avaliability(course, start_time) and exclusive_classroom_assignment(course, start_time, classroom) and coordination_restrictions(course, start_time) and instructor_preferences_compliance(course, start_time) and consecutive_scheduling(course, start_time) and capacity_compliance(course,classroom):
                assigned_times = []
                for hour in range(course.hours):
                    time_slot = instructors[instructor_id][start_time + hour]
                    assigned_times.append(time_slot)
                    schedule[course_id].append([time_slot, classroom])
                    assigned_times_classrooms[classroom].append(time_slot)
                    assigned_times_instructors[instructor_id].append(time_slot)
                    assigned_times_courses[course_id].append(time_slot)


                schedule_courses(index + 1, all_solutions)

                for time_slot in assigned_times:
                    schedule[course_id].pop()
                    assigned_times_classrooms[classroom].remove(time_slot)
                    assigned_times_instructors[instructor_id].remove(time_slot)
                    assigned_times_courses[course_id].remove(time_slot)
    
    return all_solutions
   

  
        
def main():
    problem= sys.argv[1]
    solution = sys.argv[2]
    file_paths = [problem+"/preferences.csv", problem+"/courses.csv",problem+"/classrooms.csv",problem+"/coordinations.csv"]

    for file_path in file_paths:
        file_content = read_file(file_path)
        if file_path.endswith("preferences.csv"):
            for i in range(1, len(file_content), 2):
                instructor = file_content[i - 1]
                instructors[instructor] = file_content[i]
                assigned_times_instructors[instructor] = []
        elif file_path.endswith("courses.csv"):
            for i in range(len(file_content)):
                course_id, instructor, students, hours = file_content[i]
                courses.append(Course(course_id, instructor, students, hours))
                assigned_times_courses[course_id] = []
                schedule[course_id] = []
        elif file_path.endswith("classrooms.csv"):
            for i in range(len(file_content)):
                classroom, capacity = file_content[i]
                classrooms_capacity[classroom] = int(capacity)
                assigned_times_classrooms[classroom] = []
        elif file_path.endswith("coordinations.csv"):
            for coordination in file_content:
                for course_id in coordination:
                    for c in courses:
                        if c.course_id == course_id:
                            course = c
                    for coordinated_with in coordination:
                        if coordinated_with != course_id:
                            course.coordination.append(coordinated_with)
    all_schedules = []
    schedule_courses(0,all_schedules)
    create_solution_file(solution,all_schedules)
    
    


if __name__ == "__main__":
    main()



