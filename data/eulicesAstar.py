import json


class Node:
  def __init__(self, position: str, parent: "Node" = None):
    self.position = position
    self.parent = parent
    self.g = 0  # Cost from start to this node
    self.h = 0  # Heuristic cost from this node to goal
    self.f = 0  # Total cost

  def __eq__(self, other):
    return self.position == other.position

def a_star(courses, start, goal):
    semester = {}
    end_node = Node(goal)
    open_list = []
    closed_list = []
    # Add the start node
    open_list.append(Node(start))

    while open_list:
        # Find the node with the lowest f in open_list
        current_node = min(open_list, key=lambda x: x.f)

        # Add the current node to the closed list
        open_list.remove(current_node)
        closed_list.append(current_node.position)

        # Found the goal
        if current_node == end_node:
            path = []
            while current_node:
                print(current_node.position)
                path.append(current_node.position)
                if current_node:
                    if current_node.f in semester:
                        semester[current_node.f].append(current_node.position)
                    else:
                        semester[current_node.f] = [current_node.position]
                    current_node = current_node.parent
            return path[::-1], semester

        # Generate children
        children = []
        for course in courses[current_node.position]:
            if course not in closed_list:
                children.append(Node(course))

        for child in children:
            # Child is on the closed list
            if child.position in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = 0
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list and child.g > current_node.g:
                continue

            # Add the child to the open list
            child.parent = current_node
            open_list.append(child)

def ajencencyList(data):
  adjacency_list = {}
  for section in data:
    for course in data[section]:
      for prerequisite in data[section][course]["prerequisites"]:
        if prerequisite in adjacency_list:
              adjacency_list[prerequisite].append(course)
        else:
              adjacency_list[prerequisite] = [course]

        if course not in adjacency_list:
              adjacency_list[course] = []

  return adjacency_list



def main():
  ### Loading json ###
  f = open('dataJson.json', 'r')
  catalog = json.load(f)
  f.close()

  ajencency = ajencencyList(catalog)
  
  # print(ajencency)

  travel, semester = a_star(ajencency, min(ajencency, key=lambda x: len(x)), "CPSC_223")
  print(travel)
  print("_______________________________________________________")
  print(semester)

if __name__ == "__main__":
  main()
