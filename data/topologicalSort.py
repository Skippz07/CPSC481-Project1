import json

class Course:
    def __init__(self, course_name):
        self.name = course_name
        self.in_degree = 0
        self.adj = []

class Graph:
    def __init__(self):
        self.courses = {}
    
    def add_course(self, course_name):
        if course_name not in self.courses:
            self.courses[course_name] = Course(course_name)
    
    def add_prerequisite(self, course_name, prereq_name):
        if course_name not in self.courses:
            self.add_course(course_name)
        if prereq_name not in self.courses:
            self.add_course(prereq_name)
        
        self.courses[prereq_name].adj.append(self.courses[course_name])
        self.courses[course_name].in_degree += 1

def topological_sort(graph):
    stack = []
    result = []
    
    # Find all courses with 0 in-degree
    for course_name, course in graph.courses.items():
        if course.in_degree == 0:
            stack.append(course)
    
    while stack:
        current = stack.pop()
        result.append(current.name)
        
        for neighbour in current.adj:
            neighbour.in_degree -= 1
            if neighbour.in_degree == 0:
                stack.append(neighbour)
    
    if len(result) == len(graph.courses):
        return result
    else:
        return None

with open('./dataJson.json', 'r') as file:
    data = json.load(file)

graph = Graph()

# Construct the graph
for category, courses in data.items():
    for course_code, details in courses.items():
        graph.add_course(course_code)
        for prereq in details['prerequisites']:
            graph.add_prerequisite(course_code, prereq)

# Perform the topological sort
sorted_courses = topological_sort(graph)

if sorted_courses:
    print("Topological order of courses:")
    for course in sorted_courses:
        print(course)
else:
    print("No valid order found. There might be a cycle in the prerequisites.")
