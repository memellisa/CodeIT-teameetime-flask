import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()

    print(data)

    result = []

    for testcase in data:
        result.append(find_sol(testcase))

    print(result)
    print(jsonify(result))

    return jsonify(result)


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

def p3(grid):

    grid = getNewGrid(grid)
    timer = 0

    while True:
        spreadCounter = 0
        changes = []
        for i in range(1, len(grid)-1):
            for j in range(1, len(grid[0])-1):
                if grid[i][j] == 3:
                    if grid[i+1][j] == 1:
                        spreadCounter += 1
                        changes.append([i+1, j])
                    if grid[i-1][j] == 1:
                        spreadCounter += 1
                        changes.append([i-1, j])
                    if grid[i][j+1] == 1:
                        spreadCounter += 1
                        changes.append([i, j+1])
                    if grid[i][j-1] == 1:
                        spreadCounter += 1
                        changes.append([i, j-1])
                    if grid[i-1][j-1] == 1:
                        spreadCounter += 1
                        changes.append([i-1, j-1])
                    if grid[i-1][j+1] == 1:
                        spreadCounter += 1
                        changes.append([i-1, j+1])
                    if grid[i+1][j-1] == 1:
                        spreadCounter += 1
                        changes.append([i+1, j-1])
                    if grid[i+1][j+1] == 1:
                        spreadCounter += 1
                        changes.append([i+1, j+1])
        for change in changes:
            grid[change[0]][change[1]] = 3

        if spreadCounter == 0:
            break
        else:
            timer += 1

    infectedGrid = []
    for i in range(1, len(grid)-1):
        infectedGrid.append(grid[i][1:len(grid[i])-1])

    for i in range(len(infectedGrid)):
        for j in range(len(infectedGrid[i])):
            if 1 == infectedGrid[i][j]:
                timer = -1

    return timer


def p2(grid):

    grid = getNewGrid(grid)
    timer = 0

    while True:
        spreadCounter = 0
        changes = []
        for i in range(1, len(grid)-1):
            for j in range(1, len(grid[0])-1):
                if grid[i][j] == 3:
                    if grid[i+1][j] == 1:

                        spreadCounter += 1
                        changes.append([i+1, j])

                    if grid[i-1][j] == 1:

                        spreadCounter += 1
                        changes.append([i-1, j])

                    if grid[i][j+1] == 1:

                        spreadCounter += 1
                        changes.append([i, j+1])

                    if grid[i][j-1] == 1:

                        spreadCounter += 1
                        changes.append([i, j-1])

        for change in changes:
            grid[change[0]][change[1]] = 3

        if spreadCounter == 0:
            break
        else:
            timer += 1

    infectedGrid = []
    for i in range(1, len(grid)-1):
        infectedGrid.append(grid[i][1:len(grid[i])-1])

    for i in range(len(infectedGrid)):
        for j in range(len(infectedGrid[i])):
            if 1 == infectedGrid[i][j]:
                timer = -1

    return timer


def p1(grid, row, col):
    row += 1
    col += 1
    grid = getNewGrid(grid)
    timer = 0
    if grid[row][col] == 2 or grid[row][col] == 0:
        timer = -1
    else:
        while True:
            timer += 1
            spreadCounter = 0
            changes = []
            for i in range(1, len(grid)-1):
                for j in range(1, len(grid[0])-1):
                    if grid[i][j] == 3:
                        if grid[i+1][j] == 1:

                            spreadCounter += 1
                            changes.append([i+1, j])
                            if i+1 == row and j == col:
                                spreadCounter = 0

                        if grid[i-1][j] == 1:

                            spreadCounter += 1
                            changes.append([i-1, j])
                            if i-1 == row and j == col:
                                spreadCounter = 0

                        if grid[i][j+1] == 1:

                            spreadCounter += 1
                            changes.append([i, j+1])
                            if i == row and j+1 == col:
                                spreadCounter = 0

                        if grid[i][j-1] == 1:

                            spreadCounter += 1
                            changes.append([i, j-1])
                            if i == row and j-1 == col:
                                spreadCounter = 0

            for change in changes:
                grid[change[0]][change[1]] = 3

            if spreadCounter == 0:
                break

    if grid[row][col] != 3:
        timer = -1
    return (str(row-1)+","+str(col-1), timer)


def find_sol(inputs):
    output = {}
    for input in inputs:
        
        roomNumber = input["room"]
        grid = input["grid"]
        interestedIndividuals = input["interestedIndividuals"]
        p1_ans = {}
        for individual in interestedIndividuals:
            (key, value) = p1(
                grid, int(individual[0]), int(individual[2]))
            p1_ans[key] = value
        p2_ans = p2(grid)
        p3_ans = p3(grid)

        output["room"] = roomNumber
        output["p1"] = p1_ans
        output["p2"] = p2_ans
        output["p3"] = p3_ans
        
        #change this 
        output["p4"] = 0
    
    return output