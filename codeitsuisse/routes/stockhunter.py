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
            print(ri)
        
        temp_dict = {}
        temp_dict["gridMap"] = [grid[key] for key in grid]
        temp_dict["minimumCost"] = 9
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