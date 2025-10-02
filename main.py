# import classes
from face import Face
from cube import Cube
import heapq

# helper function to "compress" cube state
def Serialize_Cube(current_cube: Cube):
    # treturns tuple constructed by concattenating the cubes face lists
    return tuple(current_cube.top.values + current_cube.left.values + current_cube.front.values + current_cube.right.values + current_cube.back.values + current_cube.bottom.values)  

# extract cube object from serialized tuple
def Unserialize_Cube(cube_state: tuple):
    # reconstruct portions of the tuple back into face value lists.
    top = list(cube_state[0:9])
    left = list(cube_state[9:18]) 
    front = list(cube_state[18:27]) 
    right = list(cube_state[27:36])
    back = list(cube_state[36:45])
    bottom = list(cube_state[45:54])
    # return a constructed cube using the extracted lists, by calling the constructor
    return Cube(top, left, front, right, back, bottom)

# Tree nodes
# takes a cube state as a tuple, unserializes and gets heuristic value
# given_cube is a tuple (already serialized)
# assumes it is given a serialized cube to begin with.
class Node:
    def __init__(self, cube_state: tuple, parent=None):
        # store serialized cube first
        self.cube_state = cube_state
        self.move_made = None
        # unserialize it to get the heuristic values
        current_cube = Unserialize_Cube(cube_state)

        # save the current heuristic value of the cube
        self.h = current_cube.Moves_To_Solved_Heuristic() # call heuristic on current cube state and store in the node
        self.parent = parent # pointer to parent node, if not passed when making a node, it will be None.

        # if its not the root, increment the depth counter
        if parent != None:
            self.g = parent.g + 1
        else:
            self.g = 0 # Initial depth
        self.f = self.g + self.h
        # vector of child nodes references.
        self.children = []

# function takes a nodes and expands
def expand_node(node: Node):
    
    # make 6 copies of the cube, and mutate:
    node_cube_1_top_rotated = Unserialize_Cube(node.cube_state)
    node_cube_1_top_rotated.rotate(node_cube_1_top_rotated.top, "left") # make the move
    # store the move as a node
    child1 = Node(Serialize_Cube(node_cube_1_top_rotated), node)
    # store the move made for path re-tracing
    child1.move_made = ['top face', 'leftward']

    # this is then repeated for the other cubes, but with each possible "leftward move"

    node_cube_2_left_rotated = Unserialize_Cube(node.cube_state)
    node_cube_2_left_rotated.rotate(node_cube_2_left_rotated.left, "left")
    child2 = Node(Serialize_Cube(node_cube_2_left_rotated), node)
    child2.move_made = ['left face', 'leftward']

    node_cube_3_front_rotated = Unserialize_Cube(node.cube_state)
    node_cube_3_front_rotated.rotate(node_cube_3_front_rotated.front, "left")
    child3 = Node(Serialize_Cube(node_cube_3_front_rotated), node)
    child3.move_made = ['front face', 'leftward']

    node_cube_4_right_rotated = Unserialize_Cube(node.cube_state)
    node_cube_4_right_rotated.rotate(node_cube_4_right_rotated.right, "left")
    child4 = Node(Serialize_Cube(node_cube_4_right_rotated), node)
    child4.move_made = ['right face', 'leftward']

    node_cube_5_back_rotated = Unserialize_Cube(node.cube_state)
    node_cube_5_back_rotated.rotate(node_cube_5_back_rotated.back, "left")
    child5 = Node(Serialize_Cube(node_cube_5_back_rotated), node)
    child5.move_made = ['back face', 'leftward']

    node_cube_6_bottom_rotated = Unserialize_Cube(node.cube_state)
    node_cube_6_bottom_rotated.rotate(node_cube_6_bottom_rotated.bottom, "left")
    child6 = Node(Serialize_Cube(node_cube_6_bottom_rotated), node)
    child6.move_made = ['bottom face', 'leftward']

    # add the children to the visited node
    node.children = [child1, child2, child3, child4, child5, child6]

# Function to trace the path to solved state by traversing parents and appending move pairs
# function then reverses the moves list to give the moves in order.
def trace_path(node: Node):
    # vector to store strings that represent what move to make
    moves_list = []
    while node.parent != None:
        moves_list.append(node.move_made)
        node = node.parent
    return list(reversed(moves_list))
        
# make an A* recursive function using priority queue and hashtable
def Star_Search(root_node: Node):
    # make the list for tracking states already visited.
    # only use the serialized value.
    visited_nodes = set() # reccomended by Dr. Harrison to ensure I can check I haven't seen a node before expanding.

    # See citations in word document, the following is based on a repsonse given by chat GPT after being supplied my code using a priority queue.
    # There were a few fixes, involving breaking ties by changing what values get inerted to the heap elements when.
    # The counter was suggested by chatGPT, though I had already theorized one could use g as a secondary comparison for breaking ties.
    # 
    # minheap
    frontier = []

    # counter for tie breaking
    # this counter increments, and is part of what gets pushed onto the heap, so popping from the heap, if there is a tie
    # between f and g values, it will pop the earliest made node first. no two elements in the heap have the same value, so overloading 
    # the = operator for the node class was not needed.
    counter = 0


    # put root node into frontier heap
    # g is compared second to break ties, and then if needed, uses counter so it never tries to compare nodes.
    heapq.heappush(frontier, (root_node.f, root_node.g, counter, root_node))

    # use of counter was suggested by chatGPT, and is cited in the word doc
    counter+=1

    # while loop to a* search
    while len(frontier) != 0:
        # pop lowest f, (if not lowest f, lowest g node)
        f_value, g_value, count, present_node = heapq.heappop(frontier)
    

        # check if node has been visited before, before checking if its a solved state.
        if present_node.cube_state in visited_nodes:
            # get new node from heap if it has been visited before
            continue

        # Add the visited node to the list of visited node
        visited_nodes.add(present_node.cube_state)

        # check if present node is solved state
        if present_node.h == 0:
            # print the path
            print('Solved, here is the path', trace_path(present_node))
            
            # commented out but you can check that it is solved.
            # print('here is the cube')
            # the_solved_cube = Unserialize_Cube(present_node.cube_state)
            # the_solved_cube.Print_Cube()
            
            # return the size of frontier
            return len(frontier)
        else:
            # expand present node
            expand_node(present_node)

            for child in present_node.children:
                # make sure child is not in visited nodes (we have never seen this state before)
                if child.cube_state not in visited_nodes:
                    # put the children into the frontier
                    heapq.heappush(frontier, (child.f, child.g, counter, child))
                    # increment counter used for tie breaking to open the node made first
                    counter += 1
                    

    # if while loop terminates without returning, there was an error
    print('error, while loop terminated without finding solution')
    return -1

# define the main function which assembles the cube faces with their values.
def main():
    # loops from k = 3 to 20
    k = 3
    while k <= 20:
        average_frontier_size = 0
        # generate 5 cubes and scramble them k times, and then print out the k value and corresponding average size frontier
        cube1 = Cube()
        cube1.Scramble(k)
        average_frontier_size += Star_Search(Node(Serialize_Cube(cube1), None))

        cube2 = Cube()
        cube2.Scramble(k)
        average_frontier_size += Star_Search(Node(Serialize_Cube(cube2), None))

        cube3 = Cube()
        cube3.Scramble(k)
        average_frontier_size += Star_Search(Node(Serialize_Cube(cube3), None))

        cube4 = Cube()
        cube4.Scramble(k)
        average_frontier_size += Star_Search(Node(Serialize_Cube(cube4), None))

        cube5 = Cube()
        cube5.Scramble(k)
        average_frontier_size += Star_Search(Node(Serialize_Cube(cube5), None))
        
        print()
        print('K = ', k, ' and the average frontier size was ', average_frontier_size/5)
        print()
        k = k + 1
    



if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")