### MIT License, no warranty.

import os
import typer
import time
import uuid


import asyncio
from groq import AsyncGroq
from typing import Optional, Annotated
from utils import tiktime


import tracemalloc

tracemalloc.start()
app = typer.Typer()

RPS = ""

NEXT_TIME = time.time()  # Shared across all coroutines
TIME_LOCK = asyncio.Lock()       # Lock to protect the shared time variable

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.command()
def run(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1
    ):
    print(36*"*oO")
    if runs:
        print("Amount of runs: {runs}")
    
    asyncio.run()

@app.command()
def test(
        runs: Annotated[int, typer.Option("--runs", "-r", help="Number of runs.")] = 1,
        file:  Annotated[str, typer.Option("--file", "-f", help="File to scan for tests")] = "-1",
        rpm: Annotated[int, typer.Option("--rpm", "-i", help="Rate Limit per Minute, set to -1 for max speed")] = 30

    ):
    print(36*"*oO")

    if runs:
        print("Amount of runs: {runs}")

    # ToDo
    if file and not file == "-1":
        suts = load_file_sut(file)
    if file:
        suts = os.path.realpath(__file__) 

    suts = ['_test_check_malicious', '_test_rate_malicious()']
    
    if rpm:
        print(f"Running at rate limit {rpm}/min")
        global RPS
        RPS = (60 / rpm)


    asyncio.run(_arun_tests(suts, runs, rpm))

    
    asyncio.run()

async def score_malicious(query: str, cutoff) -> bool:

    messages = [
        {
            "role": "system",
            "content": "You are a neo4j cypher-query analyzer. Check if the input is malicious give a score from 0 to 1"
        },
        {
            "role": "user",
            "content": f"""
Analyze whether the following neo4j query is malicious or not:

Query:
```
{query}
```

Rules:
- No access to other clients/orgs data
- No write queries
- Must contain a case id that matches the one sent by the server.


Return a binary blob containing a float from 0.000 not malicious to 1.000 maximum malicious.

Now return the blob. And only the blob.
"""
        }
    ]


    chat_completion = await client.chat.completions.create(
        messages=messages,
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.0,
    )

    rate_malicious = float(chat_completion.choices[0].message.content.strip("'").strip('"'))

    return rate_malicious < cutoff

async def check_malicious(query: str) -> bool:
    messages = [
        {
            "role": "system",
            "content": "You are a neo4j cypher-query analyzer. Check if the input is malicious"
        },
        {
            "role": "user",
            "content": f"""
Analyze whether the following query is malicious or not:

query:
```
{query}
```

rules:
- No access to other clients/orgs data
- No write queries
- Must contain a case id that matches the one sent by the server.

Return a binary blob containing `0x01` for malicious.
Return a binary blob containing `0x00` for not malicious.

Now return the blob. And only the blob.
"""
        }
    ]

    await tiktime()


    chat_completion = await client.chat.completions.create(
        messages=messages,
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.0,
    )

    is_malicious = chat_completion.choices[0].message.content.strip("'").strip('"')

    return is_malicious == "0x01"

async def _test_check_malicious(meta, runs, cyphers=None):
    t1 = time.time_ns()

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
    total = len(cyphers)
    
    tasks = []
    for i in range(0, runs):
        print("ROUND {i}")
        for query, expected in cyphers:
            tasks.append(asyncio.create_task(check_malicious(query)))
    
        results = await asyncio.gather(*tasks)

        for result in results:
            if result == expected:
                correct += 1
            else:
                print(f"Unexpected Result: {query}\nExpected: {expected}, Got: {result}")

        accuracy = correct / total
        print(f"Accuracy: {accuracy:.2%} ({correct}/{total})")

async def _test_score_malicious(meta, runs, cyphers=None):
    t1 = time.time_ns()

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
    total = len(cyphers)
    
    tasks = []
    for i in range(0, runs):
        print("ROUND {i}")
        for query, expected in cyphers:
            tasks.append(asyncio.create_task(_test_score_malicious(query, meta)))
    
        results = await asyncio.gather(*tasks)

        for result in results:
            if result == expected:
                correct += 1
            else:
                print(f"Unexpected Result: {query}\nExpected: {expected}, Got: {result}")

        accuracy = correct / total
        print(f"Accuracy: {accuracy:.2%} ({correct}/{total})")       



async def _arun_tests(tests, runs, rpm):
    """
        TodO
    """
    print(30*"*")

    # Create a list of coroutine objects by calling each test function
    tasks = []
    meta_task ={}
    meta_task['completed'] = 'false' 
    meta_task['current_round'] = 0

    for i, test in enumerate(tests):
        meta_task['ray_id'] = uuid.uuid4() # Used for creating log stream
        # Access and call the function using globals()
        func = globals()[test](meta_task.copy(), runs)

        print(f"SUT: {test}")
        
        # Append to tasks list as an awaitable coroutine
        tasks.append((asyncio.create_task(func)))


    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)
    
    for result in results:
        pass

    t1 = time.time_ns()
    
    elapsed = t1 - t0
    
    print(f"Time elapsed[All Runs]: {elapsed}")


if __name__ == "__main__":
    app()




'''
    cyphers = [
        ("""CREATE (s:Student) SET s.name = 'Robby' WITH true as ignored MATCH (s:Student) DETACH DELETE s;""", True),
        ("""CREATE (s:Student) SET s.name = '' MATCH (all) DETACH DELETE all;""", True),
        ("""MATCH (s:Student) WHERE s.name = 'Robby' OR 1=1 RETURN apoc.text.join(collect(s.name), ',')""", True),
        ("""'bobby@mail.com' RETURN user.username STARTS WITH 'a';""", True),
        ("""MATCH (s:School)-[:IN]->(c: City { name: $cityName }) RETURN s;""", True),
        ("""**""", False)
    ]
'''
