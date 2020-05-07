import collections
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
        return len(self.queue)

    def fetch(self, job_id):
        return self.results[job_id]

    def dequeue(self):
        while True:
            self.logger.info('dequeuing')
            if self.queue:
                job_id, url = self.queue.popleft()
                self.logger.info('dequeued {}'.format(job_id))
                cmd = 'lighthouse {} --output json --quiet --chrome-flags="--headless --disable-gpu --no-sandbox"'.format(url)
                lighthouse_result = subprocess.check_output(cmd, shell=True)
                with open('/app/reports/{}.json'.format(job_id), 'w') as file:
                    file.write(lighthouse_result.decode('utf-8'))
                self.results[job_id] = lighthouse_result
            time.sleep(5)
