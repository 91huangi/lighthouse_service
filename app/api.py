import json
import logging
import subprocess
import time
from flask import Flask
from classes.controller import Controller

app = Flask(__name__)

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

controller = Controller(logger)

@app.route('/lighthouse')
def lighthouse():
    job_id = str(int(time.time()*1000))
    controller.enqueue(job_id=job_id, url='http://18.222.118.221')
    return job_id, 200

@app.route('/lighthouse_results/<job_id>')
def lighthouse_results(job_id):
    results = controller.get_result(job_id=job_id)
    return json.dumps(results)