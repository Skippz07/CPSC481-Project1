import json
import heapq

class Course:
    def __init__(self, course_code, name, units, prerequisites, difficulty, semester, offered_fall, offered_spring):
        self.course_code = course_code
        self.name = name
        self.units = units
        self.prerequisites = prerequisites
        self.difficulty = difficulty
        self.offered_fall = offered_fall
        self.offered_spring = offered_spring
        self.semester = semester

class State:
    def __init__(self, courses_taken, total_units_taken, semester, difficulty, parent):
        self.courses_taken = courses_taken
        self.total_units_taken = total_units_taken
        self.semester = semester
        self.difficulty = difficulty
        self.parent = parent

    def is_goal(self, total_units_required):
        return self.total_units_taken >= total_units_required

    def __lt__(self, other):
        return self.difficulty < other.difficulty

    def successors(self, available_courses):
        if self.semester % 2 != 0:            
        # For parent state in odd semesters (e.g., Fall), consider courses offered for successors in Spring
            eligible_courses = [course for course in available_courses if
                                course not in self.courses_taken and course.course_code not in completed_courses and
                                all(prereq in completed_courses for prereq in course.prerequisites) and
                                course.offered_spring]

        else:
            # For even semesters (e.g., Fall), consider courses offered in Fall
            eligible_courses = [course for course in available_courses if
                                course not in self.courses_taken and course.course_code not in completed_courses and
                                all(prereq in completed_courses for prereq in course.prerequisites) and
                                course.offered_fall]
        next_states = []
        new_courses_taken = []
        current_units = 0
        new_total_units_taken = self.total_units_taken
        total_difficulty = 0
        
        if(self.total_units_taken == 0):
            for course in eligible_courses:
                if (len(course.prerequisites) == 0):
                    current_units += course.units
                    if(current_units <= 17 and (course.course_code not in completed_courses)):
                        new_courses_taken = self.courses_taken + [course.course_code]
                        new_total_units_taken = new_total_units_taken + course.units                                            
                        completed_courses.append(course.course_code)
                        total_difficulty += course.difficulty
            next_states.append(State(new_courses_taken, new_total_units_taken, self.semester + 1, total_difficulty, self))
 
        else:
            for course in eligible_courses:
                if course.course_code not in self.courses_taken and (course.course_code not in completed_courses) and all(prereq in completed_courses for prereq in course.prerequisites):
                    current_units += course.units
                    if(current_units <= 17 and (course.course_code not in completed_courses) and (new_total_units_taken  + course.units <= 120)):                        
                        new_courses_taken += [course.course_code]
                        new_total_units_taken = new_total_units_taken + course.units
                        print("total units : ", new_total_units_taken)
                        completed_courses.append(course.course_code)
                        total_difficulty += course.difficulty
            next_states.append(State(new_courses_taken, new_total_units_taken, self.semester + 1, total_difficulty, self))
        return next_states

def astar_search(initial_state, total_units_required):
    open_set = [(0, initial_state)]  # Added depth information
    closed_set = set()
    already_added_courses = set()
    

    while True:
                
        _, current_state = heapq.heappop(open_set)

        if current_state.is_goal(total_units_required):
            print("it's goal")
            print("----------------")
            while(current_state.parent.semester != 1):   
                current_state = current_state.parent             
                print(current_state.parent.courses_taken)
            print("-------------")
            return current_state.courses_taken

        if current_state in closed_set:
            continue

        closed_set.add(current_state)

        for next_state in current_state.successors(available_courses):            
            g_n = 1
            h_n = next_state.difficulty
            f_n = g_n + h_n
            #printNextState(next_state, g_n, h_n)
            if next_state.courses_taken[-1] not in already_added_courses:
                heapq.heappush(open_set, (f_n, next_state))
                already_added_courses.add(next_state.courses_taken[-1])

    return None

def printNextState(state, path_cost, heuristic):
    print("semester : ", state.semester)
    print("--------------------------")
    for course in state.courses_taken:
        print(course)
    print("path cost : ", path_cost)
    print("heuristic : ", heuristic)
    print("--------------------------")
    
def printEligible(courses):
    for course in courses:
        print(course.course_code)
        
def printCompleted(courses):
    for course in courses:
        print(course)

# Load the JSON data and create Course objects
with open('dataJson.json', 'r') as file:
    data = json.load(file)

available_courses = []

for course_code, details in data.items():
    course = Course(course_code, details["name"], details["units"], details["prerequisites"], details["difficulty"],0, details["offered_fall"], details["offered_spring"])
    available_courses.append(course)

# Input: List of completed courses (e.g., ["MATH_150A", "CPSC_120"])
completed_courses = []  # You can populate this list with courses already taken

# Calculate the total units required for graduation
total_units_required = 120  # Adjust this value based on your program's requirements

# Create an initial state based on completed courses
initial_state = State(completed_courses, sum(course.units for course in completed_courses), 0, 0, None)

# Perform A* search to create a plan for graduation
graduation_plan = astar_search(initial_state, total_units_required)

if graduation_plan:
    print("Graduation Plan:", type(graduation_plan))
    for course in graduation_plan:
        print(course)
else:
    print("No valid graduation plan found within the specified depth limit.")
