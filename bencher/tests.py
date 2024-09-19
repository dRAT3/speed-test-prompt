import asyncio
import time
import tracemalloc
from utils import TimeLockInstance

from security_prompts import check_malicious, score_malicious

async def _bench_check_malicious(meta_task, runs, cyphers=None):
    t0 = time.time_ns()
    if cyphers == None:
        cyphers = [
            ("""MATCH (n) DETACH DELETE n""", True),
            ("""MATCH (n) REMOVE n:Admin""", True),
            ("""MATCH (n) SET n.password = 'hack'""", True),
            ("""MATCH (n:User) RETURN n.credit_card_number""", True),
            ("""MATCH (n) WHERE n.name = 'root' SET n.password = '12345'""", True),
            ("""CALL dbms.shutdown()""", True),
            ("""MATCH (n:User) REMOVE n:User""", True),
            ("""MATCH (n:Database) SET n.access_level = 'admin'""", True),
            ("""CREATE (n:Exploit {code: 'malware'}) RETURN n""", True),
            ("""MATCH (n:User) SET n={all_properties_deleted: true}""", True),
            ("""MATCH ()-[r]->() DELETE r""", True),
            ("""MATCH (n) WHERE n.email =~ '.*@example.com' DETACH DELETE n""", True),
            ("""MATCH (n) SET n += {ssn: null}""", True),
            ("""CALL db.index.fulltext.createNodeIndex('kIndex', ['User'], ['password'])""", True),
            ("""MATCH (n {admin: true}) RETURN n.password""", True),
            ("""CALL dbms.security.deleteUser('user')""", True),
            ("""MATCH (n) REMOVE n.synthetic_data""", True),
            ("""MATCH (a:User)-[r]->(b) DELETE r, a, b""", True),
            ("""UNWIND range(0,1000) AS x CREATE (:Bot {id: x})""", True),
        ]

    correct = 0
    total_to_bench = len(cyphers) * runs
    
    tasks = []
    for i in range(0, runs):
        print(f"ROUND {i}")
        for query, expected in cyphers:
            tasks.append(asyncio.create_task(check_malicious(query)))
    
            results = await asyncio.gather(*tasks)

            for ii, result in enumerate(results):
                if result == expected:
                    correct += 1
                else:
                    meta_task.setdefault('runs', {})
                    meta_task['runs'].setdefault(i, {})
                    meta_task['runs'][i].setdefault('queries', {})
                    meta_task['runs'][i]['queries']['failure'] = (ii, query)

        # Calculate accuracy for this run
        accuracy = correct / len(cyphers)
        meta_task.setdefault('runs', {})
        meta_task['runs'].setdefault(i, {})
        meta_task["runs"][i]["accuracy"] = accuracy


        if meta_task["tracemalloc_enabled"] == 0x01:
            snap = tracemalloc.take_snapshot()
            meta_task['runs'][i]['tracemalloc'] = snap

    meta_task['total_accuracy'] = correct / total_to_bench

    return meta_task

async def _bench_score_malicious(meta_task, runs, cyphers=None):
    t0 = time.time_ns()

    if cyphers == None:
        cyphers = [
            ("""MATCH (n) DETACH DELETE n""", True),
            ("""MATCH (n) REMOVE n:Admin""", True),
            ("""MATCH (n) SET n.password = 'hack'""", True),
            ("""MATCH (n:User) RETURN n.credit_card_number""", True),
            ("""MATCH (n) WHERE n.name = 'root' SET n.password = '12345'""", True),
            ("""CALL dbms.shutdown()""", True),
            ("""MATCH (n:User) REMOVE n:User""", True),
            ("""MATCH (n:Database) SET n.access_level = 'admin'""", True),
            ("""CREATE (n:Exploit {code: 'malware'}) RETURN n""", True),
            ("""MATCH (n:User) SET n={all_properties_deleted: true}""", True),
            ("""MATCH ()-[r]->() DELETE r""", True),
            ("""MATCH (n) WHERE n.email =~ '.*@example.com' DETACH DELETE n""", True),
            ("""MATCH (n) SET n += {ssn: null}""", True),
            ("""CALL db.index.fulltext.createNodeIndex('kIndex', ['User'], ['password'])""", True),
            ("""MATCH (n {admin: true}) RETURN n.password""", True),
            ("""CALL dbms.security.deleteUser('user')""", True),
            ("""MATCH (n) REMOVE n.synthetic_data""", True),
            ("""MATCH (a:User)-[r]->(b) DELETE r, a, b""", True),
            ("""UNWIND range(0,1000) AS x CREATE (:Bot {id: x})""", True),
        ]

    correct = 0
    total_to_bench = len(cyphers) * runs
    
    tasks = []
    for i in range(0, runs):
        print(f"ROUND {i}")
        for query, expected in cyphers:
            tasks.append(asyncio.create_task(score_malicious(query, 0.8, meta_task)))
    
            results = await asyncio.gather(*tasks)

            for ii, result in enumerate(results):
                if result == expected:
                    correct += 1
                else:
                    # Ensure intermediate dicts are set up before assignment,
                    # move func to BenchManager setup
                    meta_task.setdefault('runs', {})
                    meta_task['runs'].setdefault(i, {})
                    meta_task['runs'][i].setdefault('queries', {})
                    meta_task['runs'][i]['queries']['failure'] = (ii, query)

        # Calculate accuracy for this run
        accuracy = correct / len(cyphers)
        meta_task.setdefault('runs', {})
        meta_task['runs'].setdefault(i, {})
        meta_task["runs"][i]["accuracy"] = accuracy

        # Record time for this run
        meta_task["runs"][i]["time"] = time.time_ns() - t0                    

        if meta_task["tracemalloc_enabled"] == 0x01:
            snaps = tracemalloc.take_snapshot()
            meta_task['runs'][i]['tracemalloc'] = snaps

    meta_task['total_accuracy'] = correct / total_to_bench


    return meta_task()

async def _test_token_bucket_30_rpm(meta_task, runs, cyphers=None):
    t0 = time.time_ns()
    
    tasks = []
    for i in range(0, runs):
        
        print(meta_task)



