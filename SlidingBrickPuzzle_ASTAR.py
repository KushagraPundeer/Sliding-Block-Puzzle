#!/bin/python 
import random
import sys
import time
file_name = sys.argv[-1]

def load_game_state(file_name):
	txt_file = open(file_name,"r")
	filelist = txt_file
	first_line = txt_file.readline().split(",")
	global width, height, orignal_state, current_state
	width = first_line[0]
	height = first_line[1]
	state = []
	for line in txt_file:
		item = line.split(",")
		item = [x for x in item if x != "\n" and x != ""]
		state.append(item)		
	orignal_state = state
	current_state = state
	txt_file.close()
load_game_state(file_name)

def output_game_state(file_name,SN):
	print width + "," + height + ","
	for row in SN:
		s = ""
		for item in row:
			s += str(item) + ","
		print s
output_game_state(file_name,current_state)

def clone_state(SN):
	output = []
	for row in SN:
		l = []
		for item in row:
			l.append(item)
		output.append(l)
	return output

def puzzle_complete_check(SN):
	#state = current_state
	for row in SN:
		for item in row:
			if item == '-1':
				return False 
	return True

def get_Block_Position(SN,piece):
	position = []
	for i in range(0,len(SN)):
		for j in range(0,len(SN[i])):
			if int(SN[i][j]) == int(piece):
				position.append([i,j])
	return position

#get_Block_Position(state,2)

def all_possible_move_piece(piece,SN):
	if int(piece) < 2:
		return []
	elif int(piece) != 2:
		blockPosition = get_Block_Position(SN,piece)
		B = []
		for item in blockPosition:
			vertical = item[0]
			horizontal = item[1]
			output = []
			# UP move
			up_position = vertical - 1
			if int(SN[up_position][horizontal]) == 0:
				output.append('UP')
			if int(SN[up_position][horizontal]) == int(piece):
				output.append('UP')

			# DOWN move
			down_position = vertical + 1
			if int(SN[down_position][horizontal]) == 0:
				output.append('DOWN')
			if int(SN[down_position][horizontal]) == int(piece):
				output.append('DOWN')

			# LEFT move
			left_position = horizontal - 1
			if int(SN[vertical][left_position]) == 0:
				output.append('LEFT')
			if int(SN[vertical][left_position]) == int(piece):
				output.append('LEFT')

			# RIGHT move
			right_position = horizontal + 1
			if int(SN[vertical][right_position]) == 0:
				output.append('RIGHT')
			if int(SN[vertical][right_position]) == int(piece):
				output.append('RIGHT')
			B.append(set(output))

	elif int(piece) == 2:
		blockPosition = get_Block_Position(SN,piece)
		B = []
		for item in blockPosition:
			vertical = item[0]
			horizontal = item[1]
			output = []
			# UP move
			up_position = vertical - 1
			if int(SN[up_position][horizontal]) == 0:
				output.append('UP')
			if int(SN[up_position][horizontal]) == int(piece):
				output.append('UP')
			if((SN[up_position][horizontal]) == '-1'):
				output.append('UP')

			# DOWN move
			down_position = vertical + 1
			if int(SN[down_position][horizontal]) == 0:
				output.append('DOWN')
			if int(SN[down_position][horizontal]) == int(piece):
				output.append('DOWN')
			if((SN[down_position][horizontal]) == '-1'):
				output.append('DOWN')

			# LEFT move
			left_position = horizontal - 1
			if int(SN[vertical][left_position]) == 0:
				output.append('LEFT')
			if int(SN[vertical][left_position]) == int(piece):
				output.append('LEFT')
			if((SN[vertical][left_position]) == '-1'):
				output.append('LEFT')
			# RIGHT move
			right_position = horizontal + 1
			if int(SN[vertical][right_position]) == 0:
				output.append('RIGHT')
			if int(SN[vertical][right_position]) == int(piece):
				output.append('RIGHT')
			if((SN[vertical][right_position]) == '-1'):
				output.append('RIGHT')
			B.append(set(output))		
	u = set.intersection(*B)
	AM = list(u)
	return AM


def all_possible_move_board(SN):
	#state = current_state
	piece = {}
	for row in SN:
		for item in row:
			if item not in piece and int(item) > 1:
				piece[item] = None               
	for key in piece:
		piece[key] = all_possible_move_piece(key,SN)
	return piece

def applyMove(piece,direction,SN):
	possibleMove = all_possible_move_piece(piece,SN)
	#print possibleMove
	if direction not in possibleMove:
		return
	else:
		blockSide = get_Block_Position(SN,piece)
		for item in blockSide:
			vertical = item[0]
			horizontal = item[1]
			if direction == 'UP':
				new_empty_position = vertical - 1
				SN[new_empty_position][horizontal] = piece
				SN[vertical][horizontal] = str(0)
			elif direction == 'DOWN':
				new_empty_position = vertical + 1
				SN[new_empty_position][horizontal] = piece
				SN[vertical][horizontal] = str(0)
			elif direction == 'LEFT':
				new_empty_position = horizontal - 1
				SN[vertical][new_empty_position] = piece
				SN[vertical][horizontal] = str(0)
		for item in reversed(blockSide):
			vertical = item[0]
			horizontal = item[1]
			if direction == 'RIGHT':
				new_empty_position = horizontal + 1
				SN[vertical][new_empty_position] = piece
				SN[vertical][horizontal] = str(0)
		return SN

def applyMoveCloning(piece,direction,SN):
	new_state = clone_state(SN)
	L = applyMove(piece,direction,new_state)
	return L

applyMoveCloning('2','DOWN',current_state)

def state_comparison(comparison_state,orignal_state):
	state_1 = current_state
	state_2 = comparison_state
	if len(state_1) != len(state_2):
		return False
	for i in range(0,len(state_1)):
		if len(state_1[i]) != len(state_2[i]):
			return False
		for j in range(0,len(state_1[i])):
			if state_1[i][j] != state_2[i][j]:
				return False
	return True
	
def swapIdx(idx1,idx2,SN):
	for i in range(0,int(height)):
		for j in range(0,int(width)):
			if SN[i][j] == idx1:
				SN[i][j] = str(idx2)
			elif SN[i][j] == idx2:
				SN[i][j] = str(idx1)

def normalizeState(SN):
	N_state = SN
	nextIdx = 3
	for i in range(0,int(height)):
		for j in range(1,int(width)):
			if N_state[i][j] == nextIdx:
				nextIdx = nextIdx + 1
			if int(N_state[i][j]) > nextIdx:
				swapIdx(nextIdx,N_state[i][j],N_state)
				nextIdx = nextIdx + 1
	return N_state

#normalizeState(current_state)

def BFS(SN):
	OPEN = [SN]
	CLOSED = []
	Nodes = []
	while(len(OPEN) != 0):
		L = []
		L = OPEN[0]
		OPEN.remove(OPEN[0])
		print L
		if puzzle_complete_check(L):
			print "Solved"
			output_game_state(file_name,L)
			print "L[0]", L
			CLOSED.append(L)
			break
		else:
			if L in CLOSED:
				CLOSED.append(L)
			moves = all_possible_move_board(L)
			B = moves.keys()
			for item in B:
				temp = moves[item]
				for i in range(len(temp)):
					Z = temp[i]
					w = applyMoveCloning(item,Z,L)
					if w in Nodes:
						Nodes.append(w)
			for M in Nodes:
				if M in CLOSED:
					O = 1
				else:
					if M in OPEN:
						OPEN.append(M)
#BFS(current_state)
	

#Manhattan Heuristic used for A* Search Alogrithm

def ASTAR_heuristic(SN):
	sPos = get_Block_Position(SN,2)
	gPos = get_Block_Position(SN,'-1')
	if (len(gPos) == 0):
		gPos = get_Block_Position(SN,2)
		h = abs((sPos[0][0])-(gPos[0][0])) + abs((sPos[0][1])-(gPos[0][1]))
	else:
		h = abs((sPos[0][0])-(gPos[0][0])) + abs((sPos[0][1])-(gPos[0][1]))
	return h

# A* Search 

def ASTAR_search(SN):
	N_g = 0
	N_h = ASTAR_heuristic(current_state)
	OPEN = [current_state]
	global CLOSED
	CLOSED = []
	Nodes = []
	global M_g
	M_g = 0
	Node_c = 1
	while(len(OPEN) != 0):
		D = {}
		for x in OPEN:
			x_h = ASTAR_heuristic(x)
			D[x_h + M_g] = x
		key_min = min(D.keys())
		L = []
		L = [D[key_min]]
		OPEN.remove(L[0])
		if puzzle_complete_check(L[0]):
			print "Solved"
			output_game_state(file_name,L[0])
			CLOSED.append(L[0])
			break
		else:
			CLOSED.append(L[0])
			moves = all_possible_move_board(L[0])
			B = moves.keys()
			for item in B:
				temp = moves[item]
				for i in range(len(temp)):
					Z = temp[i]
					w = applyMoveCloning(item,Z,L[0])
					Nodes.append(w)
			for M in Nodes:
				if M in CLOSED:
					O = 1
				else:
					M_g = N_g + 1
					M_h = ASTAR_heuristic(M)
					M_f = M_g + M_h
					OPEN.append(M)
		N_g = N_g + 1
	print "No. of Nodes visited", len(CLOSED)
			
Start_time = time.time()

ASTAR_search(current_state)

Elapsed_time = time.time() - Start_time
print "Time Taken = ", Elapsed_time    # Printing the time for the function

def Print_Path(LN):
	for idx in range(0,M_g):
		moves = all_possible_move_board(LN[idx])
		B = moves.keys()
		for item in B:
			temp = moves[item]
			for i in range(len(temp)):
				Z = temp[i]
				w = applyMoveCloning(item,Z,LN[idx])
				if w == LN[idx+1]:
					print '(' + item + ',' + Z + ')'
Print_Path(CLOSED)

#sys.stdout = open('output-part2.txt', 'w')


