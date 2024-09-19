import time
import asyncio
import uuid
import logging

import tracemalloc

from bencher.benches import _bench_check_malicious, _bench_score_malicious 
from bencher.tests import _test_bucket_rate_limit_30

class BenchRunner:
    def __init__(self, tests, rpm, tm = 0x00, runs = 1):
        """
        Initialize the TestRunner with the list of tests, runs, and requests per minute (rpm).
        """
        self.tests = tests
        self.runs = runs
        self.rpm = rpm
        self.meta = {}
        self.meta_task = {
            'completed': 'false',
            'current_round': 0,
            'ray_id': 0x42
        }
        self.tasks = []
        self.tm = tm
        self.logger = logging.getLogger("__name__")

    def prepare_meta_task(self, task: str):
        """
        Prepare meta_task for each test run.
        """
        self.meta_task['ray_id'] = uuid.uuid4()  # Used for creating log stream
        self.meta_task['t1'] = time.time_ns()
        self.meta_task["name"] = task 

        if self.tm == 0x00:
            return self.meta_task

        try:
            tracemalloc.start()
            self.meta_task['tracemalloc_enabled'] = 0x01
            snaps: tracemalloc.Snapshot = tracemalloc.take_snapshot()
             
            self.logger.info(6 * "*")
            self.logger.info(f"{snaps}")
            self.logger.info(1 * "*")
            self.logger.info(f"{self.meta_task}")
            self.logger.info(6 * "*")

        except Exception as e:
            self.logger.error("Tracemalloc failed to load")
            

        return self.meta_task.copy()
    
    async def arun_tests(self):
        """
        Run the tests asynchronously
        """
        print(33 * "*")
        self.logger.info("Started Timer")
        t0 = time.time_ns()  # Start time tracking

        # Iterate through the tests and schedule them with rate limiting
        for i, test in enumerate(self.tests):

            # Prepare the metadata for each test
            meta_task = self.prepare_meta_task(test)
            
            # Call the function using globals
            func = globals()[test](meta_task, self.runs)

            # Run the test as an asyncio task and append it to the list
            task = asyncio.create_task(func)
            
            self.tasks.append(task)
            
        # Run all tasks concurrently
        results = await asyncio.gather(*self.tasks)

        for result in results:
            # Process results (currently just passing)
            print(result)
            pass

        t1 = time.time_ns()
        elapsed = t1 - t0
        print(f"Time elapsed[All Runs]: {elapsed / 1e9} seconds")

    @classmethod
    async def scan_file(cls, file):
        pass

# Usage Example
# Assuming you have defined global functions for your tests
#tests = ['test_function_1', 'test_function_2']
#runner = TestRunner(tests, runs=5, rpm=30)
#asyncio.run(runner.run_tests())
