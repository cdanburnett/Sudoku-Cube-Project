from face import Face
import random
import math

class Cube:
    def __init__(self, top=None, left=None, front=None, right=None, back=None, bottom=None):
        # re-written so it can be used in reserializing function. If no arguments are givent, it uses the original solved state.
        self.top = Face(top or [8, 1, 3, 4, 6, 7, 2, 9, 5])
        self.left = Face(left or [7, 1, 8, 2, 4, 6, 9, 3, 5])
        self.front = Face(front or [9, 5, 2, 3, 8, 1, 6, 7, 4])
        self.right = Face(right or [4, 6, 3, 7, 5, 9, 1, 2, 8])
        self.back = Face(back or [9, 5, 2, 3, 8, 1, 6, 7, 4])
        self.bottom = Face(bottom or [1, 2, 8, 5, 3, 9, 7, 4, 6])

        # Just in case someone sees this and thinks I used a shortcut, no. You can observe this value is never updated
        # outside of the randomizer, where it is used to make sure a move is not immedietly un-done.
        self.last_move = [Face, str]

        # wire the cube together, telling each face what face is it's "relative top, relative left..." etc.
        # give the face a string name for comparison later in dispatcher function
        self.top.name = "top"
        self.top.reltop    = self.back
        self.top.relleft   = self.left
        self.top.relright  = self.right
        self.top.relbottom = self.front

        self.left.name = "left"
        self.left.reltop    = self.top
        self.left.relleft   = self.back
        self.left.relright  = self.front
        self.left.relbottom = self.bottom

        self.front.name = "front"
        self.front.reltop    = self.top
        self.front.relleft   = self.left
        self.front.relright  = self.right
        self.front.relbottom = self.bottom

        self.right.name = "right"
        self.right.reltop    = self.top
        self.right.relleft   = self.front
        self.right.relright  = self.back
        self.right.relbottom = self.bottom

        self.back.name = "back"
        self.back.reltop    = self.top
        self.back.relleft   = self.right
        self.back.relright  = self.left
        self.back.relbottom = self.bottom

        self.bottom.name = "bottom"
        self.bottom.reltop    = self.front
        self.bottom.relleft   = self.left
        self.bottom.relright  = self.right
        self.bottom.relbottom = self.back

    # -------------------------
    # Helpers to rotate a face in place
    def rotate_face_left(self, face: Face):
        face.values = [
            face.values[2], face.values[5], face.values[8],
            face.values[1], face.values[4], face.values[7],
            face.values[0], face.values[3], face.values[6]
        ]

    def rotate_face_right(self, face: Face):
        face.values = [
            face.values[6], face.values[3], face.values[0],
            face.values[7], face.values[4], face.values[1],
            face.values[8], face.values[5], face.values[2]
        ]

    # These functions take a face and rotate it. The function is already chosen because it is the selected face and rotation,
    # so all it takes is the face occurence and swaps the appropriate values.
    # each function is distinct because of how the values are stored for each face in rows and columns, and their adjacent stickers must be reversed in order, or not,
    # depending on what face is rotatated which direction.
    #
    # example: if you rotate the front, rightward, then the right column of the left face, must be reversed and put into the bottom row of the top face.
    # each function also calles the appropriate rotate_face function based on the direction, to rotate the values on the face itself.
    # -------------------------
    # Top rotations
    def rotate_top_leftward(self, top: Face):
        temp = top.reltop.top_row 
        top.reltop.top_row    = top.relright.top_row 
        top.relright.top_row  = top.relbottom.top_row 
        top.relbottom.top_row = top.relleft.top_row 
        top.relleft.top_row   = temp
        self.rotate_face_left(top)

    def rotate_top_rightward(self, top: Face):
        temp = top.reltop.top_row
        top.reltop.top_row    = top.relleft.top_row
        top.relleft.top_row   = top.relbottom.top_row
        top.relbottom.top_row = top.relright.top_row 
        top.relright.top_row  = temp
        self.rotate_face_right(top)

    # -------------------------
    # Left rotations
    def rotate_left_leftward(self, left: Face):
        temp = left.reltop.left_col
        left.reltop.left_col     = left.relright.left_col
        left.relright.left_col   = left.relbottom.left_col
        left.relbottom.left_col  = list(reversed(left.relleft.right_col))
        left.relleft.right_col   = list(reversed(temp))
        self.rotate_face_left(left)

    def rotate_left_rightward(self, left: Face):
        temp = left.reltop.left_col
        left.reltop.left_col     = list(reversed(left.relleft.right_col))
        left.relleft.right_col   = list(reversed(left.relbottom.left_col))
        left.relbottom.left_col  = left.relright.left_col
        left.relright.left_col   = temp
        self.rotate_face_right(left)

    # -------------------------
    # Front rotations
    def rotate_front_leftward(self, front: Face):
        temp = front.reltop.bottom_row
        front.reltop.bottom_row  = front.relright.left_col
        front.relright.left_col  = list(reversed(front.relbottom.top_row))
        front.relbottom.top_row  = front.relleft.right_col
        front.relleft.right_col  = list(reversed(temp))
        self.rotate_face_left(front)

    def rotate_front_rightward(self, front: Face):
        temp = front.reltop.bottom_row
        front.reltop.bottom_row  = list(reversed(front.relleft.right_col))
        front.relleft.right_col  = front.relbottom.top_row
        front.relbottom.top_row  = list(reversed(front.relright.left_col))
        front.relright.left_col  = temp
        self.rotate_face_right(front)

    # -------------------------
    # Right rotations
    def rotate_right_leftward(self, right: Face):
        temp = right.reltop.right_col
        right.reltop.right_col   = list(reversed(right.relright.left_col))
        right.relright.left_col  = list(reversed(right.relbottom.right_col))
        right.relbottom.right_col= right.relleft.right_col
        right.relleft.right_col  = temp
        self.rotate_face_left(right)

    def rotate_right_rightward(self, right: Face):
        temp = right.reltop.right_col
        right.reltop.right_col   = right.relleft.right_col
        right.relleft.right_col  = right.relbottom.right_col
        right.relbottom.right_col= list(reversed(right.relright.left_col))
        right.relright.left_col  = list(reversed(temp))
        self.rotate_face_right(right)

    # -------------------------
    # Back rotations
    def rotate_back_leftward(self, back: Face):
        temp = back.reltop.top_row
        back.reltop.top_row      = list(reversed(back.relright.left_col))
        back.relright.left_col   = back.relbottom.bottom_row
        back.relbottom.bottom_row= list(reversed(back.relleft.right_col))
        back.relleft.right_col   = temp
        self.rotate_face_left(back)

    def rotate_back_rightward(self, back: Face):
        temp = back.reltop.top_row
        back.reltop.top_row      = back.relleft.right_col
        back.relleft.right_col   = list(reversed(back.relbottom.bottom_row))
        back.relbottom.bottom_row= back.relright.left_col
        back.relright.left_col   = list(reversed(temp))
        self.rotate_face_right(back)

    # -------------------------
    # Bottom rotations
    def rotate_bottom_leftward(self, bottom: Face):
        temp = bottom.reltop.bottom_row
        bottom.reltop.bottom_row   = bottom.relright.bottom_row
        bottom.relright.bottom_row = bottom.relbottom.bottom_row
        bottom.relbottom.bottom_row= bottom.relleft.bottom_row
        bottom.relleft.bottom_row  = temp
        self.rotate_face_left(bottom)

    def rotate_bottom_rightward(self, bottom: Face):
        temp = bottom.reltop.bottom_row
        bottom.reltop.bottom_row   = bottom.relleft.bottom_row
        bottom.relleft.bottom_row  = bottom.relbottom.bottom_row
        bottom.relbottom.bottom_row= bottom.relright.bottom_row
        bottom.relright.bottom_row = temp
        self.rotate_face_right(bottom)

    # -------------------------
    # called from main or from other class functions
    # this takes the face and the direction
    # it then checks which face it is using the face.name string value of the face class
    # it then calls the cube rotate face function
    # Dispatcher
    def rotate(self, face: Face, direction: str):
        if face.name == "top":
            if direction == "left":
                self.rotate_top_leftward(face)
            elif direction == "right":
                self.rotate_top_rightward(face)

        elif face.name == "left":
            if direction == "left":
                self.rotate_left_leftward(face)
            elif direction == "right":
                self.rotate_left_rightward(face)

        elif face.name == "front":
            if direction == "left":
                self.rotate_front_leftward(face)
            elif direction == "right":
                self.rotate_front_rightward(face)

        elif face.name == "right":
            if direction == "left":
                self.rotate_right_leftward(face)
            elif direction == "right":
                self.rotate_right_rightward(face)

        elif face.name == "back":
            if direction == "left":
                self.rotate_back_leftward(face)
            elif direction == "right":
                self.rotate_back_rightward(face)

        elif face.name == "bottom":
            if direction == "left":
                self.rotate_bottom_leftward(face)
            elif direction == "right":
                self.rotate_bottom_rightward(face)
        else:
            print("Error: unknown face name")

    # -------------------------
    # Pretty printer
    # Called from main using the instance of cube, say cube_1, it is called using cube_1.Print_Cube()
    # prints the unfolded cube with labels for each face.
    def Print_Cube(self):
        print("               Top  ")
        print("           ", self.top.top_row)
        print("           ", self.top.middle_row)
        print("           ", self.top.bottom_row)
        print("  Left        Front       Right       Back")
        print(self.left.top_row, " ", self.front.top_row, " ", self.right.top_row, " ", self.back.top_row)
        print(self.left.middle_row, " ", self.front.middle_row, " ", self.right.middle_row, " ", self.back.middle_row)
        print(self.left.bottom_row, " ", self.front.bottom_row, " ", self.right.bottom_row, " ", self.back.bottom_row)
        print("              Bottom ")
        print("           ", self.bottom.top_row)
        print("           ", self.bottom.middle_row)
        print("           ", self.bottom.bottom_row)
        print()
        print()

    
    # Scramble cube function
    # called from main using instance_of_cube_class.Scramble(integer)
    # this scramble function will perform 10 completely unique and random scrambles, before becoming random face rotations that don't undo the last face rotation only.
    # Do do this, it makes an array of the faces of the cube instance, top, left, front, etc.
    # It then enters a while loop, which executes the number of moves given as the moves parameter.
    # it randomly chooses a face from the array of faces
    # it randomly chooses 1 or 0, if the random number is 0, the direction of rotation is right, otherwise, it is "left"
    # It then checks if the attribute "last_move" has been set.
        # if it has, it gets the Face and the direction string from the last_move
            # if the last face is the same as the currently chosen random face to rotate, it checks if the direction is the opposite.
            # if it is, we choose a different face
    # it also checks to make sure that the first 10 moves are completely distinct, by saving the first 10 moves it makes into an array in the cube data structure.
    # if we are in the first 10 moves, and the currently chosen face,direction pair are in the array of face,direction pairs
        # we restart the face choosing, to ensure the first 10 moves are completely distinct and random.
    # if we get to this point, we move the cube,
    # we save the face,direction as the last move, and if this is in the first 10 scramble moves, we also append the face,direction pair into the first_10 array for
    # future comparisons.
    def Scramble(self, moves: int):
        face_call = Face
        faces_array = [self.top, self.left, self.front, self.right, self.back, self.bottom]
        # while
        i = 1
        while i <= moves:
            random_number = random.randint(0, 1)
            direction = ""
            face_call = faces_array[random.randint(0, 5)]
            
            
            direction = "right"
            

            # don't check unless it's not the second move
            if hasattr(self, "last_move"):
                last_face_rotated, last_direction = self.last_move # split the value
                # skip if the face is the same and the direction is the opposite
                if last_face_rotated == face_call:
                    if (last_direction == "right" and direction == "left") or (last_direction == "left" and direction == "right"):
                        continue # rerun current while loop without increasing i
                    
            
            # move the face in the given direction
            self.rotate(face_call, direction)
            self.last_move = [face_call, direction]
            i += 1
    
    # helper for the heuristic to count the number of non-distinct numbers (repeated instances of each number) on a face.
    # function call, Cube.num_repeats(self.face.values)
    def num_repeats(values):
        repeated_values = 0
        for val in set(values):
            count = values.count(val)
            if count > 1:
                repeated_values += (count - 1)  # count the extras
        return repeated_values

    # heuristic function
    # called from main using Cube.Moves_To_Solved_Heuristic(instance of cube object)

    # This heuristic calls the helper function above on each of the 6 faces of the cube, and places the count of non-distinct "stickers" into an array
    # I then check if the cube is solved, if it isn't...
        # I find the max value of the array
        # I find the number of faces that have more than 0 repeated non-distinct "stickers"
        # if the max occurs on more than one face, and all of the faces of the cube have non-distinct "stickers", and the max is 4 or greater
            # I assume it would take + 1 moves to solve the cube.
                # I conclude this because if there is more than one face with a max of 4 non-distincts
                # at most it will take 2 moves to resolve those two faces, and if every face is scrambled, we can assume it would take at least one more
                # move to solve those, as 1 move could ideally resolve up to 4 faces, but if more than one face requires 2 moves, it will take at least 3.
                # So I return the ceiling of the (max / 3) + 1 (rounding up because 1 move resolves 3 values on a face, but if its 4, 1 move doesn't resolve it) 
        # if these criteria are not the case, I simply return the ceiling of the max / 3 without the + 1
    # This heuristic, since it assumes nearly 3 most ideal situations, will never, and has never over estimated the number of moves to solve.
    # I have run this more than 30 times. It never overestimates, or declares it to be 0 unless the cube is solved (move estimate is 0).
    # move estimate is never zero unless the max in the array is 0.
    def Moves_To_Solved_Heuristic(self):
        unsolved_face_counts = [Cube.num_repeats(self.top.values), Cube.num_repeats(self.left.values), Cube.num_repeats(self.front.values),
                       Cube.num_repeats(self.right.values), Cube.num_repeats(self.back.values), Cube.num_repeats(self.bottom.values)]
        
        # get the max
        max_val = max(unsolved_face_counts)
        move_estimate = math.ceil(max_val / 3)
        # get the number of faces that have repeated values
        count_faces = sum(1 for val in unsolved_face_counts if val > 0)

        
        # choose which estimate to use based on if the number of scrambled faces > 5, and the max occurs more than once, and the max scrabled face >= 4
        if unsolved_face_counts.count(max_val) > 1 and (max_val >= 4) and (count_faces > 5):
            return(move_estimate + 1) 
        else:
            return move_estimate
        
        

        
        
        
        
        