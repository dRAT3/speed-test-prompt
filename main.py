import os
import time
import asyncio
from groq import AsyncGroq

import tracemalloc

tracemalloc.start()

client = AsyncGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

####
#### Todo: 
#### Float instead of code with scoring

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

    chat_completion = await client.chat.completions.create(
        messages=messages,
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0.0,
    )

    is_malicious = chat_completion.choices[0].message.content.strip("'").strip('"')

    return is_malicious == "0x01"

async def _test_check_malicious(meta, cyphers=None):
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

async def _arun_tests(tests):
    """
        TodO
    """
    print(30*"*")

    # Create a list of coroutine objects by calling each test function
    tasks = []
    meta = {'completed': 'false', 't1': time.time() }
    for test in tests:
        # Access and call the function using globals()
        func = globals()[test](meta.copy())

        # Perform additional operations if needed
        print(f"Start test: {test}")
        
        # Append to tasks list as an awaitable coroutine
        tasks.append((asyncio.create_task(func)))


    # Run all tasks concurrently and collect results
    results = await asyncio.gather(*tasks)
    
    #elapsed = t2 - t1
    #print(elapsed)

suts = ['_test_check_malicious']
    
asyncio.run(_arun_tests(suts))


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
