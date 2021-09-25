import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
    data = request.get_json()

    print(data)

    result = []

    for testcase in data["test_cases"]:
        temp_res = find_score(testcase)
        temp_dict = {}
        if temp_res != None:
            temp_dict["input"] = testcase
            temp_dict["score"] = temp_res[0]
            temp_dict["origin"] = temp_res[1]
        else:
            temp_dict["input"] = testcase
            temp_dict["score"] = 0
            temp_dict["origin"] = 0
        result.append(temp_dict)

    print(result)
    print(jsonify(result))

    return jsonify(result)

def is_palindrome(s):
  return s == s[::-1]

def remove_duplicate(ast):
  result = ast[0]
  for letter in ast:
    if result[-1] != letter:
      result += letter

  return result

def count_score(mid, asteroid):
    left_index = mid
    right_index = mid
    refer = mid

    total_score = 0 
    curr_count = 1

    while left_index != 0 or right_index != len(asteroid) - 1:
        print(left_index, right_index)
        if left_index != 0 and asteroid[left_index - 1] == asteroid[refer] :
            curr_count += 1
            left_index -= 1
        if right_index != len(asteroid) - 1 and asteroid[right_index + 1] == asteroid[refer]:
            curr_count += 1
            right_index += 1
        if asteroid[left_index - 1] != asteroid[refer] and asteroid[right_index + 1 ] != asteroid[refer]:
        # print("hello")
            refer = left_index - 1 #use either left or right index
            if curr_count <= 6:
                total_score += curr_count
            elif curr_count >= 10:
                total_score += 2 * curr_count
            else:
                total_score += 1.5 * curr_count
            # print(curr_count, "A")
            curr_count = 0

    if curr_count <= 6:
        total_score += curr_count
    elif curr_count >= 10:
        total_score += 2 * curr_count
    else:
        total_score += 1.5 * curr_count
    
    return int(total_score)


def find_score(ast):
    process = remove_duplicate(ast)

    if is_palindrome(process):
        middle_ast = process[len(process)//2]
        pattern_to_mid = [char for char in process[0:len(process)//2]]

        mid_index_start = 0

        for i in range(len(pattern_to_mid)):
            while ast[mid_index_start] == pattern_to_mid[i]:
                mid_index_start += 1
            i += 1
            
        mid_of_mid_patt = 0

        while ast[mid_index_start  + mid_of_mid_patt] == ast[mid_index_start]:
            mid_of_mid_patt += 1
        mid_of_mid_patt = mid_of_mid_patt // 2

        mid_of_mid_patt = mid_index_start + mid_of_mid_patt

        return mid_of_mid_patt, count_score(mid_of_mid_patt, ast)