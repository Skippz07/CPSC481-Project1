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
                if course.name == "EGGN_495":
                    if new_total_units_taken >= 90 and current_units <= 14:
                        continue
                        
                if course.course_code not in completed_courses and all(prereq in completed_courses for prereq in course.prerequisites):
                    current_units += course.units
                    if(current_units <= 17 and (course.course_code not in completed_courses) and (new_total_units_taken  + course.units <= 120)):                        
                        new_courses_taken += [course.course_code]
                        new_total_units_taken = new_total_units_taken + course.units
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
        final_plan =[]
        if current_state.is_goal(total_units_required):            
            while(current_state.parent.semester >= 1):  
                final_plan.append(current_state) 
                current_state = current_state.parent
            final_plan.append(current_state)
            return final_plan

        if current_state in closed_set:
            continue

        closed_set.add(current_state)

        for next_state in current_state.successors(available_courses):            
            g_n = 1
            h_n = next_state.difficulty
            f_n = g_n + h_n
            if next_state.courses_taken[-1] not in already_added_courses:
                heapq.heappush(open_set, (f_n, next_state))
                already_added_courses.add(next_state.courses_taken[-1])

    return None


# Load the JSON data and create Course objects
with open('dataJson.json', 'r') as file:
    data = json.load(file)
original_data = data
available_courses = []
    
# for course_code, details in data.items():
#     course = Course(course_code, details["name"], details["units"], details["prerequisites"], details["difficulty"],0, details["offered_fall"], details["offered_spring"])
#     available_courses.append(course)


    
taken_courses_input = input("Enter the courses you have already taken separated by commas (e.g. CPSC_120, MATH_150A), or press Enter if you haven't taken any: ").strip()
taken_courses = [course.strip() for course in taken_courses_input.split(",")] if taken_courses_input else []

total_units_taken = 0
        
def remove_taken_courses(courses_data, courses_to_remove, total_units_taken):
    updated_courses = courses_data.copy()
    for course_code in courses_to_remove.copy():
        if course_code in updated_courses:
            course_details = updated_courses[course_code]
            del updated_courses[course_code]
            courses_to_remove.extend(course_details['prerequisites'])
    return updated_courses



# Recursively remove taken courses and their prerequisites
while True:
    filtered_data = remove_taken_courses(data, taken_courses, total_units_taken)
    if filtered_data == data:
        break
    data = filtered_data

    
for course_code, details in original_data.items():
    if course_code in filtered_data:
        course = Course(course_code, details["name"], details["units"], details["prerequisites"], details["difficulty"],0, details["offered_fall"], details["offered_spring"])
        available_courses.append(course)
    else:
        total_units_taken += details['units']

total_units_required = 120 - total_units_taken # Adjust this value based on your program's requirements

print("total units required")
print(total_units_required)
# Create an initial state based on completed courses
completed_courses = taken_courses
initial_state = State(completed_courses, total_units_taken, 0, 0, None)

# Perform A* search to create a plan for graduation
graduation_plan = astar_search(initial_state, total_units_required)

if graduation_plan:
    print("Graduation Plan:", type(graduation_plan))
    counter = 1
    for course in reversed(graduation_plan):
        print('Semester %i: %s' % (counter, course.courses_taken))
        counter += 1
else:
    print("No valid graduation plan found within the specified depth limit.")
