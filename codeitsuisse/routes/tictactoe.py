import logging
import json
import requests
import sseclient
import pprint

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/tic-tac-toe', methods=['POST'])
def evaluateTicTacToe():
    data = request.get_json()

    headers = {'Accept': 'text/event-stream'}

    event = requests.get("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + data["battleId"], stream=True, headers=headers)

    print(data)
    print(event)

    client = sseclient.SSEClient(event)
    for event in client.events():
        # pprint.pprint(json.loads(event.data))
        print(event.data)
    


