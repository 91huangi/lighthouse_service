import logging
import subprocess
import time
from flask import Flask

app = Flask(__name__)

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

@app.route('/lighthouse')
def lighthouse():
	lighthouse_output = subprocess.check_output('lighthouse http://18.222.118.221 --output json --quiet --chrome-flags="--headless --disable-gpu --no-sandbox"', shell=True)
	with open('/api/reports/asdf.json', 'w') as file:
		file.write(lighthouse_output.decode('utf-8'))
	return ''