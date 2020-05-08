import collections
import json
import subprocess
import time

from threading import Thread
LH_CATEGORIES = ['performance',
                 'pwa-fast-reliable',
                 'pwa-installable',
                 'pwa-optimized',
                 'pwa',
                 'accessibility',
                 'best-practices',
                 'seo']

class Controller:

    def __init__(self, logger):
        self.logger = logger

        self.lighthouse_mapping = collections.defaultdict(list)
        with open('/app/ref/mappings_v5.csv', 'r') as file:
            lines = file.readlines()
        for line in lines[1::]:
            audit, cat, weight = line.split(',')
            self.lighthouse_mapping[audit] = [cat, float(weight)]
        self.logger.info(self.lighthouse_mapping)

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
        return {'job_id': job_id}

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
                    lighthouse_result = self.process_result(raw_results=lighthouse_result)
                    with open('/app/reports/{}.json'.format(job_id), 'w') as file:
                        file.write(json.dumps(lighthouse_result))
                    self.results[job_id] = {'status': 'complete', 'results': lighthouse_result}
                except Exception as e:
                    self.results[job_id] = {'status': 'error', 'message': str(e)}

                self.current_job = int()

            time.sleep(5)


    def process_result(self, raw_results):
        processed_results = dict()
        for category in LH_CATEGORIES:
            processed_results[category] = {'sum': 0, 'total': 0}
        results_dict = json.loads(raw_results)
        audits = results_dict['audits']

        # Example k='speed-index', v='{"score": 0.5, ... }'
        for k, v in audits.items():
            cat_weight = self.lighthouse_mapping[k]
            if not cat_weight:
                continue
            category, weight = cat_weight
            if v['score']:
                processed_results[category][k] = v['score']
                processed_results[category]['sum'] += v['score']*weight
                processed_results[category]['total'] += weight

        for category in LH_CATEGORIES:
            if processed_results[category]['total']:
                processed_results[category]['score'] = round(processed_results[category]['sum']/processed_results[category]['total'], 2)
            else:
                processed_results[category]['score'] = None
        return processed_results
