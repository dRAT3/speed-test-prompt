import asyncio
import time
import tracemalloc

from security_prompts import check_malicious, score_malicious

async def _bench_check_malicious(meta_task, runs, cyphers=None):
    t0 = time.time_ns()
    print(f"[{meta_task['task_name']}]Starting _bench_check_malicious at {t0} ns")
    
    if cyphers is None:
        print("No cyphers provided, using default set")
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
    print(f"[{meta_task['task_name']}]Total queries to benchmark: {total_to_bench}")
    
    tasks = []
    for i in range(0, runs):
        print(f"{__name__}.{meta_task['name']}--ROUND {i}")
        for query, expected in cyphers:
            print(f"Running check_malicious for query: {query}")
            tasks.append(asyncio.create_task(check_malicious(query)))
    
        results = await asyncio.gather(*tasks)
        print(f"[{meta_task['task_name']}]Results for round {i}: {results}")

        for ii, result in enumerate(results):
            if result == expected:
                correct += 1
            else:
                print(f"[{meta_task['task_name']}]Failure in run {i} for query {ii}: {query}")
                meta_task.setdefault('runs', {})
                meta_task['runs'].setdefault(i, {})
                meta_task['runs'][i].setdefault('queries', {})
                meta_task['runs'][i]['queries']['failure'] = (ii, query)

        # Calculate accuracy for this run
        accuracy = correct / len(cyphers)
        print(f"Accuracy for run {i}: {accuracy}")
        meta_task.setdefault('runs', {})
        meta_task['runs'].setdefault(i, {})
        meta_task["runs"][i]["accuracy"] = accuracy

        if meta_task["tracemalloc_enabled"] == 0x01:
            snap = tracemalloc.take_snapshot()
            print(f"Tracemalloc snapshot taken for run {i}")
            meta_task['runs'][i]['tracemalloc'] = snap

    meta_task['total_accuracy'] = correct / total_to_bench
    print(f"[{meta_task['task_name']}]Total accuracy: {meta_task['total_accuracy']}")

    return meta_task

async def _bench_score_malicious(meta_task, runs, cyphers=None):
    t0 = time.time_ns()
    print(f"[{meta_task['task_name']}]Starting _bench_score_malicious at {t0} ns")

    if cyphers is None:
        print("[{meta_task['task_name']}]No cyphers provided, using default set")
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
    print(f"[{meta_task['task_name']}] - Total queries to benchmark: {total_to_bench}")
    
    tasks = []
    for i in range(0, runs):
        print(f"{__name__}.{meta_task['name']}--ROUND {i}")
        for query, expected in cyphers:
            print(f"[{meta_task['task_name']}]Running score_malicious for query: {query}")
            tasks.append(asyncio.create_task(score_malicious(query, 0.8, meta_task)))
    
        results = await asyncio.gather(*tasks)
        print(f"[{meta_task['task_name']}]Results for round {i}: {results}")

        for ii, result in enumerate(results):
            if result == expected:
                correct += 1
            else:
                print(f"[{meta_task['task_name']}]Failure in run {i} for query {ii}: {query}")
                meta_task.setdefault('runs', {})
                meta_task['runs'].setdefault(i, {})
                meta_task['runs'][i].setdefault('queries', {})
                meta_task['runs'][i]['queries']['failure'] = (ii, query)

        # Calculate accuracy for this run
        accuracy = correct / len(cyphers)
        print(f"[{meta_task['task_name']}]Accuracy for run {i}: {accuracy}")
        meta_task.setdefault('runs', {})
        meta_task['runs'].setdefault(i, {})
        meta_task["runs"][i]["accuracy"] = accuracy

        # Record time for this run
        run_time = time.time_ns() - t0
        print(f"[{meta_task['task_name']}]Run time for round {i}: {run_time} ns")
        meta_task["runs"][i]["time"] = run_time                    

        if meta_task["tracemalloc_enabled"] == 0x01:
            snaps = tracemalloc.take_snapshot()
            print(f"[{meta_task['task_name']}]Tracemalloc snapshot taken for run {i}")
            meta_task['runs'][i]['tracemalloc'] = snaps

    meta_task['total_accuracy'] = correct / total_to_bench
    print(f"[{meta_task['task_name']}]Total accuracy: {meta_task['total_accuracy']}")

    return meta_task
