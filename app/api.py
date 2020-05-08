import json
import logging
import subprocess
import time
from flask import Flask, request
from flask_cors import CORS, cross_origin
from classes.controller import Controller

app = Flask(__name__)
CORS(app)

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

controller = Controller(logger)

@app.route('/lighthouse', methods=['POST'])
@cross_origin()
def lighthouse():
    job_id = str(int(time.time()*1000))
    url = request.json['url']
    if not url.startswith('http://') or not url.startswith('https://'):
    	url = 'http://{}'.format(url)
    result = controller.enqueue(job_id=job_id, url=url)
    return result, 200

@app.route('/lighthouse_results/<job_id>')
@cross_origin()
def lighthouse_results(job_id):
    results = controller.get_result(job_id=job_id)
    return json.dumps(results)