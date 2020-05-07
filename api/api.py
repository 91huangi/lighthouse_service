import os
import time
from flask import Flask

app = Flask(__name__)

@app.route('/lighthouse')
def lighthouse():
	print('Running lighthouse...')
	# os.system('ls -l')
