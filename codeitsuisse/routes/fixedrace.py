import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fixedrace', methods=['POST'])
def evaluateFixedRace():
    data = request.get_data(as_text=True)
    

    print(data)

    return "Joseph Jarosz, Caitlin Cully, Nelson Noss, Cortez Carranco, Shona Stanek, Rudolf Ravelo, Alysia Alejandro, Justin Jack, Britt Bisceglia, Amos Alward."


