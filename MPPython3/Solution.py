import Traversals
from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

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
        ###########################################################################################################
        #This will be paths section
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
        ###################################################################################################################

        #This will be bandwidths section
        bandwidths = {node: self.info["bandwidths"][node] for node in self.graph}
        highestBW = self.info["bandwidths"][sortedNeighborToBW[0]]
        for fln in self.graph[self.isp]:
            #if len(self.graph[fln]) > 1:
            bandwidths[fln] = bandwidths[fln] * 5





        #******************************************************************************************************************
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
