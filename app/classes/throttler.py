import collections
import json
import subprocess
import time

from threading import Thread

class Throttler:

    def __init__(self, logger):
        self.logger = logger
        self.queue = collections.deque()
        self.results = collections.defaultdict(str)
        dequeuer = Thread(group=None, target=self.dequeue)
        dequeuer.start()


    def enqueue(self, job_id, url):
        self.queue.append((job_id, url))

    def place_in_line(self, job_id):
        place_in_line = -1
        for i, obj in enumerate(self.queue):
            if job_id == obj[0]:
                place_in_line = i
                break
        return {'place_in_line': place_in_line+1}

    def fetch(self, job_id):
        if self.results[job_id]:
            results = self.results[job_id]
            del self.results[job_id]
        else:
            results = {'status': 'pending'}
        return results

    def dequeue(self):
        while True:
            self.logger.info('dequeuing')
            if self.queue:

                try:
                    job_id, url = self.queue.popleft()
                    self.logger.info('dequeued {}'.format(job_id))
                    cmd = 'lighthouse {} --output json --quiet --chrome-flags="--headless --disable-gpu --no-sandbox"'.format(url)
                    lighthouse_result = subprocess.check_output(cmd, shell=True).decode('utf-8')
                    with open('/app/reports/{}.json'.format(job_id), 'w') as file:
                        file.write(lighthouse_result)
                    self.results[job_id] = {'status': 'complete', 'results': json.loads(lighthouse_result)}
                except Exception as e:
                    self.results[job_id] = {'status': 'error', 'message': '{}'.format(e)}

            time.sleep(5)
