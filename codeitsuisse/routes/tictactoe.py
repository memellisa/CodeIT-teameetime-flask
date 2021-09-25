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

    url = "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + data["battleId"]
    print(url)
    stream_response = requests.get(url, stream=True)

    # event = requests.get("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + data["battleId"], stream=True, headers=headers)
    client = sseclient.SSEClient(stream_response)


    for event in client.events():
        print ("got a new event from server")
        pprint.pprint(event.data)

    # print(data)
    # print(event.data)

    # client = sseclient.SSEClient(event)
    # for event in client.events():
    #     # pprint.pprint(json.loads(event.data))
    #     print(event.data)
    


