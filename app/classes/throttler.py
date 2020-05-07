import collections
import json
import subprocess
import time

from threading import Thread

class Throttler:

    def __init__(self, logger):
        self.logger = logger
        self.queue = collections.deque()
        self.current_job = int()
        self.results = collections.defaultdict(str)
        dequeuer = Thread(group=None, target=self.dequeue)
        dequeuer.start()


    def get_result(self, job_id):
        place_in_line = self.place_in_line(job_id=job_id)
        if place_in_line:
            return place_in_line
        if job_id == self.current_job:
            return {'status': 'pending'}
        results = self.fetch(job_id=job_id)
        if results:
            return results
        return {'status': 'none'}

    def enqueue(self, job_id, url):
        self.queue.append((job_id, url))

    def place_in_line(self, job_id):
        place_in_line = 0
        for i, obj in enumerate(self.queue):
            if job_id == obj[0]:
                place_in_line = i+1
                break
        result = dict()
        if place_in_line:
            result = {'status': 'queued', 'place_in_line': place_in_line}
        return result

    def fetch(self, job_id):
        results = dict()
        if self.results[job_id]:
            results = self.results[job_id]
            del self.results[job_id]
        return results


    def dequeue(self):
        while True:
            self.logger.info('dequeuing')

            if self.queue:

                job_id, url = self.queue.popleft()
                self.current_job = job_id
                self.logger.info('dequeued {}'.format(job_id))

                try:
                    cmd = 'lighthouse {} --output json --quiet --chrome-flags="--headless --disable-gpu --no-sandbox"'.format(url)
                    lighthouse_result = subprocess.check_output(cmd, shell=True).decode('utf-8')
                    with open('/app/reports/{}.json'.format(job_id), 'w') as file:
                        file.write(lighthouse_result)
                    self.results[job_id] = {'status': 'complete', 'results': json.loads(lighthouse_result)}
                except Exception as e:
                    self.results[job_id] = {'status': 'error', 'message': '{}'.format(e)}

                self.current_job = int()

            time.sleep(5)
