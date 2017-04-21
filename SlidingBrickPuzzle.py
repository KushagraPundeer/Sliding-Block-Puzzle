#!/bin/python
import random
import sys
file_name = sys.argv[-1]



def load_game_state(file_name):
	txt_file = open(file_name,"r")
	filelist = txt_file
	#first_line = txt_file.readline().split(",")
	#width = first_line[0]
	#height = first_line[1]
	global states
	states = filelist.read()
	print states
	state=[]
	for line in txt_file:
  		item = line.split(",")
   		item = [x for x in item if x != "\n" and x != ""]
   		state.append(item)
	txt_file.close()
	original_state = state
	current_state = state


def output_game_state(file_name):
	load_game_state(file_name)

output_game_state(file_name)

def clone_state(file_name):
	clone = output_game_state(file_name)
	print clone

def puzzle_complete_check(file_name):
	array = map(lambda states: states.strip(), states)
	for i in array:
  		if(int(i) == '-1'):
    			return False
  		else:
   				return True


#puzzle_complete_check(file_name)
clone_state(file_name)

def __init__():
	current_state = []
	original_state = []
	height = 0
	width = 0

def get_Block_config(states,piece):
  pos = []
  for i in range(0,len(states)):
    for j in range(0,len(states[i])):
      if (int(states[i][j]) == int(piece)):
        pos.append([i,j])
      if len(pos) == 0:       # if no list present then
				return []       # return an empty list

      horizontal = []
      vertical = []
      for block in pos:
        if block[0] not in horizontal:
          horizontal.append(block[0])
        if block[1] not in vertical:
          vertical.append(block[1])
      horizontal.sort()
      vertical.sort()
      return [vertical,horizontal]


def all_Move_Possible(piece):
	if int(piece) < 2:
		return []

	Block_config = get_Block_config(state,piece)
	vertical = Block_config[0]
	horizontal = Block_config[1]
	Moves = ["RIGHT","LEFT","UP","Down"]

	# Check UP movement
	Pos_UP = horizontal[0] - 1
	for piec_posi in vertical:
		if int(state[Pos_UP][piece_posi]) != 0:
			Moves.remove('UP')
			break
	
	# Check DOWN movement
	POS_DOWN = horizontal[len(horizontal)-1] + 1
	for piece_posi in vertical:
		if int(state[POS_DOWN][piece_posi]) != 0:
			Moves.remove('DOWN')
			break

	# Check LEFT movement
	POS_LEFT = vertical[0] - 1
	for piece_posi in horizontal:
		if int(state[piece_posi][POS_LEFT]) != 0:
			Moves.remove('LEFT')
			break

	# Check RIGHT movement
	POS_RIGHT = vertical[len(vertical)-1] + 1
	for piece_posi in horizontal:
		if int(state[piece_posi][POS_RIGHT]) != 0:
			Moves.remove('RIGHT')
			break
	return Moves
		
def All_Moves_Board(states=None):
	piece = {}
	for row in states:
		for item in row:
			if item not in piece and int(item) > 1:
				piece[item] = None
	for key in piece:
		piece[key] = all_Move_Possible(key)
	return piece


def apply_Move(piece,direction,states):
	possible_Move = all_Move_Possible(piece,states)
	if direction not in possible_Move:
		return
	else:
		block_config = get_Block_config(states,piece)
		vertical = block_config[0]
		horizontal = block_config[1]

		if direction == "UP":
			new_empty_pos = horizontal[len(horizontal)-1]
			for i in range(0,len(horizontal)): 
				horizontal[i] -= 1
			for i in horizontal:
				for j in vertical:
					states[i][j] = piece
					states[new_empty_pos][j] = 0
		elif direction == "DOWN":
			new_empty_pos = horizontal[0]
			for i in range(0,len(horizontal)): 
				horizontal[i] += 1
			for i in horizontal:
				for j in vertical:
					states[i][j] = piece
					states[new_empty_pos][j] = 0
		elif direction == "LEFT":
			new_empty_pos = vertical[len(vertical)-1]
			for i in range(0,len(vertical)): 
				vertical[i] -= 1
			for i in horizontal:
				for j in vertical:
					states[i][j] = piece
					states[i][new_empty_pos] = 0
		else:
			new_empty_pos = vertical[0]
			for i in range(0,len(vertical)): 
				vertical[i] += 1
			for i in horizontal:
				for j in vertical:
					states[i][j] = piece
					states[i][new_empty_pos] = 0

def applyMoveCloning(piece,direction,states=None):
	new_state = clone_state(state)
	applyMove(new_state,piece,direction)
	return new_state

def state_comparison(compare_state,original_state=None):
	if original_state == None:
		state1 = current_state
	state2 = compare_state
	if len(state1) != len(state2):
		return False
	for i in range(0,len(state1)):
		if len(state1[i]) != len(state2[i]):
			return False
		for j in range(0,len(state1[i])):
			if state1[i][j] != state2[i][j]:
				return False
		return True

def swapIdx(state,idx1,idx2):
	for i in range(0,len(state)):
		for j in range(0,len(state[i])):
			if state[i][j] == idx1:
				state[i][j] = idx2
			elif state[i][j] == idx2:
				state[i][j] = idx2

def normalize_State(file_name):
		nextIdx = 3
		for i in range(0,len(current_state)):
			for j in range(0,len(current_state[i])):
				if current_state[i][j] == nextIdx:
					nextIdx += 1
				elif current_state[i][j] > nextIdx:
					swapIdx(self.current_state,nextIdx,current_state[i][j])
					nextIdx += 1

def randomWalk(n):

		all_move = All_Moves_Board(state)
		no_move_pieces = []
		for item in all_move:
			if len(all_move[item]) == 0:
				no_move_pieces.append(item)
		for item in no_move_pieces:
			all_move.pop(item,None)

print "All Possible Moves"
print "Game State:"

#print "\nPossible move of piece 3: "
#print all_Move_Possible(3)
print "\nPossible moves of board: "
#print c.All_Moves_Board()
#print "\n"
current_state = output_game_state(file_name)
apply_Move(3,"LEFT",current_state)
