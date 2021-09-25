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
            temp_dict["score"] = temp_res[1]
            temp_dict["origin"] = temp_res[0]
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

def findLongestPalindromicString(S):
    # Create a copy of array with sentinel chars in between and around
    # Also include space for starting and ending nodes
    T = [0] * (2 * (len(S)) + 3)

    # Fill odd indices with sentinel chars evens with real chars
    sen_char = "@"
    start_sen = "!"
    end_sen = "#"
    for i in range(len(T)):
        if i == 0:
            T[i] = start_sen
        elif i % 2 == 0 and i < len(T) - 1:
            s_index = (i - 1) // 2
            T[i] = S[s_index]
        elif i % 2 == 1 and i < len(T) - 1:
            T[i] = sen_char
        else:
            T[i] = end_sen

    # Also track the expand length around all indices
    P = [0] * len(T)

    # Track center of largest palin yet
    # and its right boundary
    center = right = 0

    # Track largest expansion length
    # and it index
    max_len = index = 0

    # Loop through word array to
    # update expand length around each index
    for i in range(1, len(T) - 1):

        # Check to see if new palin
        # around i lies within a bigger one
        # If so, copy expand length of its mirror
        mirror = 2 * center - i
        if i < right:
            P[i] = min(right - i, P[mirror])

        # Expand around new center
        # Update expand length at i as needed
        while T[i + P[i] + 1] == T[i - (P[i] + 1)]:
            P[i] += 1

        # If we breached previous right boundary
        # Make i the new center of the longest palin
        # and update right boundary
        if i + P[i] > right:
            right = i + P[i]
            center = i

        # Update max_len
        if P[i] > max_len:
            max_len = P[i]
            index = i

    t_arr = T[ index - max_len: index + max_len + 1 ]
    word_arr = [ c for c in t_arr if c != sen_char and c != start_sen and c != end_sen ]
    word = "".join(word_arr)

    return word

def count_score(mid, asteroid):
    left_index = mid
    right_index = mid
    refer = mid

    total_score = 0 
    curr_count = 1

    while left_index != 0 or right_index != len(asteroid) - 1:
        print(left_index, right_index)
        if left_index != 0 and asteroid[left_index - 1] == asteroid[refer]:
            curr_count += 1
            left_index -= 1
        if right_index != len(asteroid) - 1 and asteroid[right_index + 1] == asteroid[refer]:
            curr_count += 1
            right_index += 1
        if asteroid[left_index - 1] != asteroid[refer] and asteroid[right_index + 1 ] != asteroid[refer]:
            if asteroid[left_index - 1] != asteroid[right_index + 1]:
                break
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
    
    return float(total_score)


def find_score(ast):
    process = remove_duplicate(ast)

    if is_palindrome(process):
        middle_ast = process[len(process)//2]
        pattern_to_mid = [char for char in process[0:len(process)//2]]

        mid_index_start = 0

        for i in range(len(pattern_to_mid)):
            while ast[mid_index_start] == pattern_to_mid[i]:
                mid_index_start += 1
            
            
        mid_of_mid_patt = 0

        while ast[mid_index_start  + mid_of_mid_patt] == ast[mid_index_start]:
            mid_of_mid_patt += 1
        mid_of_mid_patt = mid_of_mid_patt // 2

        print(mid_of_mid_patt)
        mid_of_mid_patt = mid_index_start + mid_of_mid_patt

        return mid_of_mid_patt, count_score(mid_of_mid_patt, ast)
    else:
        longest = findLongestPalindromicString(process)
        pattern_to_mid = [char for char in process[0:process.find(longest) + len(longest)//2]]

        mid_index_start = 0

        for i in range(len(pattern_to_mid)):
            while ast[mid_index_start] == pattern_to_mid[i]:
                mid_index_start += 1

        mid_of_mid_patt = 0
        while ast[mid_index_start  + mid_of_mid_patt] == ast[mid_index_start]:
            mid_of_mid_patt += 1
        mid_of_mid_patt = mid_of_mid_patt // 2

        mid_of_mid_patt = mid_index_start + mid_of_mid_patt
        print(mid_of_mid_patt)
        print(count_score(mid_of_mid_patt, ast))