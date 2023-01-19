# Name: Abigail Holloway
# Email: hollowayab21@students.ecu.edu
# Date: 11/20/2022
# Class: CSCI6410
# Assignment: Assignment 5 - Djikstra's algorithm
# Execution instructions:
#   Run this program using the command format:
#       python3 djikstras.py
#   The program accepts inputs one at a time and validates each input for correct formatting
import sys
import copy

class Node:
	def __init__(self,_value):
		self.key = float('inf')
		self.value = _value
		self.explored = False
		self.adjacent = []
		self.shortestPath = []

	def __lt__(self, other):
		return self.key < other.key

	def printOutput(self):
		print(f"\nVertex {self.value}")
		if self.shortestPath:
			print(f"Shortest Distance is {self.key}")
			print(f"Shortest Path is {' '.join([str(p) for p in self.shortestPath])}")
		else:
			print("There is no possible path to this node.")

# Min-heap implementation			
class MinHeap:
	size = 0
	maxsize = -1
	heap = None

	def __init__(self,maxsize):
		self.maxsize = maxsize
		self.heap = [0]*maxsize

	def swap(self, pos1, pos2):
		self.heap[pos1], self.heap[pos2] = self.heap[pos2], self.heap[pos1]

	def parentIndex(self, pos):
		return (pos-1)//2

	def leftIndex(self, pos):
		return 2*pos+1

	def rightIndex(self, pos):
		return 2*pos+2

	def hasLeft(self, pos):
		return self.leftIndex(pos) < self.size

	def hasRight(self, pos):
		return self.rightIndex(pos) < self.size

	def node(self, pos):
		return self.heap[pos]

	def parent(self, pos):
		return self.heap[self.parentIndex(pos)]

	def left(self, pos):
		return self.heap[self.leftIndex(pos)]

	def right(self, pos):
		return self.heap[self.rightIndex(pos)]

	def insert(self, node):
		if self.size < self.maxsize:
			self.heap[self.size] = node
			self.size += 1
			self.swapUp(self.size-1)

	# After inserting at the leaf level, swap the new element up until it is in the right place
	# Recursive; base case is that the current node is greater than its parent and can stay put
	def swapUp(self, pos):
		if self.parentIndex(pos)>=0 and self.parent(pos).key > self.node(pos).key:
			parentPos = self.parentIndex(pos)
			self.swap(parentPos, pos)
			self.swapUp(parentPos)

	# Starting at pos, if the node is greater than either child, swap it down with the smallest one
	# Recursive; base case is that the current node is the min, or there are no children to check
	def heapify(self, pos):
		minIndex = pos
		if self.hasLeft(pos) and self.node(minIndex).key > self.left(pos).key:
			minIndex = self.leftIndex(pos)
		if self.hasRight(pos) and self.node(minIndex).key > self.right(pos).key:
			minIndex = self.rightIndex(pos)

		if minIndex != pos:
			self.swap(pos, minIndex)
			self.heapify(minIndex)

	# Remove the min element (at index 0) by swapping it with a leaf, removing it, and then heapifying
	def pop(self):
		if self.size > 0:
			self.heap[self.size-1], self.heap[0] = self.heap[0], self.heap[self.size-1]
			minNode = self.heap[self.size-1] 
			self.heap[self.size-1] = 0
			self.size-=1
			self.heapify(0)
			return minNode

class Djikstras:
	nodesCount = -1 
	edgesCount = -1

	graph = {}
	minHeap = None

	def __init__(self):

		# Accept input for the number of vertices and number of edges from stdin
		while self.nodesCount < 0:
			numNodes = input('Please input the number of vertices: ')		
			try:
				self.nodesCount = int(numNodes)
			except BaseException:
				print("Input was an invalid format. Please try again.")

		while self.edgesCount < 0:
			numEdges = input('Please input the number of edges: ')		
			try:
				self.edgesCount = int(numEdges)
			except BaseException:
				print("Input was an invalid format. Please try again.")

		# Initialize the adjacency lists (using hash maps here so we can have O(1) access time complexity)
		self.graph = {n:Node(n) for n in range(1,self.nodesCount+1)}

		# Accept input for the edges from stdin
		edgesInput = 1 
		while edgesInput <= self.edgesCount:
			newEdge = input(f"Please enter edge {edgesInput} of {self.edgesCount}: ")
			edgeAndWeight = []
			try:
				parts = newEdge.split(" ")
				if len(parts) != 3:
					raise
				v1 = int(parts[0])
				v2 = int(parts[1])
				w = float(parts[2])
				if v1 not in self.graph.keys() or v2 not in self.graph.keys():
					raise

				edgeAndWeight = [v1,v2,w]

			except BaseException: 
				print("Input was an invalid format. Please try again.")
				continue
				
			# Add the new edge to the node's adjacency list
			self.graph[int(edgeAndWeight[0])].adjacent.append((self.graph[edgeAndWeight[1]],edgeAndWeight[2]))

			edgesInput+=1


		# Initialize the min heap with the starting node 
		start = self.graph[1]
		start.key = float(0)
		start.shortestPath = [1]
		self.minHeap = MinHeap(self.nodesCount)
		self.minHeap.insert(start)

		self.compute()

	def compute(self):
		while self.minHeap.size > 0:
			node = self.minHeap.pop()

			if not node.explored:
				for (neighbor, weight) in node.adjacent:
					distance = node.key + weight
					if distance < neighbor.key:
						neighbor.key = distance
						neighbor.shortestPath = copy.copy(node.shortestPath)
						neighbor.shortestPath.append(neighbor.value)
						self.minHeap.insert(neighbor)
				node.explored = True

		for node in self.graph:
			self.graph[node].printOutput()

Djikstras()

