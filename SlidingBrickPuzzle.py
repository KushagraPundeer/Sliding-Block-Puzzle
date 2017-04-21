#!/bin/python
import random
import sys
file_name = sys.argv[-1]
def load_game_state(file_name):
	txt_file = open(file_name,"r")
 	filelist = txt_file
	first_line = txt_file.readline().split(",")
	global width, height, item, state, orignal_state, current_state
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

def output_game_state(file_name):
	print width + "," + height + ","
	for row in state:
		s = ""
		for item in row:
			s += str(item) + ","
		print s	
output_game_state(file_name)

def clone_state(file_name):
	state = current_state
	output = []
	for row in state:
		l = []
		for item in row:
			l.append(item)
		output.append(l)
	print output
	return output
clone_state(file_name)
def puzzle_complete_check(file_name):
	state = current_state
	for row in state:
		for item in row:
			if int(item) == -1:
				return False 
	print 'Solved'
	return True
def get_Block_Position(state,piece):
	state = current_state
	position = []
	for i in range(0,len(state)):
		for j in range(0,len(state[i])):
			if int(state[i][j]) == int(piece):
				position.append([i,j])
	return position

#get_Block_Position(state,2)

def all_possible_move_piece(piece,state):
	if int(piece) < 2:
		return []
	else:
		state = current_state
		blockPosition = get_Block_Position(state,piece)
		for item in blockPosition:
			vertical = item[0]
			horizontal = item[1]
			output = ["UP","DOWN","RIGHT","LEFT"]              
			# UP move
			up_position = vertical - 1
			if int(state[up_position][horizontal]) != 0:
				output.remove('UP')       
			# DOWN move
			down_position = vertical + 1
			if int(state[down_position][horizontal]) != 0:
				output.remove('DOWN') 
			# LEFT move
			left_position = horizontal - 1
			if int(state[vertical][left_position]) != 0:
				output.remove('LEFT') 
			# RIGHT move
			right_position = horizontal + 1
			if int(state[vertical][right_position]) != 0:
				output.remove('RIGHT')
			return output

def all_possible_move_board(state):
	state = current_state
	piece = {}
	for row in state:
		for item in row:
			if item not in piece and int(item) > 1:
				piece[item] = None               
	for key in piece:
		piece[key] = all_possible_move_piece(key,state)
	print piece
	return piece
all_possible_move_board(state)

def applyMove(piece,direction,state):
  possibleMove = all_possible_move_piece(piece,state)
  if direction not in possibleMove:
    return
  else:
		blockSide = get_Block_Position(state,piece)
		for item in blockSide:
			vertical = item[0]
			horizontal = item[1]
			if direction == "UP":
				new_empty_position = vertical - 1
				state[new_empty_position][horizontal] = piece
				state[vertical][horizontal] = str(0)
			elif direction == "DOWN":
				new_empty_position = vertical + 1
				state[new_empty_position][horizontal] = piece
				state[vertical][horizontal] = str(0)
			elif direction == "LEFT":
				new_empty_position = horizontal - 1
				state[vertical][new_empty_position] = piece
				state[vertical][horizontal] = str(0)
			else:
				new_empty_position = horizontal + 1
				state[vertical][new_empty_position] = piece
				state[vertical][horizontal] = str(0)
		print state
		return state
applyMove(2,"LEFT",state)

def applyMoveCloning(piece,direction,state):
	state = current_state
	new_state = clone_state(state)
	applyMove(piece,direction,new_state)
	return new_state

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
	
def swapIdx(idx1,idx2):
	for i in range(0,int(height)):
		for j in range(0,int(width)):
			if current_state[i][j] == idx1:
				current_state[i][j] = idx2
			elif current_state[i][j] == idx2:
				current_state[i][j] = idx1

def normalizeState(state):
	current_state = state
	nextIdx = 3
	for i in range(0,int(height)):
		for j in range(1,int(width)):
			if current_state[i][j] == nextIdx:
				nextIdx = nextIdx + 1
			if int(current_state[i][j]) > nextIdx:
				swapIdx(nextIdx,current_state[i][j])
				nextIdx = nextIdx + 1
	
	print current_state

normalizeState(state)


def Graph(orignal_state):
	p_node = orignal_state
	Stack = [p_node]
	Stack_current = {}
	Graph_n = dict()
	k = 1
	i = 1
	s = []
	outer = 0
	inner = 0
	counter = 2
	Stack_all = {1:p_node}
	for node in Stack:
		A = all_possible_move_board(node)
		A = A.items()
		for item in A:
			n = applyMoveCloning(int(item[0]),item[1],node)
			if n != None:
				Stack_all[counter] = n
				#Stack_all = {counter: n[k-1]}
				Stack.append(n)
				if n in Stack_all.values():
					return None
				else:
					Stack_current[counter] = n
					#del Stack_current['k']
					Stack_current.keys()
					#Stack.remove(node)
					inner = inner + 1
					if inner == 10:
						return False
					Graph_n[k] = set(Stack_current)
					counter = counter + 1
				k = k + 1
				outer = outer + 1
				if outer == 10:
					return False
				print Graph_n

Graph(orignal_state)

def dfs(graph, start):
	visited, stack = set(), [start]
	while stack:
		vertex = stack.pop()
		if vertex not in visited:
			visited.add(vertex)
		stack.extend(graph[vertex] - visited)
	return visited

def bfs(Graph, start):
	visited, queue = set(), [start]
	while queue:
		vertex = queue.pop(0)
		if vertex not in visited:
			visited.add(vertex)
		queue.extend(graph[vertex] - visited)
	return visited

