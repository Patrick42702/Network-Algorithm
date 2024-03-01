import collections

import Traversals
from Traversals import bfs_path
from datetime import datetime
import heapq
from collections import deque
from Simulator import Simulator
import sys
from queue import Queue

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info


    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        paths, bandwidths, priorities = {}, {}, {}
        shortestPaths = Traversals.bfs_path(self.graph, self.isp, self.info["list_clients"])
        tableForPaths = {neighbor: {} for neighbor in self.graph[self.isp]}
        nodeCapacity = {node: 0 for node in self.graph[self.isp]}
        for firstLevelNeighbor in self.graph[self.isp]:
            tableForPaths[firstLevelNeighbor] = self.output_pathBFS(firstLevelNeighbor)
            if firstLevelNeighbor in self.info["list_clients"]:
                paths[firstLevelNeighbor] = [self.isp, firstLevelNeighbor]
        # 1) Construct NodeCapacity Dict... init at {node : 0 }
        # 2) Sort ISP neighbors by BW
        # 3) Loop through clients
        #       Loop through sorted neighbors from step 2.
        #           If NodeCapacity[neighbor] < neighbors bandwidth
        #               If there exists a path from the neighbor to client, set paths[client] to that path
        #               Increment NodeCapacity[neighbor]
        #           Else: Try next neighbor
        #           If all neighbors are maxed out: Reset NodeCapacity[neighbor] to 0
        #
        # 4)
        neighborToBw = {neighbor: self.info["bandwidths"][neighbor] for neighbor in self.graph[self.isp]}
        sortedNeighborToBW = sorted(neighborToBw, key=neighborToBw.get)
        sortedNeighborToBW.reverse()
        for client in self.info["list_clients"]:
            initialCapacity = dict(nodeCapacity)
            for firstLevelNode in sortedNeighborToBW:
                if nodeCapacity[firstLevelNode] < self.info["bandwidths"][firstLevelNode]:
                    if client in tableForPaths[firstLevelNode]:
                        altPath = tableForPaths[firstLevelNode][client]
                        paths[client] = altPath
                        nodeCapacity[firstLevelNode] += 1
                        break
            newCapacity = dict(nodeCapacity)
            if newCapacity == initialCapacity:
                for fln in newCapacity:
                    nodeCapacity[fln] = 0
        for client in self.info["list_clients"]:
            if client not in paths:
                paths[client] = shortestPaths[client]
        print(paths)
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)

    def output_pathBFS(self, start):
        """
        :return: the list of minimum distances from each node to the start node
        """
        visited = {}  # client : T/F
        paths = {}  # client : path from start to client
        queue = deque()
        # Set all nodes to unvisited
        for i in self.graph:
            visited[i] = False

        # Set all first level neighbors to explored
        for neighbor in self.graph[self.isp]:
            visited[neighbor] = True

        visited[self.isp] = True
        queue.append(start)
        paths[start] = [self.isp, start]
        # print(paths)
        while len(queue) > 0:
            curr = queue.popleft()  # curr is a key to a list
            for neighbor in self.graph[curr]:
                if visited[neighbor] == False:
                    if curr == start:
                        paths[neighbor] = [self.isp, start, neighbor]
                        queue.append(neighbor)
                        visited[neighbor] = True
                    else:
                        currList = list(paths[curr])
                        currList.append(neighbor)
                        paths[neighbor] = currList
                        queue.append(neighbor)
                        visited[neighbor] = True
        return paths



    def bandwidthCountsinit(self):
        bandwidthcounts = {}
        for x in self.graph:
            bandwidthcounts[x] = 0
        return bandwidthcounts

    def bfsdepth(self, paths):
        longestPath = []
        for x in paths:
            if len(paths[x]) > len(longestPath):
                longestPath = paths[x]
        return longestPath

    def curbandWidthForTotalLevelinit(self, longestPath):
        bandWidthForTotalLevelInit = {}
        count = len(longestPath)
        #count is set to the deepset level of the bfs tree, where the beginning node starts with 1
        for x in range(0,count):#changing root level to 0 and last level to len - 1
            bandWidthForTotalLevelInit[x] = 0
        return bandWidthForTotalLevelInit

    def totalbandwidthperlevel(self, longestpath, paths):
        totalbandforlevel = {}
        start = self.isp
        distance = self.output_distances(start)
        for x in range(0, len(longestpath)):
            totalbandforlevel[x] = 0
        for i,node in enumerate(distance):#idx = the number of node, node represents the distance
            distanceAtNode = node
            bandwidthAtNode = self.info["bandwidths"][i]
            totalbandforlevel[distanceAtNode] += bandwidthAtNode
        return totalbandforlevel


    def unexplored(self):
        unexplored = {}
        for x in range(0, len(self.graph)):
            unexplored[x] = True
        return unexplored

    def distancePerNode(self):
        distance = {}
        for x in range(0, len(self.graph)):
            distance[x] = 0
        return distance

    def output_distances(self, start):
        """
        :return: the list of minimum distances from each node to the start node
        """
        nodesToExplore = collections.deque()
        nodesExplored = {}
        nodesUnexplored = self.unexplored()
        distancePerNode = self.distancePerNode()
        nodesToExplore.append(start)  #
        nodesExplored[start] = True  #
        distancePerNode[start] = 0  #
        nodesUnexplored.pop(start)
        # mark start node as explored and enqueue it
        count = 0
        while (len(nodesToExplore) != 0):  #
            exploringNode = nodesToExplore.popleft()  #
            for node in self.graph[exploringNode]:  #
                if node not in nodesExplored:  #
                    nodesUnexplored.pop(node)
                    distancePerNode[node] = distancePerNode[exploringNode] + 1  #
                    nodesToExplore.append(node)  #
                    nodesExplored[node] = True  #
                    if distancePerNode[exploringNode] + 1 > count:
                        count = distancePerNode[exploringNode] + 1
        for x in nodesUnexplored:
            distancePerNode[x] = -1
        distancesList = list(distancePerNode.values())

        """
        nodeToDistance = {distance: [] for distance in range(0, count + 1)}
        for idx,distance in enumerate(distancesList):
            nodeToDistance[distance].append(idx)
        """
        return distancesList  # Return empty

    def output_nodesPerLevel(self,count):
        distances = self.output_distances(self.isp)
        nodesAtEachlevel = {num: 0 for num in range(0,count)}
        for x in distances:
            nodesAtEachlevel[x] += 1
        return nodesAtEachlevel