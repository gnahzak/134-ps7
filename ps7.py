import random
import queue
from datetime import datetime

def main():
  n = 0

  # determine largest node
  for line in open("network.txt"):
    line = line.rstrip("\n")
    fields = line.split()
    if not fields[0] == '#':
      fields[0] = int(fields[0])
      fields[1] = int(fields[1])
      if fields[0] > n:
        n = fields[0]
      elif fields[1] > n:
        n = fields[1]

  # keep each node's neighbors and edge weights as a dict
  n += 1
  adjacency = [{} for j in range(n)]

  # store neighbors
  for line in open("network.txt"):
    line = line.rstrip("\n")
    fields = line.split()
    if not fields[0] == "#":
      fields[0] = int(fields[0])
      fields[1] = int(fields[1])
      fields[2] = float(fields[2])

      adjacency[fields[0]][fields[1]] = fields[2]

  print("The probability of node 42 influencing node 72 is", adjacency[42][75])

  # run genRandGraph 100 times and determine the average number of nodes
  random.seed(datetime.now())
  nodes = 0
  for i in range(100):
    graph = genRandGraph(adjacency)
    for node in range(n):
      if len(graph[node]) > 0:
        nodes += 1
  nodes /= 100
  print("The average number of nodes is", nodes)

  # run sampleInfluence
  print("The influence of S is", sampleInfluence(adjacency, [17, 23, 42, 2017], 500))

def genRandGraph(weights):
  n = len(weights)

  graph = [set() for j in range(n)]

  # go through all edges in weights and decide whether to add them to graph
  for i in range(n):
    for v, w in weights[i].items():
      if random.random() < w:
        graph[i].add(v)

  return graph

def sampleInfluence(G, S, m):

  r = 0
  for i in range(m):
    # randomly realize a graph
    graph = genRandGraph(G)

    # count the number of reachable edges and add it to r

    q = queue.Queue()
    visited = set()

    # add all values in S to q and visited
    for v in S:
      q.put(v)
      visited.add(v)

    #run BFS
    while not q.empty():
      node = q.get()
      # for the node's neighbors, add them to the queue and set as visited
      for neighbor in graph[node]:
        if not (neighbor in visited):
          q.put(neighbor)
          visited.add(neighbor)

    r += len(visited)

  return r / m

if __name__ == "__main__":
    main()
