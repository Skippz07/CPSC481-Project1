import json

class Course:
    def __init__(self, course_name, units, difficulty):
        self.name = course_name
        self.units = units
        self.difficulty = difficulty
        self.in_degree = 0
        self.prerequisites = []
        self.adj = []

class Graph:
    def __init__(self):
        self.courses = {}

    def add_course(self, course_name, units, difficulty):
        # If the course is not already in the graph, add it
        if course_name not in self.courses:
            self.courses[course_name] = Course(course_name, units, difficulty)

    def add_prerequisite(self, course_name, prereq_name, units, difficulty):
        # Ensure both the course and its prerequisite are added to the graph
        self.add_course(course_name, units, difficulty)
        self.add_course(prereq_name, units, difficulty)
        # Update adjacency list and in_degree of the courses
        self.courses[prereq_name].adj.append(self.courses[course_name])
        self.courses[course_name].in_degree += 1
        self.courses[course_name].prerequisites.append(self.courses[prereq_name])

#perform balanced topological sort on the graph
def balanced_topological_sort(graph, max_classes_per_semester, max_total_courses, taken_courses, total_units_taken):
    semesters = []  # List to store the sorted courses semester-wise
    # Find all courses with in_degree 0 that are not already taken
    zero_in_degree = [course for course in graph.courses.values() if course.in_degree == 0 and course.name not in taken_courses]
    total_courses_taken = len(taken_courses)  # Count of already taken courses, can be Adjusted for units later??
    
    # Adjust in_degree for courses that are prerequisites of the taken courses
    for course_name in taken_courses:
        course = graph.courses[course_name]
        for neighbor in course.adj: 
            neighbor.in_degree -= 1  
            if neighbor.in_degree == 0:  # If in_degree becomes 0, append to zero_in_degree list
                zero_in_degree.append(neighbor)
    
    iteration = 1  
    # Loop through to sort courses until no more courses can be added or total courses reached maximum
    while zero_in_degree and total_courses_taken < max_total_courses:
        semester_courses = []  # List to store courses in the current semester
        next_zero_in_degree = []  # List to store courses with in_degree 0 for the next iteration
        zero_in_degree.sort(key=lambda course: course.difficulty)
        
        # Iterate over all courses with in_degree 0
        for course in zero_in_degree:
            if course.name == "EGGN_495":
                # Check if the student has completed 90 units to take this course
                if total_units_taken >= 90 and len(semester_courses) < max_classes_per_semester:
                    semester_courses.append(course.name)
                    total_courses_taken += 1
                    total_units_taken += 3 
                else:
                    next_zero_in_degree.append(course)  # Add it back to be considered in the next iteration
                continue  
            # If all prerequisites are taken, add course to the current semester
            if all(prereq.name in [c for s in semesters for c in s] + taken_courses for prereq in course.prerequisites):
                if len(semester_courses) < max_classes_per_semester and total_courses_taken < max_total_courses:
                    semester_courses.append(course.name)
                    total_courses_taken += 1  
                    total_units_taken += graph.courses[course.name].units
                    # Decrement in_degree of neighboring courses and add to next_zero_in_degree list if in_degree becomes 0
                    for neighbor in course.adj:
                        neighbor.in_degree -= 1
                        if neighbor.in_degree == 0:
                            next_zero_in_degree.append(neighbor)
                else:
                    next_zero_in_degree.append(course)  
        
        if not semester_courses:  
            break
        
        #update values
        semesters.append(semester_courses)  
        zero_in_degree = next_zero_in_degree  
        iteration += 1  
    
    return semesters  

def validate_input(taken_courses, graph):
    for course in taken_courses:
        # Check if the input course is a valid course
        if course not in graph.courses:
            print(f"{course} is not a valid course.")
            return False

        # Check if the user has taken the prerequisites for each input course
        for prereq in graph.courses[course].prerequisites:
            if prereq.name not in taken_courses:
                print(f"You cannot take {course} without taking {prereq.name} first.")
                return False
    return True

def main():
    with open('dataJson.json', 'r') as file:
        data = json.load(file)

    taken_courses_input = input("Enter the courses you have already taken separated by commas (e.g. CPSC_120, MATH_150A), or press Enter if you haven't taken any: ").strip()
    taken_courses = [course.strip() for course in taken_courses_input.split(",")] if taken_courses_input else []

    # Function to recursively remove taken courses and their prerequisites
    def remove_taken_courses(courses_data, courses_to_remove):
        updated_courses = courses_data.copy()
        for category, courses in updated_courses.items():
            updated_category_courses = courses.copy()
            for course_code, details in courses.items():
                if course_code in courses_to_remove:
                    del updated_category_courses[course_code]
                    courses_to_remove.extend(details['prerequisites'])
            updated_courses[category] = updated_category_courses
        return updated_courses

    # Recursively remove taken courses and their prerequisites
    while True:
        filtered_data = remove_taken_courses(data, taken_courses)
        if filtered_data == data:
            break
        data = filtered_data

    graph = Graph()
    for category, courses in data.items():
        for course_code, details in courses.items():
            # Check if the course is in the filtered data and is not already taken
            if course_code in filtered_data[category]:
                units = details.get('units', 0)
                difficulty = details.get('difficulty', 1)
                graph.add_course(course_code, units, difficulty)  # Pass the units to add_course
                for prereq in details['prerequisites']:
                    graph.add_prerequisite(course_code, prereq, units, difficulty)

    # Remove courses from taken_courses that are not in the graph
    taken_courses = [course_name for course_name in taken_courses if course_name in graph.courses]

    total_units_taken = sum(graph.courses[course_name].units for course_name in taken_courses)

    # Validate user input and prompt until valid input is received
    max_classes_per_semester = 5
    max_total_courses = 40

    sorted_courses = balanced_topological_sort(graph, max_classes_per_semester, max_total_courses, taken_courses, total_units_taken)

    if sorted_courses:
        print("Balanced Semester-wise course plan:")
        for i, courses in enumerate(sorted_courses, 1):
            print(f"Semester {i}: {', '.join(courses)}")
    else:
        print("No valid order found. There might be a cycle in the prerequisites.")

    remaining_courses = set(graph.courses.keys()) - set(course for semester in sorted_courses for course in semester) - set(taken_courses)
    print("Remaining Courses:")
    for course_name in remaining_courses:
        course = graph.courses[course_name]
        print(f"{course_name}, in_degree: {course.in_degree}, prerequisites: {[prereq.name for prereq in course.prerequisites]}")

if __name__ == "__main__":
    main()
