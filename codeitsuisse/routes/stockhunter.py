import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluateStockHunter():
    data = request.get_json()
    
    result = []

    for testcase in data:
        entryPoint = (testcase["entryPoint"]["first"], testcase["entryPoint"]["second"])
        targetPoint = (testcase["targetPoint"]["first"], testcase["targetPoint"]["second"])

        gridDepth = testcase["gridDepth"]
        gridKey = testcase["gridKey"]
        horizontalStepper = testcase["horizontalStepper"]
        verticalStepper = testcase["verticalStepper"]

        ri = {}
        rl = {}
        grid = {}

        for i in range(targetPoint[1] + 1):
            ri[i] = []
            grid[i] = []
            rl[i] = []

        for y in range(targetPoint[1] + 1):
            for x in range(targetPoint[0] + 1):
                # print(x,y)
                tem = find_ri((x,y), entryPoint, targetPoint, horizontalStepper, verticalStepper, rl)
                # print(tem)
                ri[y].append(tem)
                rl[y].append((tem + gridDepth) % gridKey)
                grid[y].append(convert_to_letter(tem, gridDepth, gridKey))
            # print(ri)
        
        print(grid)

        temp_dict = {}
        temp_dict["gridMap"] = [grid[key] for key in grid]

        ### Finding minimum distance 
        gridMap = [grid[key] for key in grid]

        newGrid= getNewGrid(gridMap)
        neighbors = getNeighbors(newGrid)
        # print(neighbors)
        minCost = findPath(neighbors, entryPoint, targetPoint)
        print("Min cost ",minCost)

        temp_dict["minimumCost"] = minCost
        result.append(temp_dict)

    return jsonify(result)


def convert_to_letter(number, gridDepth, gridKey):
  # print(int(number))
  if ((number + gridDepth) % gridKey) % 3 == 0:
    return "L"
  elif ((number + gridDepth) % gridKey) % 3 == 1:
    return "M"
  elif ((number + gridDepth) % gridKey) % 3 == 2:
    return "S"

def get_rl(tup, rl):
    return rl[tup[1]][tup[0]]

def find_ri(tup, entryPoint, targetPoint, horizontalStepper, verticalStepper, rl):
  if tup == entryPoint:
    return 0
  elif tup == targetPoint:
    return 0
  elif tup[1] == 0:
    return tup[0] * horizontalStepper
  elif tup[0] == 0:
    return tup[1] * verticalStepper
  else:
    return get_rl((tup[0] - 1, tup[1]), rl) * get_rl((tup[0], tup[1] - 1), rl)

def findPath(neighbors, entry, target):
    from heapq import heappush, heappop
    frontier = []
    heappush(frontier, (0,[(),entry]))
    explored = set()
    while frontier:
        node = heappop(frontier)
        if node[1][-1] == target:
            return node[0]
        if node[1][-1] not in explored:
            print('Exploring:',node[1][-1],'at cost',node[0])
            explored.add(node[1][-1])
            for child in neighbors[node[1][-1]]:
                newNode = node[1].copy()
                newNode.append(child[1])
                heappush(frontier, (node[0]+child[0],newNode))

def convertToCost(letter):
    if letter == "L":
        return 3
    elif letter == "M":
        return 2
    elif letter == "S":
        return 1

def getNewGrid(grid):
    newColLength = len(grid[0]) + 2
    newGrid = []
    newGrid.append([0] * newColLength)
    for i in range(len(grid)):
        newCol = [0]
        for j in range(len(grid[0])):
            newCol.append(grid[i][j])
        newCol.append(0)
        newGrid.append(newCol)
    newGrid.append([0] * newColLength)
    return newGrid

def getNeighbors(grid):
    neighbors={}
    for i in range(1,len(grid)-1):
        for j in range(1,len(grid[0])-1):
            directions = {
                (i-2,j-1):grid[i-1][j],
                (i,j-1):grid[i+1][j],
                (i-1,j):grid[i][j+1],
                (i-1,j-2):grid[i][j-1]
                }
            list = []
            for key,value in directions.items():
                cost = convertToCost(value)
                if value != 0:
                    list.append((cost,key))
            real_x = i-1
            real_y = j-1
            neighbors[(real_x,real_y)] = list

    return neighbors