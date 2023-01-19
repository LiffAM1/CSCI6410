# Name: Abigail Holloway
# Email: hollowayab21@students.ecu.edu
# Date: 10/17/2022
# Class: CSCI6410
# Assignment: Assignment 3 - Kosaraju Sharir
# Execution instructions:
#   Run this program using the command format:
#       python3 kosaraju_sharir.py
#   The program accepts inputs one at a time and validates each input for correct formatting
import sys

class KosarajuSharir:
	nodesCount = -1 
	edgesCount = -1

	graph = {}
	reverseGraph = {}
	topological = []
	connectedComponents = {}
	currentComponent = 0
	phase = 0
	discoveredInit = {}

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
		self.graph = {n:[] for n in range(0,self.nodesCount)}
		self.reverseGraph = {n:[] for n in range(0,self.nodesCount)}

		# Hash map to use during dfs for O(1) access time complexity to check if any node has been discovered
		self.discoveredInit = { n:False for n in range(0,self.nodesCount) }

		# Accept input for the edges from stdin
		edgesInput = 1 
		while edgesInput <= self.edgesCount:
			newEdge = input(f"Please enter edge {edgesInput} of {self.edgesCount}: ")
			orderedPair = []
			try :
				vertices = newEdge.split(" ")
				if len(vertices) != 2:
					raise
				for v in vertices:
					node = int(v)
					if node not in self.graph.keys():
						raise
					orderedPair.append(node)
			except BaseException: 
				print("Input was an invalid format. Please try again.")
				continue
				

			# Add the new edge to the graph and reverse graph now to save time later
			self.graph[orderedPair[0]].append(orderedPair[1])
			self.reverseGraph[orderedPair[1]].append(orderedPair[0])

			edgesInput+=1


		# Run the Kosaraju Sharir algorithm phases
		self.phaseOne()
		self.phaseTwo()

		# Print the resulting connected components
		print(f"The given graph has {len(self.connectedComponents)} Strongly Connected Components.")
		for scc,n in self.connectedComponents.items():
			n.sort()
			print(f"Strongly Connected Component #{scc}: {', '.join([str(i) for i in n])}")
		self.constructKernelGraph()

	def phaseOne(self):
		self.phase = 1

		discovered = self.discoveredInit.copy()

		# Run dfs on the reverse graph until all nodes have been inserted into the topological ordering
		nextNode = 0
		while len(self.topological) < self.nodesCount:
			self.dfs(nextNode,discovered,self.reverseGraph)
			remaining = list(set(range(0,self.nodesCount))-set(self.topological))
			if remaining:
				nextNode = remaining[0]

	def phaseTwo(self):
		self.phase = 2
		self.currentComponent = 0

		discovered = self.discoveredInit.copy()

		# We'll insert a -1 at the beginning of the topological list so that we know that all the nodes
		# have been popped from the stack and processed when we reach the -1
		self.topological.insert(0,-1)

		# Pop elements from the end of the topological stack and run dfs until all nodes have been discovered
		nextNode = self.topological.pop()
		while nextNode >= 0:
			self.connectedComponents[self.currentComponent] = []
			self.dfs(nextNode,discovered,self.graph)
			while self.topological and discovered[nextNode]:
				nextNode = self.topological.pop()
			self.currentComponent = self.currentComponent+1

	# DFS utility for use in the two phases of the algorithm
	def dfs(self,node, discovered, graph):
		if not discovered[node]:
			discovered[node] = True
			# If we are in phase 2, add the node to the current connected component
			if self.phase == 2:
				self.connectedComponents[self.currentComponent].append(node)
			for neighbor in graph[node]:
				self.dfs(neighbor,discovered,graph)
			# If we are in phase 1, once dfs has finished for all neighbors, add the node
			# to the end of the topological ordering
			if self.phase == 1:
				self.topological.append(node)

	def constructKernelGraph(self):
		kernelGraph = {n:[] for n in self.connectedComponents.keys()}

		# For each node in the kernel DAG, figure out which other nodes it connects to
		for scc,nodes in self.connectedComponents.items():
			for otherNode in kernelGraph.keys():
				if otherNode == scc:
					continue
				done = False
				for i in nodes:
					for j in self.connectedComponents[otherNode]:
						if j in self.graph[i]:
							kernelGraph[scc].append(otherNode)
							done = True
							break
					if done:
						break

		# Print result using same format as the graph input
		print("The Kernel Graph for the input is:")
		for k,e in kernelGraph.items():
			for n in e:
				print(f"{k} {n}")

KosarajuSharir()
