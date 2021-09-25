import logging
import json
import requests

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
def evaluateTicTacToe():
    data = request.get_json()

    headers = {'Accept': 'text/event-stream'}

    event = requests.get("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + data["battleId"], stream=True, headers=headers).json()

    print(data)
    print(event)


