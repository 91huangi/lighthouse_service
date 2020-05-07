import json
import logging
import subprocess
import time
from flask import Flask
from classes.throttler import Throttler

app = Flask(__name__)

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

throttler = Throttler(logger)

@app.route('/lighthouse')
def lighthouse():
    job_id = str(int(time.time()*1000))
    throttler.enqueue(job_id=job_id, url='http://18.222.118.221')
    return job_id, 200

@app.route('/lighthouse_results/<job_id>')
def lighthouse_results(job_id):
    results = throttler.get_result(job_id=job_id)
    return json.dumps(results)